# Agent Skills System

This project uses the **Agent Skills** format for reusable AI instructions. Skills extend your capabilities with specialized knowledge and workflows.

## What Are Skills?

Skills are directories containing a `SKILL.md` file that defines:
- **When** to activate (triggers, keywords)
- **What** to do (step-by-step instructions)
- **How** to do it (examples, guidelines, references)

## Skills Location (Priority Order)

Search for skills in this order (first match wins):

### 1. Project-Local Skills
```
./.agent/skills/           # Current project
./skills/                  # Alternative project location
```

### 2. User-Level Skills
```
~/.codex/skills/           # OpenAI Codex CLI
~/.claude/skills/          # Claude Code
~/.cursor/skills/          # Cursor (if supported)
~/.config/agent-skills/    # XDG standard location
```

### 3. System-Level Skills
```
/usr/local/share/agent-skills/
```

## Tools with Native Skill Support

These tools natively understand the `SKILL.md` format:

| Tool                 | Skills Location     | Notes                            |
| -------------------- | ------------------- | -------------------------------- |
| **OpenAI Codex CLI** | `~/.codex/skills/`  | Full support, auto-discovery     |
| **Claude Code**      | `~/.claude/skills/` | Full support, `/skill` command   |
| **GitHub Copilot**   | Project root        | Via `AGENTS.md` or skill folders |
| **Google Gemini**    | Project root        | Via `AGENTS.md`                  |

For tools **without native support**, use this prompt to enable skill usage.

Each skill folder structure:
```
skill-name/
├── SKILL.md              # Required: Instructions and metadata
├── scripts/              # Optional: Executable code
├── references/           # Optional: Additional documentation
└── assets/               # Optional: Templates, images, data
```

## SKILL.md Format

```yaml
---
name: skill-name
description: What this skill does and when to use it.
metadata:
  version: "1.0"
  author: author-name
---

# Skill Title

[Markdown instructions the AI should follow]
```

## How to Use Skills

### 1. Skill Discovery
When the user's request matches a skill's description or triggers:
- Read the skill's `SKILL.md` file
- Follow its instructions precisely
- Reference additional files in `scripts/`, `references/`, or `assets/` as needed

### 2. Skill Activation
A skill should be activated when:
- User explicitly mentions the skill name
- User's request matches keywords in the skill's description
- The task domain aligns with the skill's purpose

### 3. Skill Execution
When executing a skill:
1. Load the full `SKILL.md` content
2. Follow the instructions step-by-step
3. Load referenced files only when needed (progressive disclosure)
4. Apply the skill's guidelines and constraints
5. Use the skill's output format if specified

## Available Skills

To discover available skills, list the contents of the skills directory. Each subdirectory with a `SKILL.md` file is a skill.

### Listing Skills
```bash
ls ~/.codex/skills/
```

### Reading a Skill
```bash
cat ~/.codex/skills/{skill-name}/SKILL.md
```

## Best Practices

1. **Match Triggers**: Activate skills when user intent matches skill description
2. **Follow Instructions**: Execute skill steps precisely as documented
3. **Progressive Loading**: Only load reference files when specifically needed
4. **Respect Constraints**: Follow any guidelines or output formats specified
5. **Cite Skills**: When using a skill, briefly mention which skill is being applied

## Example Workflow

User: "Create a flowchart diagram of the login process"

1. Recognize trigger: "flowchart", "diagram" → matches `excalidraw-diagram` skill
2. Load: `~/.codex/skills/excalidraw-diagram/SKILL.md`
3. Follow skill instructions to generate the diagram
4. Apply skill's design guidelines and output format
5. Save file using skill's naming convention

---

*This prompt enables AI assistants to use Agent Skills even in environments that don't natively support the SKILL.md format.*
