# Workflow Patterns

## Sequential Multi-Step Workflows

For complex tasks, break operations into clear sequential steps. Give the agent an overview at the start of SKILL.md using a **checklist with links** to step files:

```markdown
## Workflow

Progress:

- [ ] Step 1: Fetch the problem → Read [references/01-fetch-problem.md](references/01-fetch-problem.md)
- [ ] Step 2: Analyze and solve → Read [references/02-analyze-and-solve.md](references/02-analyze-and-solve.md)
- [ ] Step 3: Fill note sections → Read [references/03-fill-note-sections.md](references/03-fill-note-sections.md)
- [ ] Step 4: Verify and report → Read [references/04-verify-and-report.md](references/04-verify-and-report.md)

**Default**: Run Step 1 only. **Full workflow**: Run Steps 1 → 2 → 3 → 4 when user asks for it.
```

The checklist format gives the agent a visible progress tracker and makes navigation explicit.

## Step File Anatomy

Each step file (`references/NN-step-name.md`) should follow this structure:

```markdown
# Step N: Descriptive Title

Brief description of what this step does and when to run it.

## Process

1. First action
2. Second action
3. ...

## Rules / Guidelines

- Specific constraints
- Formatting requirements
- Edge cases

## Example

Concrete input/output example showing the expected result.

## Gotchas

- Common mistakes to avoid (optional but valuable)

## Next

Proceed to [Step N+1: Next Step](NN-next-step.md).
```

## File Naming Convention for Step Files

> Always zero-pad step numbers: `01-`, `02-`, `03-` — **never** `1-`, `2-`, `3-`

Zero-padding ensures correct alphabetical sort order in file browsers and editors.

| ❌ Wrong     | ✅ Correct                 |
| ------------ | -------------------------- |
| `1-fetch.md` | `01-fetch-problem.md`      |
| `2-solve.md` | `02-analyze-and-solve.md`  |
| `step3.md`   | `03-fill-note-sections.md` |

## Conditional Workflows

For tasks with branching logic, guide the agent through decision points:

```markdown
1. Determine the modification type: **Creating new content?** → Follow "Creation workflow" below **Editing existing content?** → Follow "Editing workflow" below

2. Creation workflow: [steps]
3. Editing workflow: [steps]
```

## Validation Loops

Always include a verification step at the end:

```markdown
## Verification

1. Make your edits
2. Run validation: `python scripts/validate.py output/`
3. If validation fails:
   - Review the error message
   - Fix the issues
   - Run validation again
4. Only proceed when validation passes
```

## Success Response Template

Define a consistent completion message:

```markdown
## Done

Report to the user: ✅ Task complete! 📍 File: `{filename}` ⚡ Summary: {brief result}
```
