#!/usr/bin/env python3
"""Uninstall a skill."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

from detect_agents import detect_all


def uninstall_builtin(skill_name: str, agent: dict) -> bool:
    """Try to uninstall using agent's built-in command."""
    if not agent.get("builtin_install"):
        return False
    
    # Derive uninstall command from install command
    # "claude skill install" -> "claude skill remove"
    cmd_parts = agent["builtin_install"].replace("install", "remove").split()
    cmd = [*cmd_parts, skill_name]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False


def uninstall_skill(
    skill_name: str,
    agents: list[str] | None = None,
) -> dict:
    """Uninstall a skill from specified agents."""
    results = {"removed": [], "not_found": []}
    
    detected = {a["name"]: a for a in detect_all()}
    
    if not detected:
        return results
    
    # Filter to requested agents
    if agents and agents != ["all"]:
        target_agents = {k: v for k, v in detected.items() if k in agents}
    else:
        target_agents = detected
    
    for name, agent in target_agents.items():
        skill_path = Path(agent["skills_path"]) / skill_name
        removed = False
        method = None
        
        # Try built-in uninstall first
        if agent.get("builtin_install"):
            if uninstall_builtin(skill_name, agent):
                removed = True
                method = "builtin"
        
        # Fall back to file-based removal
        if not removed and skill_path.exists():
            if skill_path.is_symlink():
                skill_path.unlink()
            else:
                shutil.rmtree(skill_path)
            removed = True
            method = "file"
        
        if removed:
            results["removed"].append({
                "agent": name,
                "path": str(skill_path),
                "method": method,
            })
        else:
            results["not_found"].append({
                "agent": name,
                "path": str(skill_path),
            })
    
    return results


def main(argv: list[str]) -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Uninstall a skill")
    parser.add_argument("skill_name", help="Name of skill to uninstall")
    parser.add_argument("--agents", help="Comma-separated agents or 'all'", default="all")
    parser.add_argument("--format", choices=["text", "json"], default="text")
    args = parser.parse_args(argv)
    
    agents = args.agents.split(",") if args.agents != "all" else ["all"]
    results = uninstall_skill(args.skill_name, agents)
    
    if args.format == "json":
        print(json.dumps(results, indent=2))
    else:
        if results["removed"]:
            print("🗑️  Removed:")
            for item in results["removed"]:
                print(f"   ✅ {item['agent']}: {item['path']} ({item['method']})")
        if results["not_found"]:
            print("⚠️  Not found:")
            for item in results["not_found"]:
                print(f"   📭 {item['agent']}")
    
    return 0 if results["removed"] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
