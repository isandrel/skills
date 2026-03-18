---
name: excalidraw-diagram
description: |
  Generate Excalidraw diagrams from text content for Obsidian.
  Use when user asks to create diagrams, flowcharts, mind maps, or visual representations.
  Triggers: "excalidraw", "diagram", "flowchart", "mind map", "visualize", "draw".
---

# Excalidraw Diagram Generator

Create publication-quality Excalidraw diagrams from text content, outputting Obsidian-ready `.md` files with proper JSON structure.

## Workflow

### 1. Determine Target Path

**Priority order:**

1. **User provides path** → Verify it exists
   ```bash
   [ -d "$USER_PATH" ] && echo "Valid" || echo "Path not found"
   ```
   - If valid: use it
   - If invalid: inform user and ask for correction

2. **No path provided** → AI suggests with numbered options
   - Analyze diagram topic/domain
   - Search current workspace for relevant folders
   - Present numbered list for user to choose:
     ```
     📁 Where should I save this diagram?

     [1] ./path/to/relevant-folder/  (matches: topic keyword)
     [2] ./diagrams/                  (existing diagrams folder)
     [3] ./assets/                    (general assets folder)
     [4] ./ (current directory)
     [5] Create new folder...

     Enter number or type custom path:
     ```
   - Wait for user selection before proceeding

3. **Fallback** → Current working directory (`./`)

### 2. Generate Diagram

1. Analyze content for concepts and relationships
2. Select appropriate diagram type
3. Generate valid Excalidraw JSON with proper element binding

### 3. Save & Confirm

1. Save as Obsidian-compatible `.md` file to target path
2. Provide viewing instructions

## Diagram Type Selection

Choose based on content structure and communication goals:

| Type             | Use For                                          | Key Tips                               |
| ---------------- | ------------------------------------------------ | -------------------------------------- |
| **Flowchart**    | Sequential processes, decision trees, algorithms | 7-10 steps max; diamonds for decisions |
| **Mind Map**     | Brainstorming, topic exploration                 | Central node largest; 3-4 depth levels |
| **Hierarchy**    | Org charts, taxonomies                           | Align siblings; consistent spacing     |
| **Relationship** | Dependencies, entity relationships               | Label connections; minimize crossing   |
| **Comparison**   | Feature comparison, pros/cons                    | Side-by-side; color-code pos/neg       |
| **Timeline**     | Events, milestones                               | Alternate labels above/below           |
| **Matrix**       | Priority mapping, 2D classification              | Label both axes; name quadrants        |
| **Freeform**     | Sketches, mixed diagrams                         | Group related elements; use frames     |

## Output Format

### Obsidian Markdown Structure

```markdown
---
excalidraw-plugin: parsed
tags: [excalidraw]
---

==⚠ Switch to EXCALIDRAW VIEW in the MORE OPTIONS menu of this document. ⚠== You can decompress Drawing data with the command palette: 'Decompress current Excalidraw file'. For more info check in plugin settings under 'Saving'

# Excalidraw Data

## Text Elements

%%

## Drawing

\`\`\`json {EXCALIDRAW_JSON} \`\`\` %%
```

### Critical Requirements

| Requirement   | Details                                                           |
| ------------- | ----------------------------------------------------------------- |
| Frontmatter   | Must include `excalidraw-plugin: parsed` and `tags: [excalidraw]` |
| Warning       | Include exact warning text for user guidance                      |
| JSON wrapper  | Wrap JSON in `%%` markers (Obsidian comment)                      |
| Text Elements | Leave section empty—plugin auto-populates                         |

## File Naming Convention

**Format**: `{descriptive-name}.{diagram-type}.md`

| Example                         | Description           |
| ------------------------------- | --------------------- |
| `ci-cd-pipeline.flowchart.md`   | Deployment workflow   |
| `q1-roadmap.timeline.md`        | Quarterly planning    |
| `microservices.relationship.md` | System architecture   |
| `product-ideas.mindmap.md`      | Brainstorming session |
| `task-priorities.matrix.md`     | Eisenhower matrix     |

## Design & JSON Reference

For detailed specifications, load these references as needed:

- **[Design System](references/design-system.md)** — Typography, colors, layout grid, element dimensions, positioning rules, visual hierarchy
- **[JSON Reference](references/json-reference.md)** — Root document structure, element IDs, binding patterns, common diagram patterns
- **[Excalidraw Schema](references/excalidraw-schema.md)** — Complete element schema reference

## Quality Checklist

Before saving, verify:

- [ ] All elements have unique IDs
- [ ] Text uses `fontFamily: 5`
- [ ] Colors follow the design system
- [ ] Elements are within canvas bounds (1200×800)
- [ ] Arrows are properly bound to shapes
- [ ] Text is bound to containers where appropriate
- [ ] JSON is valid and complete
- [ ] Frontmatter is correct
- [ ] File name follows convention

## Success Response Template

```
✅ Excalidraw diagram created!

📍 **File**: `{filename}`
🎨 **Type**: {diagram-type}
💡 **Design choice**: {1-line rationale}

**To view in Obsidian:**
1. Open the file
2. Click ⋮ (More Options)
3. Select "Switch to EXCALIDRAW VIEW"

Need changes? Just describe what you'd like adjusted!
```

## References

- [Excalidraw JSON Schema](references/excalidraw-schema.md) - Complete element reference
- [Design System](references/design-system.md) - Typography, colors, layout
- [JSON Reference](references/json-reference.md) - Binding patterns, common patterns
- [Obsidian Excalidraw Plugin](https://github.com/zsviczian/obsidian-excalidraw-plugin)
- [Excalidraw Official Docs](https://docs.excalidraw.com)
