# Excalidraw JSON Schema Reference

Complete reference for Excalidraw element types and properties.

## Color Palette

### Primary Colors

| Purpose   | Color       | Hex       |
| --------- | ----------- | --------- |
| Title     | Deep Blue   | `#1e40af` |
| Subtitle  | Medium Blue | `#3b82f6` |
| Body Text | Dark Gray   | `#374151` |
| Emphasis  | Amber       | `#f59e0b` |
| Success   | Green       | `#10b981` |
| Warning   | Red         | `#ef4444` |

### Background Colors

| Purpose      | Color        | Hex       |
| ------------ | ------------ | --------- |
| Light Blue   | Primary BG   | `#dbeafe` |
| Light Gray   | Neutral BG   | `#f3f4f6` |
| Light Amber  | Highlight BG | `#fef3c7` |
| Light Green  | Success BG   | `#d1fae5` |
| Light Purple | Accent BG    | `#ede9fe` |

## Element Types

### Rectangle

```json
{
  "type": "rectangle",
  "id": "rect-1",
  "x": 100,
  "y": 100,
  "width": 200,
  "height": 80,
  "strokeColor": "#1e40af",
  "backgroundColor": "#dbeafe",
  "fillStyle": "solid",
  "strokeWidth": 2,
  "roughness": 1,
  "opacity": 100,
  "roundness": { "type": 3 }
}
```

### Text

```json
{
  "type": "text",
  "id": "text-1",
  "x": 150,
  "y": 130,
  "text": "Content here",
  "fontSize": 20,
  "fontFamily": 5,
  "textAlign": "center",
  "verticalAlign": "middle",
  "strokeColor": "#1e40af",
  "backgroundColor": "transparent"
}
```

### Arrow

```json
{
  "type": "arrow",
  "id": "arrow-1",
  "x": 300,
  "y": 140,
  "width": 100,
  "height": 0,
  "points": [[0, 0], [100, 0]],
  "strokeColor": "#374151",
  "strokeWidth": 2,
  "startArrowhead": null,
  "endArrowhead": "arrow"
}
```

### Ellipse

```json
{
  "type": "ellipse",
  "id": "ellipse-1",
  "x": 100,
  "y": 100,
  "width": 120,
  "height": 120,
  "strokeColor": "#10b981",
  "backgroundColor": "#d1fae5",
  "fillStyle": "solid"
}
```

### Diamond

```json
{
  "type": "diamond",
  "id": "diamond-1",
  "x": 100,
  "y": 100,
  "width": 150,
  "height": 100,
  "strokeColor": "#f59e0b",
  "backgroundColor": "#fef3c7",
  "fillStyle": "solid"
}
```

### Line

```json
{
  "type": "line",
  "id": "line-1",
  "x": 100,
  "y": 100,
  "points": [[0, 0], [200, 100]],
  "strokeColor": "#374151",
  "strokeWidth": 2
}
```

## Root JSON Structure

```json
{
  "type": "excalidraw",
  "version": 2,
  "source": "https://excalidraw.com",
  "elements": [],
  "appState": {
    "gridSize": null,
    "viewBackgroundColor": "#ffffff"
  },
  "files": {}
}
```

## Font Family Values

| Value | Font Name  | Notes            |
| ----- | ---------- | ---------------- |
| 1     | Virgil     | Hand-drawn style |
| 2     | Helvetica  | Sans-serif       |
| 3     | Cascadia   | Monospace        |
| 4     | Assistant  | Clean sans       |
| 5     | Excalifont | **Recommended**  |

## Fill Styles

| Style         | Description           |
| ------------- | --------------------- |
| `solid`       | Solid fill color      |
| `hachure`     | Hatched lines         |
| `cross-hatch` | Cross-hatched pattern |
| `dots`        | Dotted pattern        |

## Roundness Types

| Type            | Description                 |
| --------------- | --------------------------- |
| `{ "type": 1 }` | Sharp corners               |
| `{ "type": 2 }` | Slight rounding             |
| `{ "type": 3 }` | Full rounding (recommended) |

## Arrowhead Types

| Value        | Description     |
| ------------ | --------------- |
| `null`       | No arrowhead    |
| `"arrow"`    | Standard arrow  |
| `"bar"`      | Bar/line end    |
| `"dot"`      | Circle end      |
| `"triangle"` | Filled triangle |

## Element Binding

### Bind Text to Container

Container element:
```json
{
  "type": "rectangle",
  "id": "container-1",
  "boundElements": [{ "id": "text-1", "type": "text" }]
}
```

Text element:
```json
{
  "type": "text",
  "id": "text-1",
  "containerId": "container-1"
}
```

### Bind Arrow to Shapes

```json
{
  "type": "arrow",
  "startBinding": {
    "elementId": "source-shape-id",
    "focus": 0,
    "gap": 5
  },
  "endBinding": {
    "elementId": "target-shape-id",
    "focus": 0,
    "gap": 5
  }
}
```

## Required Fields for All Elements

| Field             | Type        | Description                 |
| ----------------- | ----------- | --------------------------- |
| `id`              | string      | Unique identifier           |
| `type`            | string      | Element type                |
| `x`, `y`          | number      | Position coordinates        |
| `width`, `height` | number      | Dimensions                  |
| `angle`           | number      | Rotation in radians         |
| `strokeColor`     | string      | Border color (hex)          |
| `backgroundColor` | string      | Fill color or "transparent" |
| `fillStyle`       | string      | Fill pattern                |
| `strokeWidth`     | number      | Border thickness            |
| `strokeStyle`     | string      | "solid" or "dashed"         |
| `roughness`       | number      | Hand-drawn effect (0-2)     |
| `opacity`         | number      | 0-100                       |
| `groupIds`        | array       | Group memberships           |
| `frameId`         | string/null | Frame container             |
| `index`           | string      | Layer order (a1, a2, etc.)  |
| `roundness`       | object      | Corner rounding             |
| `seed`            | number      | Random seed for roughness   |
| `version`         | number      | Edit version                |
| `versionNonce`    | number      | Version uniqueness          |
| `isDeleted`       | boolean     | Deletion flag               |
| `boundElements`   | array       | Connected elements          |
| `updated`         | number      | Timestamp                   |
| `link`            | string/null | External link               |
| `locked`          | boolean     | Edit lock                   |
