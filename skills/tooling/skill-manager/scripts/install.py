#!/usr/bin/env python3
"""Install a skill from GitHub or local path."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
import urllib.error
import urllib.parse
import urllib.request
import zipfile
from dataclasses import dataclass
from pathlib import Path

# Import agent detection
from detect_agents import AGENTS, detect_all


@dataclass
class Source:
    """Parsed skill source."""
    owner: str
    repo: str
    ref: str
    path: str
    skill_name: str


class InstallError(Exception):
    """Installation error."""
    pass


def parse_github_url(url: str, default_ref: str = "main") -> Source:
    """Parse a GitHub URL into components."""
    parsed = urllib.parse.urlparse(url)
    if parsed.netloc not in ("github.com", "www.github.com"):
        raise InstallError("Only GitHub URLs are supported.")
    
    parts = [p for p in parsed.path.split("/") if p]
    if len(parts) < 2:
        raise InstallError("Invalid GitHub URL.")
    
    owner, repo = parts[0], parts[1]
    ref = default_ref
    subpath = ""
    
    if len(parts) > 2:
        if parts[2] in ("tree", "blob"):
            if len(parts) < 4:
                raise InstallError("GitHub URL missing ref or path.")
            ref = parts[3]
            subpath = "/".join(parts[4:])
        else:
            subpath = "/".join(parts[2:])
    
    skill_name = subpath.rstrip("/").split("/")[-1] if subpath else repo
    
    return Source(
        owner=owner,
        repo=repo,
        ref=ref,
        path=subpath,
        skill_name=skill_name,
    )


def parse_shorthand(shorthand: str, default_ref: str = "main") -> Source:
    """Parse owner/repo/path shorthand."""
    parts = shorthand.split("/")
    if len(parts) < 2:
        raise InstallError("Invalid shorthand. Use: owner/repo[/path/to/skill]")
    
    owner = parts[0]
    repo = parts[1]
    path = "/".join(parts[2:]) if len(parts) > 2 else ""
    skill_name = parts[-1] if len(parts) > 2 else repo
    
    return Source(
        owner=owner,
        repo=repo,
        ref=default_ref,
        path=path,
        skill_name=skill_name,
    )


def github_request(url: str) -> bytes:
    """Make a GitHub API request."""
    headers = {"User-Agent": "skill-manager"}
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if token:
        headers["Authorization"] = f"token {token}"
    
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return resp.read()
    except urllib.error.HTTPError as e:
        raise InstallError(f"HTTP {e.code}: {e.reason}") from e


def install_builtin(source: Source, agent_cmd: str) -> bool:
    """Try to install using agent's built-in command."""
    cmd_parts = agent_cmd.split()
    skill_ref = f"{source.owner}/{source.repo}"
    if source.path:
        skill_ref += f"/{source.path}"
    
    cmd = [*cmd_parts, skill_ref]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False


def install_git_sparse(source: Source, dest: Path) -> bool:
    """Install using git sparse-checkout."""
    if not shutil.which("git"):
        return False
    
    with tempfile.TemporaryDirectory() as tmp:
        repo_dir = Path(tmp) / "repo"
        repo_url = f"https://github.com/{source.owner}/{source.repo}.git"
        
        # Clone with sparse checkout
        clone_cmd = [
            "git", "clone",
            "--filter=blob:none",
            "--depth", "1",
            "--sparse",
            "--single-branch",
            "--branch", source.ref,
            repo_url,
            str(repo_dir),
        ]
        
        try:
            subprocess.run(clone_cmd, capture_output=True, check=True, timeout=60)
        except subprocess.CalledProcessError:
            return False
        
        # Set sparse-checkout to only include our path
        if source.path:
            sparse_cmd = ["git", "-C", str(repo_dir), "sparse-checkout", "set", source.path]
            subprocess.run(sparse_cmd, capture_output=True, check=True)
        
        # Copy skill files to destination
        src_path = repo_dir / source.path if source.path else repo_dir
        if not src_path.exists():
            return False
        
        dest.mkdir(parents=True, exist_ok=True)
        shutil.copytree(src_path, dest, dirs_exist_ok=True)
        
        # Remove .git if copied
        git_dir = dest / ".git"
        if git_dir.exists():
            shutil.rmtree(git_dir)
        
        return True


def install_download(source: Source, dest: Path) -> bool:
    """Install by downloading repo zip."""
    zip_url = f"https://codeload.github.com/{source.owner}/{source.repo}/zip/{source.ref}"
    
    try:
        payload = github_request(zip_url)
    except InstallError:
        return False
    
    with tempfile.TemporaryDirectory() as tmp:
        zip_path = Path(tmp) / "repo.zip"
        zip_path.write_bytes(payload)
        
        with zipfile.ZipFile(zip_path, "r") as zf:
            zf.extractall(tmp)
        
        # Find extracted directory (usually repo-ref)
        extracted = next(Path(tmp).glob(f"{source.repo}-*"), None)
        if not extracted:
            return False
        
        src_path = extracted / source.path if source.path else extracted
        if not src_path.exists():
            return False
        
        dest.mkdir(parents=True, exist_ok=True)
        shutil.copytree(src_path, dest, dirs_exist_ok=True)
        return True


