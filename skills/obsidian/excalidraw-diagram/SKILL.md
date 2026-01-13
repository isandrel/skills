---
name: excalidraw-diagram
description: |
  Generate Excalidraw diagrams from text content for Obsidian.
  Use when user asks to create diagrams, flowcharts, mind maps, or visual representations.
  Triggers: "excalidraw", "diagram", "flowchart", "mind map", "visualize", "draw".
metadata:
  version: 0.0.1
  category: obsidian
  author: isandrel
---

# Excalidraw Diagram Generator

Create publication-quality Excalidraw diagrams from text content, outputting Obsidian-ready `.md` files with proper JSON structure.

## Quick Start

1. Analyze the user's content for concepts and relationships
2. Select the most appropriate diagram type
3. Generate valid Excalidraw JSON with proper element binding
4. Save as Obsidian-compatible `.md` file
5. Provide viewing instructions

## Diagram Type Selection

Choose based on content structure and communication goals:

### Flowchart
**Use for**: Sequential processes, decision trees, algorithms, workflows
**Structure**: Start → Steps → Decision points → End
**Best practices**:
- Use diamonds for decisions, rectangles for actions
- Keep flow direction consistent (top-to-bottom or left-to-right)
- Limit to 7-10 steps per diagram; split complex flows
- Label all decision branches (Yes/No, True/False)

### Mind Map
**Use for**: Brainstorming, topic exploration, knowledge organization
**Structure**: Central concept radiating outward
**Best practices**:
- Central node should be largest and most prominent
- Use color-coding for different branches
- Limit depth to 3-4 levels for readability
- Balance branches visually around the center

### Hierarchy / Org Chart
**Use for**: Organizational structures, taxonomies, system decomposition
**Structure**: Root at top, children below
**Best practices**:
- Align siblings horizontally
- Use consistent spacing between levels
- Container boxes for departments/groups
- Consider left-to-right for deep hierarchies

### Relationship Diagram
**Use for**: Dependencies, system interactions, entity relationships
**Structure**: Nodes with labeled connecting lines
**Best practices**:
- Use arrowheads to show direction of relationship
- Label connections with relationship type
- Group related entities with background shapes
- Minimize crossing lines

### Comparison Chart
**Use for**: Feature comparison, pros/cons, A vs B analysis
**Structure**: Side-by-side columns or rows
**Best practices**:
- Use consistent layout for compared items
- Color-code positive (green) and negative (red) aspects
- Include a legend if using symbols
- Align comparison points horizontally

### Timeline
**Use for**: Historical events, project milestones, evolution
**Structure**: Linear time axis with event markers
**Best practices**:
- Consistent spacing for equal time intervals
- Alternate event labels above/below line to avoid overlap
- Use icons or colors to categorize events
- Mark the present or key reference points

### Matrix / Quadrant
**Use for**: Priority mapping, 2D classification, positioning
**Structure**: X-Y axes dividing space into regions
**Best practices**:
- Label both axes clearly
- Name each quadrant
- Size items by importance if applicable
- Use the Eisenhower matrix pattern for priority

### Freeform Canvas
**Use for**: Initial sketches, mixed diagrams, creative layouts
**Structure**: No fixed structure
**Best practices**:
- Group related elements
- Use frames to create sections
- Maintain visual balance
- Add annotations for context

## Output Format

### Obsidian Markdown Structure

```markdown
---
excalidraw-plugin: parsed
tags: [excalidraw]
---
==⚠  Switch to EXCALIDRAW VIEW in the MORE OPTIONS menu of this document. ⚠== You can decompress Drawing data with the command palette: 'Decompress current Excalidraw file'. For more info check in plugin settings under 'Saving'

# Excalidraw Data

## Text Elements
%%
## Drawing
\`\`\`json
{EXCALIDRAW_JSON}
\`\`\`
%%
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

## Design System

### Typography Scale

| Level   | Size    | Weight    | Use Case                      |
| ------- | ------- | --------- | ----------------------------- |
| H1      | 28px    | Bold      | Diagram title, main concept   |
| H2      | 22px    | Semi-bold | Section headers, major nodes  |
| H3      | 18px    | Medium    | Sub-sections, secondary nodes |
| Body    | 14-16px | Regular   | Descriptions, annotations     |
| Caption | 12px    | Light     | Labels, footnotes             |

**Font**: Always use `fontFamily: 5` (Excalifont) for consistent hand-drawn aesthetic.

### Color System

#### Semantic Colors

| Purpose     | Primary   | Background   | Hex Primary | Hex BG    |
| ----------- | --------- | ------------ | ----------- | --------- |
| Information | Deep Blue | Light Blue   | `#1e40af`   | `#dbeafe` |
| Success     | Green     | Light Green  | `#10b981`   | `#d1fae5` |
| Warning     | Amber     | Light Amber  | `#f59e0b`   | `#fef3c7` |
| Error       | Red       | Light Red    | `#ef4444`   | `#fee2e2` |
| Neutral     | Gray      | Light Gray   | `#374151`   | `#f3f4f6` |
| Accent      | Purple    | Light Purple | `#8b5cf6`   | `#ede9fe` |

#### Color Usage Guidelines

- **Title/Headers**: Deep Blue (`#1e40af`)
- **Connections/Arrows**: Medium Blue (`#3b82f6`) or Gray (`#374151`)
- **Body Text**: Dark Gray (`#374151`)
- **Highlights**: Amber (`#f59e0b`)
- **Backgrounds**: Use light variants at 10-20% opacity

