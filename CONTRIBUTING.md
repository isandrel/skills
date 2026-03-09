# Contributing to Skills

Thank you for contributing! This guide covers how to add new skills, improve existing ones, and maintain quality standards.

## Creating a New Skill

### Quick Start

1. Use the `skill-creator` to scaffold a new skill:
   ```bash
   python skills/development/skill-creator/scripts/init_skill.py my-skill \
     --path skills/ --category <category>
   ```
   Categories: `development`, `obsidian`, `tooling` (or create a new one)

2. Edit `SKILL.md` — replace all TODO placeholders
3. Add scripts, references, and assets as needed
4. Delete any unused example files from the generated directories

### Alternatively, from Template

1. Copy `template/SKILL.md` into `skills/<category>/<skill-name>/`
2. Fill in frontmatter and instructions

## Skill Quality Checklist

Before submitting a PR, verify:

- [ ] `SKILL.md` has valid YAML frontmatter with **only** `name` and `description`
- [ ] `name` is lowercase, hyphenated, matches the directory name
- [ ] `description` explains **what** the skill does and **when** to use it
- [ ] SKILL.md body is **under 500 lines** — use `references/` for detailed content
- [ ] Directory uses only standard subdirectories: `scripts/`, `references/`, `assets/`
- [ ] Scripts are tested and executable
- [ ] No unnecessary files (CHANGELOG.md, INSTALLATION_GUIDE.md, etc.)
- [ ] Skill is placed in the appropriate category folder

## Naming Conventions

| Item | Convention | Example |
|------|-----------|---------|
| Skill directory | `kebab-case` | `md-to-email` |
| Category directory | `lowercase` | `tooling` |
| SKILL.md `name` field | Must match directory name | `md-to-email` |
| Scripts | `snake_case.py` | `validate.py` |
| References | `kebab-case.md` | `design-system.md` |

## Frontmatter Spec

Only two fields allowed:

```yaml
---
name: skill-name
description: "What the skill does and when to use it."
---
```

Do **not** include `metadata`, `version`, `category`, or `author` in frontmatter. See [spec/SPEC.md](spec/SPEC.md) for full specification.

## Pull Request Process

1. Fork the repository
2. Create a feature branch: `feat/<skill-name>` or `fix/<skill-name>`
3. Follow the quality checklist above
4. Submit a PR with a clear description of the skill's purpose

## Improving Existing Skills

- Keep changes focused — one skill per PR when possible
- If extracting content into references, update SKILL.md to link to the new reference files
- Test any modified scripts
