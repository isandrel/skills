# Skills

Agent Skills for Claude Code, Codex, and other AI agents.

## Repository Structure

```
skills/
├── skills/           # Individual skill folders
│   └── [skill-name]/
│       ├── SKILL.md      # Required: Instructions + metadata
│       ├── scripts/      # Optional: Executable code
│       ├── references/   # Optional: Documentation
│       └── assets/       # Optional: Templates, images
├── spec/             # Agent Skills specification
└── template/         # Starter template for new skills
```

## Creating a Skill

1. Copy the `template/` folder and rename it
2. Edit `SKILL.md` with your skill's instructions
3. Add any scripts, references, or assets as needed

### SKILL.md Format

```yaml
---
name: my-skill-name
description: A clear description of what this skill does and when to use it
---

# My Skill Name

[Instructions that the agent will follow when this skill is active]

## Examples
- Example usage 1
- Example usage 2

## Guidelines
- Guideline 1
- Guideline 2
```

## Usage

### Claude Code
```bash
# Install a skill from this repo
claude skill install isandrel/skills/skills/[category]/[skill-name]
```

### openskills (Cross-platform)
```bash
# Install for any agent that supports openskills
openskills install isandrel/skills/skills/[category]/[skill-name]
```

## Resources

- [What are skills?](https://support.claude.com/en/articles/12512176-what-are-skills)
- [Creating custom skills](https://support.claude.com/en/articles/12512198-creating-custom-skills)
- [Anthropic Skills Repo](https://github.com/anthropics/skills)

## License

AGPL-3.0
