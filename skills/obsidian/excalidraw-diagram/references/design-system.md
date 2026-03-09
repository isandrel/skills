# Excalidraw Design System

## Typography Scale

| Level   | Size    | Weight    | Use Case                      |
| ------- | ------- | --------- | ----------------------------- |
| H1      | 28px    | Bold      | Diagram title, main concept   |
| H2      | 22px    | Semi-bold | Section headers, major nodes  |
| H3      | 18px    | Medium    | Sub-sections, secondary nodes |
| Body    | 14-16px | Regular   | Descriptions, annotations     |
| Caption | 12px    | Light     | Labels, footnotes             |

**Font**: Always use `fontFamily: 5` (Excalifont) for consistent hand-drawn aesthetic.

## Color System

### Semantic Colors

| Purpose     | Primary   | Background   | Hex Primary | Hex BG    |
| ----------- | --------- | ------------ | ----------- | --------- |
| Information | Deep Blue | Light Blue   | `#1e40af`   | `#dbeafe` |
| Success     | Green     | Light Green  | `#10b981`   | `#d1fae5` |
| Warning     | Amber     | Light Amber  | `#f59e0b`   | `#fef3c7` |
| Error       | Red       | Light Red    | `#ef4444`   | `#fee2e2` |
| Neutral     | Gray      | Light Gray   | `#374151`   | `#f3f4f6` |
| Accent      | Purple    | Light Purple | `#8b5cf6`   | `#ede9fe` |

### Color Usage Guidelines

- **Title/Headers**: Deep Blue (`#1e40af`)
- **Connections/Arrows**: Medium Blue (`#3b82f6`) or Gray (`#374151`)
- **Body Text**: Dark Gray (`#374151`)
- **Highlights**: Amber (`#f59e0b`)
- **Backgrounds**: Use light variants at 10-20% opacity

## Layout Grid

| Property       | Value         | Purpose                      |
| -------------- | ------------- | ---------------------------- |
| Canvas         | 1200 × 900 px | Default working area         |
| Vertical gap   | 60-80px       | Between flow elements        |
| Horizontal gap | 40-60px       | Between parallel branches    |
| Arrow gap      | 5px           | Distance from element edge   |
| Title margin   | 40px          | Below title to first element |

## Element Dimensions

| Element   | Width     | Height  | Roundness          |
| --------- | --------- | ------- | ------------------ |
| Title     | auto      | 36px    | n/a (text)         |
| Start/End | 160-200px | 50px    | `type: 3` (full)   |
| Process   | 240-300px | 60px    | `type: 3` (slight) |
| Decision  | 180px     | 120px   | n/a (diamond)      |
| Error box | 200-280px | 60-80px | `type: 3` (full)   |

## Positioning Rules

1. **Title**: Centered horizontally, top of canvas (y: 20-40)
2. **Start node**: Centered below title
3. **Main flow**: Vertical center alignment (x: ~500-600)
4. **Decisions**: Centered on main flow
5. **Error states**: Branch **left** from decisions (x: 80-200)
6. **Sub-processes**: Branch **right** from decisions
7. **Arrows**: Exit from bottom, enter from top (for vertical flow)

## Visual Hierarchy

1. **Size**: Larger = more important
2. **Color**: Saturated = draws attention
3. **Position**: Center/top = primary focus
4. **Stroke**: Thicker = emphasis (strokeWidth: 2)
5. **Fill**: Solid bg = contained concept

## Flowchart Element Types & Colors

| Element         | Shape        | Stroke    | Background | Use                        |
| --------------- | ------------ | --------- | ---------- | -------------------------- |
| **Title**       | Text only    | `#1e40af` | none       | Diagram heading            |
| **Start/End**   | Rounded rect | `#10b981` | `#d1fae5`  | Entry/exit points          |
| **Process**     | Rectangle    | `#3b82f6` | `#dbeafe`  | Actions, steps             |
| **Decision**    | Diamond      | `#f59e0b` | `#fef3c7`  | Yes/No branches            |
| **Error/Alt**   | Rounded rect | `#ef4444` | `#fee2e2`  | Failure/alternative states |
| **Sub-process** | Rectangle    | `#8b5cf6` | `#ede9fe`  | External/optional actions  |
