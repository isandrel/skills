---
name: skill-creator
description: |
  Create new Agent Skills with proper SKILL.md structure and best practices.
  Use when user asks to create, generate, or scaffold a new skill.
  Triggers: "create skill", "new skill", "skill generator", "scaffold skill", "make skill".
metadata:
  version: 0.0.1
  category: development
  author: isandrel
---

# Skill Creator

Generate well-structured Agent Skills following the Agent Skills specification.

## Workflow

### 1. Gather Requirements

Ask the user:
```
🛠️ Let's create a new skill!

1. **Skill name**: What should this skill be called? (lowercase, hyphens only)
2. **Purpose**: What does this skill do?
3. **Triggers**: What keywords/phrases should activate it?
4. **Category**: Where should it live?
   [1] development   [2] obsidian   [3] productivity
   [4] automation    [5] other (specify)
```

### 2. Validate Name

Ensure name follows Agent Skills spec:
- 1-64 characters
- Lowercase alphanumeric and hyphens only
- No leading/trailing/consecutive hyphens
- Match parent directory name

```
✓ Valid: data-processor, api-client, note-formatter
✗ Invalid: DataProcessor, -api, my--skill
```

### 3. Generate SKILL.md

Create file with this structure:

```markdown
---
name: {skill-name}
description: |
  {Clear description of what the skill does}
  {When the agent should use it}
  Triggers: "{trigger1}", "{trigger2}", "{trigger3}".
metadata:
  version: 0.0.1
  category: {category}
  author: {author}
---

# {Skill Title}

{One-line summary of the skill's purpose}

## Workflow

### 1. {First Step}
{Instructions}

### 2. {Second Step}
{Instructions}

## Guidelines

- {Guideline 1}
- {Guideline 2}

## Examples

### Example 1: {Use Case}
{Input → Output example}

## References

- [Reference 1](references/file.md)
```

### 4. Create Directory Structure

```bash
mkdir -p skills/{category}/{skill-name}/references
```

Generate files:
- `SKILL.md` - Main skill definition
- `references/` - Optional reference docs (if needed)

### 5. Suggest Improvements

Review the skill and suggest:
- Additional triggers for better discovery
- Edge cases to handle
- Reference docs to include
- Scripts for automation (if applicable)

## Best Practices

### Description Field
- **DO**: Include specific triggers and use cases
- **DON'T**: Keep it vague (e.g., "Helps with stuff")

```yaml
# Good
description: |
  Generate Mermaid diagrams from text. Use for flowcharts, 
  sequence diagrams, and architecture visualizations.
  Triggers: "mermaid", "diagram", "flowchart", "sequence".

# Bad
description: Makes diagrams.
```

### Instructions
- Keep under 500 lines (use references for details)
- Use progressive disclosure (load details on demand)
- Include concrete examples
- Specify output formats

### Triggers
Include varied phrases:
- Action verbs: "create", "generate", "make"
- Domain keywords: specific to skill's function
- Synonyms: multiple ways users might ask

## Quality Checklist

Before saving:
- [ ] Name follows spec (lowercase, hyphens)
- [ ] Description is clear and specific
- [ ] Triggers cover common user phrases
- [ ] Instructions are actionable
- [ ] Examples are included
- [ ] Directory matches skill name

## Success Response

```
✅ Skill created!

📁 Location: skills/{category}/{skill-name}/
📄 Files:
   - SKILL.md (main skill definition)
   - references/ (ready for docs)

🔗 To use in Codex:
   ln -s $(pwd)/skills/{category}/{skill-name} ~/.codex/skills/

Need to add reference docs or scripts? Just ask!
```

## References

- [Agent Skills Specification](https://agentskills.io/specification)
- [Anthropic Skills Repo](https://github.com/anthropics/skills)
