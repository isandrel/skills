#!/usr/bin/env python3
"""List installed skills."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from detect_agents import detect_all


def list_skills(agent_filter: str | None = None) -> dict:
    """List installed skills for all or specific agents."""
    detected = detect_all()
    
    if agent_filter:
        detected = [a for a in detected if a["name"] == agent_filter]
    
    results = {}
    for agent in detected:
        skills_path = Path(agent["skills_path"])
        skills = []
        
        if skills_path.exists():
            for skill_dir in skills_path.iterdir():
                if skill_dir.is_dir() and (skill_dir / "SKILL.md").exists():
                    skills.append({
                        "name": skill_dir.name,
                        "path": str(skill_dir),
                        "symlink": skill_dir.is_symlink(),
                    })
        
        results[agent["name"]] = {
            "display_name": agent["display_name"],
            "skills_path": agent["skills_path"],
            "skills": sorted(skills, key=lambda x: x["name"]),
        }
    
    return results


def main(argv: list[str]) -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(description="List installed skills")
    parser.add_argument("--agent", help="Filter to specific agent")
    parser.add_argument("--format", choices=["text", "json"], default="text")
    args = parser.parse_args(argv)
    
    results = list_skills(args.agent)
    
    if args.format == "json":
        print(json.dumps(results, indent=2))
    else:
        if not results:
            print("🔍 No AI agents detected.")
            return 0
        
        for name, data in results.items():
            skills = data["skills"]
            count = len(skills)
            print(f"🤖 {data['display_name']} ({count} skill{'s' if count != 1 else ''}):")
            
            if not skills:
                print("   (none)")
            else:
                for skill in skills:
                    icon = "🔗" if skill["symlink"] else "📦"
                    print(f"   {icon} {skill['name']}")
            print()
    
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