### Layout Grid

| Property       | Value         | Purpose                      |
| -------------- | ------------- | ---------------------------- |
| Canvas         | 1200 × 900 px | Default working area         |
| Vertical gap   | 60-80px       | Between flow elements        |
| Horizontal gap | 40-60px       | Between parallel branches    |
| Arrow gap      | 5px           | Distance from element edge   |
| Title margin   | 40px          | Below title to first element |

### Element Dimensions

| Element   | Width     | Height  | Roundness          |
| --------- | --------- | ------- | ------------------ |
| Title     | auto      | 36px    | n/a (text)         |
| Start/End | 160-200px | 50px    | `type: 3` (full)   |
| Process   | 240-300px | 60px    | `type: 3` (slight) |
| Decision  | 180px     | 120px   | n/a (diamond)      |
| Error box | 200-280px | 60-80px | `type: 3` (full)   |

### Positioning Rules

1. **Title**: Centered horizontally, top of canvas (y: 20-40)
2. **Start node**: Centered below title
3. **Main flow**: Vertical center alignment (x: ~500-600)
4. **Decisions**: Centered on main flow
5. **Error states**: Branch **left** from decisions (x: 80-200)
6. **Sub-processes**: Branch **right** from decisions
7. **Arrows**: Exit from bottom, enter from top (for vertical flow)

### Visual Hierarchy

1. **Size**: Larger = more important
2. **Color**: Saturated = draws attention
3. **Position**: Center/top = primary focus
4. **Stroke**: Thicker = emphasis (strokeWidth: 2)
5. **Fill**: Solid bg = contained concept

## JSON Structure

### Root Document

```json
{
  "type": "excalidraw",
  "version": 2,
  "source": "https://github.com/zsviczian/obsidian-excalidraw-plugin",
  "elements": [],
  "appState": {
    "gridSize": null,
    "viewBackgroundColor": "#ffffff"
  },
  "files": {}
}
```

### Element Index System

Use alphabetical indexing for layer ordering:
- `a0`, `a1`, `a2` ... for first layer
- `b0`, `b1`, `b2` ... for second layer
- Arrows typically on higher layer than shapes

### Element ID Conventions

Use semantic, readable IDs:
- `title-main`, `node-auth`, `arrow-1-to-2`
- Avoid: `abcd1234`, `elem1`, `x`

### Binding Patterns

#### Text Inside Container

```json
// Container
{
  "id": "box-auth",
  "type": "rectangle",
  "boundElements": [{ "id": "text-auth", "type": "text" }]
}

// Text
{
  "id": "text-auth",
  "type": "text",
  "containerId": "box-auth",
  "verticalAlign": "middle",
  "textAlign": "center"
}
```

#### Arrow Connecting Shapes

```json
{
  "id": "arrow-1-to-2",
  "type": "arrow",
  "startBinding": {
    "elementId": "box-1",
    "focus": 0,
    "gap": 5
  },
  "endBinding": {
    "elementId": "box-2",
    "focus": 0,
    "gap": 5
  }
}
```

## Common Patterns

### Flowchart Pattern

```
          [Title]
             
          (Start)
             ↓
        [Process 1]
             ↓
       <Decision 1?>
     No ↙       ↘ Yes
[Alt/Error]    [Process 2]
                   ↓
              <Decision 2?>
            No ↓       ↘ Yes
               ↓    [Sub-process]
               ↓         ↓
          [Final Step]←──┘
               ↓
            (End)
```

#### Element Types & Colors

| Element         | Shape        | Stroke    | Background | Use                        |
| --------------- | ------------ | --------- | ---------- | -------------------------- |
| **Title**       | Text only    | `#1e40af` | none       | Diagram heading            |
| **Start/End**   | Rounded rect | `#10b981` | `#d1fae5`  | Entry/exit points          |
| **Process**     | Rectangle    | `#3b82f6` | `#dbeafe`  | Actions, steps             |
| **Decision**    | Diamond      | `#f59e0b` | `#fef3c7`  | Yes/No branches            |
| **Error/Alt**   | Rounded rect | `#ef4444` | `#fee2e2`  | Failure/alternative states |
| **Sub-process** | Rectangle    | `#8b5cf6` | `#ede9fe`  | External/optional actions  |

#### Arrow Labels
- Place **Yes/No** labels near decision diamonds
- Main flow continues downward or rightward
- Alternatives/errors branch left

#### Layout
- **Title**: Top center, largest text
- **Main flow**: Vertical, top-to-bottom
- **Errors**: Branch left from decisions
- **Sub-processes**: Branch right, rejoin main flow

### Mind Map Pattern

```
              [Branch 1]
                  ↑
[Sub] ← [Central Topic] → [Branch 2]
                  ↓
              [Branch 3] → [Sub-branch]
```

- Large central node
- Radiating structure
- Color per branch
- Decreasing node size by depth

### Architecture Pattern

```
┌─────────────────────────────────┐
│           Frontend              │
├─────────────────────────────────┤
│    API Gateway / Load Balancer  │
├─────────────────────────────────┤
│  Service A  │  Service B  │ ... │
├─────────────────────────────────┤
│         Database Layer          │
└─────────────────────────────────┘
```

- Layered rectangles
- Clear separation lines
- Labels for each layer
- Arrows for data flow

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
- [Obsidian Excalidraw Plugin](https://github.com/zsviczian/obsidian-excalidraw-plugin)
- [Excalidraw Official Docs](https://docs.excalidraw.com)
