# View Types Reference

Complete reference for all view types in Obsidian Bases.

## Table View

The most versatile view type for displaying data in rows and columns.

### Basic Table

```yaml
views:
  - type: table
    name: "All Items"
    order:
      - file.name
      - status
      - priority
```

### Table with Grouping

Group rows by a property value:

```yaml
views:
  - type: table
    name: "Grouped by Status"
    order:
      - file.name
      - priority
      - due
    groupBy:
      property: status
      direction: ASC  # or DESC
```

### Table with Sorting

Sort results by specific criteria:

```yaml
views:
  - type: table
    name: "Sorted Tasks"
    order:
      - file.name
      - due
      - priority
    sort:
      - property: due
        direction: ASC
      - property: priority
        direction: DESC
```

### Table with Limit

Limit number of results:

```yaml
views:
  - type: table
    name: "Top 10"
    order:
      - file.name
      - score
    sort:
      - property: score
        direction: DESC
    limit: 10
```

### Table with Column Sizes

Set custom column widths:

```yaml
views:
  - type: table
    name: "Custom Columns"
    order:
      - file.name
      - description
      - status
    columnSize:
      file.name: 200
      description: 400
      status: 100
```

### Table with Summaries

Show aggregate data:

```yaml
views:
  - type: table
    name: "With Totals"
    order:
      - file.name
      - hours
      - cost
    summaries:
      hours: Sum
      cost: Average
```

## Cards View

Visual card layout, ideal for image-based content.

### Basic Cards

```yaml
views:
  - type: cards
    name: "Gallery"
    order:
      - cover          # Image property (shown at top)
      - file.name
      - author
      - rating
```

### Cards with Filters

```yaml
views:
  - type: cards
    name: "Five Stars"
    filters: 'rating >= 4.5'
    order:
      - cover
      - file.name
      - author
```

### Cards Best Practices

- First property should be an image for visual impact
- Keep property list short (3-5 items)
- Use formula properties for status icons

```yaml
formulas:
  status_icon: 'if(status == "done", "✅", "⏳")'

views:
  - type: cards
    order:
      - cover
      - formula.status_icon
      - file.name
      - summary
```

## List View

Simple list format for quick scanning.

### Basic List

```yaml
views:
  - type: list
    name: "Quick List"
    order:
      - file.name
      - status
```

### List with Sorting

```yaml
views:
  - type: list
    name: "Priority List"
    order:
      - file.name
      - priority
    sort:
      - property: priority
        direction: DESC
```

### List Best Practices

- Keep to 2-3 properties max
- First property should be most important
- Great for simple overviews

## Map View

Geographic visualization requiring location data.

### Basic Map

```yaml
views:
  - type: map
    name: "Locations"
    order:
      - file.name
      - location
      - address
```

### Map Requirements

Files must have location data in frontmatter:

```yaml
---
location: [51.5074, -0.1278]  # [latitude, longitude]
address: "London, UK"
---
```

### Map with Filters

```yaml
views:
  - type: map
    name: "Visited Places"
    filters: 'visited == true'
    order:
      - file.name
      - location
      - visit_date
```

## View Combinations

### Multiple Views in One Base

```yaml
views:
  # Overview table
  - type: table
    name: "All Tasks"
    order:
      - file.name
      - status
      - due
  
  # Active only
  - type: list
    name: "Active"
    filters: 'status != "done"'
    order:
      - file.name
      - priority
  
  # Visual cards
  - type: cards
    name: "Gallery"
    filters: 'cover'
    order:
      - cover
      - file.name
```

### View-Specific Filters

Global filters + view-specific filters combine with AND logic:

```yaml
# Global: only markdown in Projects
filters:
  and:
    - file.inFolder("Projects")
    - 'file.ext == "md"'

views:
  - type: table
    name: "Active"
    filters: 'status == "active"'  # Additional filter
    order:
      - file.name
  
  - type: table
    name: "Done"
    filters: 'status == "done"'    # Additional filter
    order:
      - file.name
```

## Advanced Patterns

### Dynamic Groups with Formulas

```yaml
formulas:
  priority_group: 'if(priority >= 4, "High", if(priority >= 2, "Medium", "Low"))'

views:
  - type: table
    name: "By Priority Group"
    groupBy:
      property: formula.priority_group
      direction: DESC
    order:
      - file.name
      - priority
```

### Conditional Sorting

```yaml
formulas:
  sort_key: 'if(status == "done", 999, priority)'

views:
  - type: table
    name: "Smart Sort"
    sort:
      - property: formula.sort_key
        direction: ASC
    order:
      - file.name
      - status
      - priority
```

### Paginated Results

```yaml
views:
  - type: table
    name: "Page 1"
    limit: 20
    sort:
      - property: created
        direction: DESC
    order:
      - file.name
      - created
```
