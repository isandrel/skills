# Skills

Agent Skills for Claude Code, Codex, and other AI agents.

## Available Skills

| Skill | Category | Description |
|-------|----------|-------------|
| [skill-creator](skills/development/skill-creator/) | development | Create, validate, and package professional Agent Skills |
| [excalidraw-diagram](skills/obsidian/excalidraw-diagram/) | obsidian | Generate Excalidraw diagrams from text content for Obsidian |
| [obsidian-bases](skills/obsidian/obsidian-bases/) | obsidian | Create and edit Obsidian Bases (.base) YAML database views |
| [md-to-email](skills/tooling/md-to-email/) | tooling | Transform Markdown into styled HTML emails |
| [skill-manager](skills/tooling/skill-manager/) | tooling | Install, list, and manage skills across multiple AI agents |

## Repository Structure

```
skills/
├── skills/               # Individual skills by category
│   ├── development/
│   │   └── skill-creator/
│   ├── obsidian/
│   │   ├── excalidraw-diagram/
│   │   └── obsidian-bases/
│   └── tooling/
│       ├── md-to-email/
│       └── skill-manager/
├── spec/                 # Agent Skills specification
├── template/             # Starter template for new skills
├── CONTRIBUTING.md       # Contribution guidelines
└── SKILLS_PROMPT.md      # Prompt for non-native agent support
```

## Creating a Skill

1. Use `skill-creator` to scaffold:
   ```bash
   python skills/development/skill-creator/scripts/init_skill.py my-skill \
     --path skills/ --category <category>
   ```
2. Edit `SKILL.md` with your skill's instructions
3. Add scripts, references, or assets as needed

See [CONTRIBUTING.md](CONTRIBUTING.md) for full guidelines.

### SKILL.md Format

```yaml
---
name: my-skill-name
description: A clear description of what this skill does and when to use it
---

# My Skill Name

[Instructions that the agent will follow when this skill is active]
```

## Usage

### Claude Code
```bash
claude skill install isandrel/skills/skills/[category]/[skill-name]
```

### openskills (Cross-platform)
```bash
openskills install isandrel/skills/skills/[category]/[skill-name]
```

## Resources

- [What are skills?](https://support.claude.com/en/articles/12512176-what-are-skills)
- [Creating custom skills](https://support.claude.com/en/articles/12512198-creating-custom-skills)
- [Anthropic Skills Repo](https://github.com/anthropics/skills)

## License

AGPL-3.0