def install_local(local_path: Path, dest: Path, symlink: bool = False) -> bool:
    """Install from local path."""
    if not local_path.exists():
        return False
    
    dest.parent.mkdir(parents=True, exist_ok=True)
    
    if symlink:
        if dest.exists():
            dest.unlink() if dest.is_symlink() else shutil.rmtree(dest)
        dest.symlink_to(local_path.resolve())
    else:
        dest.mkdir(parents=True, exist_ok=True)
        shutil.copytree(local_path, dest, dirs_exist_ok=True)
    
    return True


def install_skill(
    source_str: str,
    agents: list[str] | None = None,
    symlink: bool = False,
    method: str = "auto",
    local: bool = False,
) -> dict:
    """Install a skill to specified agents."""
    results = {"installed": [], "failed": [], "skipped": []}
    
    # Parse source
    local_path = Path(source_str)
    if local_path.exists():
        source = None
        skill_name = local_path.name
    elif source_str.startswith("http"):
        source = parse_github_url(source_str)
        skill_name = source.skill_name
    else:
        source = parse_shorthand(source_str)
        skill_name = source.skill_name
    
    # Detect agents
    detected = {a["name"]: a for a in detect_all()}
    
    if not detected:
        raise InstallError("No AI agents detected on this system.")
    
    # Filter to requested agents
    if agents and agents != ["all"]:
        target_agents = {k: v for k, v in detected.items() if k in agents}
        if not target_agents:
            raise InstallError(f"None of the specified agents found: {agents}")
    else:
        target_agents = detected
    
    # Install to each agent
    for name, agent in target_agents.items():
        # Use project-local path if --local flag is set
        if local:
            base = Path.cwd() / agent.get("local_skills_dir", f".{name}/skills")
            dest = base / skill_name
        else:
            dest = Path(agent["skills_path"]) / skill_name
        
        if dest.exists() and not symlink:
            results["skipped"].append({
                "agent": name,
                "reason": "Already exists",
                "path": str(dest),
            })
            continue
        
        success = False
        method_used = None
        
        # Local install
        if local_path.exists():
            success = install_local(local_path, dest, symlink)
            method_used = "symlink" if symlink else "copy"
        
        # GitHub install
        elif source:
            # Try built-in first
            if method in ("auto", "builtin") and agent.get("builtin_install"):
                success = install_builtin(source, agent["builtin_install"])
                if success:
                    method_used = "builtin"
            
            # Try git sparse-checkout
            if not success and method in ("auto", "git"):
                success = install_git_sparse(source, dest)
                if success:
                    method_used = "git"
            
            # Try download
            if not success and method in ("auto", "download"):
                success = install_download(source, dest)
                if success:
                    method_used = "download"
        
        if success:
            results["installed"].append({
                "agent": name,
                "path": str(dest),
                "method": method_used,
            })
        else:
            results["failed"].append({
                "agent": name,
                "path": str(dest),
            })
    
    return results


def main(argv: list[str]) -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Install a skill")
    parser.add_argument("source", help="GitHub URL, shorthand, or local path")
    parser.add_argument("--agents", help="Comma-separated agents or 'all'", default="all")
    parser.add_argument("--symlink", action="store_true", help="Create symlinks")
    parser.add_argument("--local", action="store_true", help="Install to project-local skills dir")
    parser.add_argument("--method", choices=["auto", "builtin", "git", "download"], default="auto")
    parser.add_argument("--format", choices=["text", "json"], default="text")
    args = parser.parse_args(argv)
    
    agents = args.agents.split(",") if args.agents != "all" else ["all"]
    
    try:
        results = install_skill(args.source, agents, args.symlink, args.method, args.local)
    except InstallError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    
    if args.format == "json":
        print(json.dumps(results, indent=2))
    else:
        if results["installed"]:
            print("✅ Installed:")
            for item in results["installed"]:
                print(f"   📦 {item['agent']}: {item['path']} ({item['method']})")
        if results["skipped"]:
            print("⏭️  Skipped:")
            for item in results["skipped"]:
                print(f"   ⚠️  {item['agent']}: {item['reason']}")
        if results["failed"]:
            print("❌ Failed:")
            for item in results["failed"]:
                print(f"   💥 {item['agent']}: {item['path']}")
        
        if results["installed"]:
            print("\n🔄 Restart your agents to load the new skill.")
    
    return 1 if results["failed"] and not results["installed"] else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
