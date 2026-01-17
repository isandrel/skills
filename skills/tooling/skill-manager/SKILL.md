---
name: skill-manager
description: |
  Manage AI agent skills across multiple platforms. Detects installed agents,
  installs skills from GitHub, lists installed skills, and uninstalls.
  Triggers: "install skill", "manage skills", "list skills", "uninstall skill".
metadata:
  version: 0.1.0
  category: tooling
  author: isandrel
---

# Skill Manager

Universal skill manager for AI coding agents. Automatically detects installed agents
and installs skills using the best available method.

## Supported Agents

Run `scripts/detect_agents.py` to see which agents are available on this system.
Agent definitions are in `references/agents.md` for easy extensibility.

## Commands

### Install a skill

```bash
python scripts/install.py <source> [options]
```

**Source formats:**
- GitHub shorthand: `owner/repo/path/to/skill`
- GitHub URL: `https://github.com/owner/repo/tree/main/skills/my-skill`
- Local path: `/path/to/local/skill`

**Options:**
| Option             | Description                                            |
| ------------------ | ------------------------------------------------------ |
| `--agents <a1,a2>` | Install to specific agents (default: `all`)            |
| `--local`          | Install to project-local dir (e.g., `.claude/skills/`) |
| `--symlink`        | Create symlinks instead of copying                     |
| `--method`         | Force: `auto`, `builtin`, `git`, `download`            |

### List installed skills

```bash
python scripts/list.py [--agent <agent>]
```

### Uninstall a skill

```bash
python scripts/uninstall.py <skill-name> [--agents <a1,a2>]
```

## Workflow

When user asks to install a skill:

1. **Detect agents** → Run `scripts/detect_agents.py`
2. **Present options** → Show detected agents, ask which to install to
3. **Install** → Run `scripts/install.py` with user's choices
4. **Confirm** → Tell user to restart their agent

## Install Method Priority

1. **Built-in CLI** (if agent supports it, e.g., `claude skill install`)
2. **Git sparse-checkout** (efficient, downloads only needed files)
3. **Direct download** (download zip, extract)

## Examples

### Install to user space (default)

```
python scripts/install.py anthropics/skills/skills/prompt-engineering
→ ~/.claude/skills/prompt-engineering
→ ~/.codex/skills/prompt-engineering
```

### Install to project-local

```
python scripts/install.py anthropics/skills/skills/prompt-engineering --local
→ ./.claude/skills/prompt-engineering
```

### Install using symlink (for development)

```
python scripts/install.py /path/to/local/skill --symlink --agents claude
→ ~/.claude/skills/my-skill → /path/to/local/skill
```

## Requirements

- Python 3.8+
- Git (for sparse-checkout method)
- No external dependencies (stdlib only)

## References

- [references/agents.md](references/agents.md) - Agent detection and install paths
