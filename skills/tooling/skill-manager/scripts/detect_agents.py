#!/usr/bin/env python3
"""Detect installed AI coding agents."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Agent:
    """Agent definition."""
    name: str
    display_name: str
    skills_path: Path
    local_skills_dir: str  # e.g., ".claude/skills" for project-local
    detect_cmd: list[str] | None = None
    detect_path: Path | None = None
    builtin_install: str | None = None


# Agent registry - add new agents here
AGENTS: list[Agent] = [
    Agent(
        name="claude",
        display_name="Claude Code",
        skills_path=Path.home() / ".claude" / "skills",
        local_skills_dir=".claude/skills",
        detect_cmd=["claude", "--version"],
        builtin_install="claude skill install",
    ),
    Agent(
        name="codex",
        display_name="Codex",
        skills_path=Path(os.environ.get("CODEX_HOME", Path.home() / ".codex")) / "skills",
        local_skills_dir=".codex/skills",
        detect_cmd=["codex", "--version"],
        builtin_install="codex skill install",
    ),
    Agent(
        name="opencode",
        display_name="OpenCode",
        skills_path=Path.home() / ".config" / "opencode" / "skills",
        local_skills_dir=".opencode/skills",
        detect_cmd=["opencode", "--version"],
    ),
    Agent(
        name="cursor",
        display_name="Cursor",
        skills_path=Path.home() / ".cursor" / "skills",
        local_skills_dir=".cursor/skills",
        detect_path=Path.home() / ".cursor",
    ),
    Agent(
        name="windsurf",
        display_name="Windsurf",
        skills_path=Path.home() / ".windsurf" / "skills",
        local_skills_dir=".windsurf/skills",
        detect_path=Path.home() / ".windsurf",
    ),
    Agent(
        name="antigravity",
        display_name="Antigravity",
        skills_path=Path.home() / ".gemini" / "antigravity" / "skills",
        local_skills_dir=".agent/skills",
        detect_path=Path.home() / ".gemini" / "antigravity",
    ),
]


def detect_agent(agent: Agent) -> dict | None:
    """Check if an agent is installed."""
    version = None
    
    # Check by command
    if agent.detect_cmd:
        if shutil.which(agent.detect_cmd[0]):
            try:
                result = subprocess.run(
                    agent.detect_cmd,
                    capture_output=True,
                    text=True,
                    timeout=5,
                )
                if result.returncode == 0:
                    version = result.stdout.strip().split("\n")[0]
            except (subprocess.TimeoutExpired, FileNotFoundError):
                pass
    
    # Check by path existence
    if agent.detect_path and agent.detect_path.exists():
        version = version or "detected"
    
    if version:
        return {
            "name": agent.name,
            "display_name": agent.display_name,
            "version": version,
            "skills_path": str(agent.skills_path),
            "local_skills_dir": agent.local_skills_dir,
            "builtin_install": agent.builtin_install,
        }
    return None


def detect_all() -> list[dict]:
    """Detect all installed agents."""
    detected = []
    for agent in AGENTS:
        result = detect_agent(agent)
        if result:
            detected.append(result)
    return detected


def main(argv: list[str]) -> int:
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Detect installed AI agents")
    parser.add_argument("--format", choices=["text", "json"], default="text")
    parser.add_argument("--agent", help="Check specific agent only")
    args = parser.parse_args(argv)
    
    if args.agent:
        agent = next((a for a in AGENTS if a.name == args.agent), None)
        if not agent:
            print(f"Unknown agent: {args.agent}", file=sys.stderr)
            return 1
        result = detect_agent(agent)
        agents = [result] if result else []
    else:
        agents = detect_all()
    
    if args.format == "json":
        print(json.dumps(agents, indent=2))
    else:
        if not agents:
            print("🔍 No AI agents detected.")
            return 0
        print("🤖 Detected AI Agents:")
        for i, agent in enumerate(agents, 1):
            icon = "🔧" if agent["builtin_install"] else "📁"
            print(f"  {icon} [{i}] {agent['display_name']} ({agent['version']})")
            print(f"      └─ {agent['skills_path']}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
