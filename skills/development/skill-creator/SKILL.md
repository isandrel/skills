---
name: skill-creator
description: "Comprehensive toolkit for creating professional Agent Skills with proper structure, validation, and packaging. Includes customizable templates, config-based defaults, modern validation with rich output, and automated packaging. Use when: (1) Creating new skills, (2) Validating skill structure, (3) Packaging skills for distribution, or (4) Learning skill development best practices."
---

# Skill Creator

Comprehensive guidance and tools for creating effective skills.

## About Skills

Skills are modular, self-contained packages that extend an AI agent's capabilities by providing specialized knowledge, workflows, and tools. They transform a general-purpose agent into a specialized one equipped with procedural knowledge.

### What Skills Provide

1. Specialized workflows - Multi-step procedures for specific domains
2. Tool integrations - Instructions for working with specific file formats or APIs
3. Domain expertise - Company-specific knowledge, schemas, business logic
4. Bundled resources - Scripts, references, and assets for complex and repetitive tasks

## Core Design Principles

For detailed principles including conciseness, freedom levels, and progressive disclosure patterns, see [references/skill-design-guide.md](references/skill-design-guide.md).

**Key takeaways:**
- Only add context the agent doesn't already have
- Keep SKILL.md under 500 lines
- Use progressive disclosure (metadata → SKILL.md → bundled resources)
- Match specificity to the task's fragility

## Anatomy of a Skill

```
skill-name/
├── SKILL.md (required)
│   ├── YAML frontmatter: name + description (required)
│   └── Markdown instructions (required)
├── config.toml (recommended) - User-customizable settings
└── Bundled Resources (optional)
    ├── scripts/          - Executable code (Python/Bash/etc.)
    ├── references/       - Documentation loaded into context as needed
    └── assets/           - Files used in output (templates, icons, fonts)
```

### SKILL.md Frontmatter

Only `name` and `description` fields. The description is the primary triggering mechanism — include both what the skill does and specific triggers/contexts for when to use it.

### Bundled Resources

| Directory | Purpose | When to Use |
|-----------|---------|-------------|
| `scripts/` | Executable code | Same code rewritten repeatedly; deterministic reliability needed |
| `references/` | Documentation | Claude should reference while working; keeps SKILL.md lean |
| `assets/` | Output files | Templates, images, fonts used in final output |
| `config.toml` | Settings | User-specific paths, dependencies, feature flags |

**Config pattern** — use `base_dir` + relative paths:

```toml
[paths]
base_dir = "~/Documents/project/data"
input = "raw/input.csv"
output = "processed/output.json"
```

## Skill Creation Process

1. Understand the skill with concrete examples
2. Plan reusable skill contents (scripts, references, assets)
3. Initialize the skill (run init_skill.py)
4. Edit the skill (implement resources and write SKILL.md)
5. Package the skill (run package_skill.py)
6. Iterate based on real usage

### Step 1: Understanding the Skill

Skip only when skill usage patterns are already clearly understood.

Gather concrete examples of how the skill will be used:
- "What functionality should the skill support?"
- "Can you give examples of how this would be used?"
- "What would a user say that should trigger this skill?"

### Step 2: Planning Reusable Contents

Analyze each example to identify what scripts, references, and assets would help:
- Repeated code → `scripts/`
- Domain knowledge or schemas → `references/`
- Boilerplate or templates → `assets/`

### Step 3: Initializing the Skill

Run `init_skill.py` to generate a template skill directory:

```bash
scripts/init_skill.py <skill-name> --path <output-directory> --category <category>
```

The `--category` flag places the skill inside a category subfolder (e.g., `--category tooling` creates `<path>/tooling/<skill-name>/`).

### Step 4: Edit the Skill

When editing, remember the skill is for another AI agent instance. Include non-obvious procedural knowledge and domain-specific details.

#### Learn Proven Design Patterns

- **Multi-step processes**: See [references/workflows.md](references/workflows.md)
- **Output formats or quality standards**: See [references/output-patterns.md](references/output-patterns.md)
- **Core principles & progressive disclosure**: See [references/skill-design-guide.md](references/skill-design-guide.md)

#### Start with Reusable Contents

Implement `scripts/`, `references/`, and `assets/` files first. Test scripts by running them. Delete unneeded example files.

#### Update SKILL.md

**Writing Guidelines:** Always use imperative/infinitive form.

**Frontmatter:**
- `name`: The skill name
- `description`: Include what the skill does AND specific triggers/contexts. All "when to use" information belongs here, not in the body.

**Body:** Instructions for using the skill and its bundled resources.

### Step 5: Packaging

```bash
scripts/package_skill.py <path/to/skill-folder> [output-dir]
```

The script validates (frontmatter, naming, structure, description quality) then packages into a `.skill` zip file. Fix any validation errors and re-run.

### Step 6: Iterate

1. Use the skill on real tasks
2. Notice struggles or inefficiencies
3. Update SKILL.md or bundled resources
4. Test again
