# Agent Skills Specification

## Overview

Skills are folders containing instructions, scripts, and resources that AI agents load dynamically to improve performance on specialized tasks.

## File Structure

### Required Files

| File       | Description                                                           |
| ---------- | --------------------------------------------------------------------- |
| `SKILL.md` | Main skill definition with YAML frontmatter and markdown instructions |

### Optional Directories

| Directory     | Description                                     |
| ------------- | ----------------------------------------------- |
| `scripts/`    | Executable scripts (bash, python, etc.)         |
| `references/` | Documentation loaded on-demand                  |
| `assets/`     | Templates, fonts, images, or other static files |

## SKILL.md Format

### Frontmatter (Required)

```yaml
---
name: skill-name          # Unique identifier, lowercase with hyphens
description: |            # What the skill does and when to use it
  Multi-line description
  explaining the skill's purpose
---
```

### Content (Markdown)

The body contains:
- **Instructions**: What the agent should do
- **Examples**: Sample inputs/outputs
- **Guidelines**: Constraints and preferences

## Progressive Disclosure

Skills use progressive disclosure to maintain concise context:
- Full instructions load only when the skill is activated
- References are loaded on-demand when needed
- Scripts are executed only when called

## Compatibility

This spec is compatible with:
- Claude Code (Anthropic)
- OpenAI Codex
- GitHub Copilot (via AGENTS.md)
- Google Gemini
- Any agent supporting openskills

## Versioning

Use semantic versioning in an optional `version` frontmatter field:

```yaml
---
name: my-skill
version: 1.0.0
description: ...
---
```
