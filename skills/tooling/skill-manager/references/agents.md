# Supported Agents

Agent definitions for skill-manager. Add new agents here.

## Agent Registry

| Agent      | Detection             | User Skills Path             | Project Skills Path |
| ---------- | --------------------- | ---------------------------- | ------------------- |
| `claude`   | `claude --version`    | `~/.claude/skills/`          | `.claude/skills/`   |
| `codex`    | `codex --version`     | `~/.codex/skills/`           | `.codex/skills/`    |
| `opencode` | `opencode --version`  | `~/.config/opencode/skills/` | `.opencode/skills/` |
| `cursor`   | `~/.cursor/` exists   | `~/.cursor/skills/`          | `.cursor/skills/`   |
| `windsurf` | `~/.windsurf/` exists | `~/.windsurf/skills/`        | `.windsurf/skills/` |
| `copilot`  | `.github/copilot/`    | `.github/copilot/skills/`    | (project-only)      |

---

## Agent Details

### Claude Code (Anthropic)

| Property             | Value                                                                       |
| -------------------- | --------------------------------------------------------------------------- |
| **CLI**              | `claude`                                                                    |
| **Built-in install** | `claude skill install owner/repo/path`                                      |
| **Config**           | `~/.claude/settings.json`                                                   |
| **Docs**             | [Claude Code Skills](https://docs.anthropic.com/en/docs/claude-code/skills) |

**Notes:**
- Skills are auto-loaded on startup
- Supports both user (`~/.claude/skills/`) and project (`.claude/skills/`) skills
- Project skills take precedence

---

### Codex (OpenAI)

| Property             | Value                                           |
| -------------------- | ----------------------------------------------- |
| **CLI**              | `codex`                                         |
| **Built-in install** | `codex skill install owner/repo/path`           |
| **Config**           | `$CODEX_HOME` (default: `~/.codex/`)            |
| **Docs**             | [Codex Skills](https://github.com/openai/codex) |

**Notes:**
- Similar skill format to Claude Code
- Curated skills at `openai/skills` repo
- Preinstalled system skills in `.system/`

---

### OpenCode

| Property             | Value                                              |
| -------------------- | -------------------------------------------------- |
| **CLI**              | `opencode`                                         |
| **Built-in install** | ❌ (use file-based)                                 |
| **Config**           | `~/.config/opencode/opencode.jsonc`                |
| **Docs**             | [OpenCode Skills](https://opencode.ai/docs/skills) |

**Notes:**
- Searches for `SKILL.md` in configured paths
- Compatible with Claude Code skill format

---

### Cursor

| Property             | Value                                                        |
| -------------------- | ------------------------------------------------------------ |
| **CLI**              | ❌                                                            |
| **Built-in install** | ❌ (use file-based)                                           |
| **Config**           | `~/.cursor/`                                                 |
| **Docs**             | [Cursor Rules](https://docs.cursor.com/context/rules-for-ai) |

**Notes:**
- Uses `.cursorrules` file format
- Skills in `~/.cursor/skills/` are experimental

---

### Windsurf (Codeium)

| Property             | Value                                              |
| -------------------- | -------------------------------------------------- |
| **CLI**              | ❌                                                  |
| **Built-in install** | ❌ (use file-based)                                 |
| **Config**           | `~/.windsurf/`                                     |
| **Docs**             | [Windsurf Docs](https://docs.codeium.com/windsurf) |

**Notes:**
- Similar architecture to Cursor
- Skills support is emerging

---

## Adding a New Agent

1. Add entry to the table above
2. Add to `AGENTS` list in `scripts/detect_agents.py`:

```python
Agent(
    name="new-agent",
    display_name="New Agent",
    skills_path=Path.home() / ".new-agent" / "skills",
    local_skills_dir=".new-agent/skills",
    detect_cmd=["new-agent", "--version"],  # or use detect_path
    builtin_install="new-agent skill install",  # if supported
),
```

3. Test detection: `python scripts/detect_agents.py`

---

## Related Resources

- [Agent Skills Specification](https://agentskills.io/specification)
- [Anthropic Skills Repo](https://github.com/anthropics/skills)
- [OpenAI Skills Repo](https://github.com/openai/skills)
