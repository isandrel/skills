# Excalidraw JSON Reference

## Root Document

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

## Element Index System

Use alphabetical indexing for layer ordering:

- `a0`, `a1`, `a2` ... for first layer
- `b0`, `b1`, `b2` ... for second layer
- Arrows typically on higher layer than shapes

## Element ID Conventions

Use semantic, readable IDs:

- `title-main`, `node-auth`, `arrow-1-to-2`
- Avoid: `abcd1234`, `elem1`, `x`

## Binding Patterns

### Text Inside Container

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

### Arrow Connecting Shapes

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
