# Property Reference

Complete reference for properties in Obsidian Bases.

## Three Types of Properties

### 1. File Properties

Built-in properties available on all files.

### 2. Custom Properties

User-defined properties from YAML frontmatter in notes.

### 3. Formula Properties

Calculated properties defined in the base file.

## File Properties

### Basic Metadata

| Property        | Type   | Description                  |
| --------------- | ------ | ---------------------------- |
| `file.name`     | string | Full filename with extension |
| `file.basename` | string | Filename without extension   |
| `file.path`     | string | Full file path               |
| `file.folder`   | string | Parent folder path           |
| `file.ext`      | string | File extension (e.g., "md")  |

### Timestamps

| Property     | Type | Description            |
| ------------ | ---- | ---------------------- |
| `file.ctime` | date | Creation time          |
| `file.mtime` | date | Last modification time |

### Size

| Property    | Type   | Description        |
| ----------- | ------ | ------------------ |
| `file.size` | number | File size in bytes |

### Links and References

| Property        | Type  | Description                |
| --------------- | ----- | -------------------------- |
| `file.links`    | array | All links in the file      |
| `file.outlinks` | array | Outgoing links             |
| `file.inlinks`  | array | Incoming links (backlinks) |
| `file.tags`     | array | All tags in the file       |

### File Functions

| Function                | Returns | Description                    |
| ----------------------- | ------- | ------------------------------ |
| `file.hasTag(tag)`      | boolean | Check if file has tag          |
| `file.hasLink(link)`    | boolean | Check if file links to another |
| `file.inFolder(folder)` | boolean | Check if file is in folder     |

## Custom Properties

Properties defined in YAML frontmatter of notes.

### Example Note

```markdown
---
title: Project Alpha
status: in-progress
priority: 1
due: 2024-12-31
tags:
  - project
  - important
author: John Doe
completed: false
---

# Project Alpha

Content here...
```

### Using Custom Properties

Reference directly by name in filters and views:

```yaml
# In filters
filters: 'status == "in-progress"'

# In views
views:
  - type: table
    name: "Projects"
    order:
      - file.name
      - title
      - status
      - priority
      - due
      - author
```

### Property Type Inference

Obsidian automatically infers types:

- `status: in-progress` → string
- `priority: 1` → number
- `due: 2024-12-31` → date
- `completed: false` → boolean
- `tags: [project, important]` → array

## Formula Properties

Calculated properties defined in base files.

### Defining Formulas

```yaml
formulas:
  days_remaining: '((date(due) - today()) / 86400000).round(0)'
  is_overdue: 'date(due) < today()'
  full_title: 'title + " (" + status + ")"'
```

### Using Formula Properties

Reference with `formula.` prefix:

```yaml
views:
  - type: table
    name: "Tasks"
    order:
      - file.name
      - formula.days_remaining
      - formula.is_overdue
      - formula.full_title
```

## Property Configuration

### Display Names

Customize how properties appear in views:

```yaml
properties:
  # Custom property
  status:
    displayName: "Task Status"
  
  # Formula property
  formula.days_remaining:
    displayName: "Days Left"
  
  # File property
  file.mtime:
    displayName: "Last Modified"
  
  # Empty display name (hide label)
  formula.status_icon:
    displayName: ""
```

### Configuration Structure

```yaml
properties:
  property_name:
    displayName: "Human Readable Name"
```

Property name can be:
- Custom property: `property_name`
- Formula property: `formula.formula_name`
- File property: `file.property_name`

## The `this` Keyword

Reference the current file's properties within formulas.

### Self-Reference

```yaml
formulas:
  # Reference other properties
  total_cost: 'this.price * this.quantity'
  
  # Conditional on own property
  discount_price: 'if(this.member, this.price * 0.9, this.price)'
  
  # String combination
  display_title: 'this.title + " - " + this.author'
```

### When to Use

Use `this` when a formula needs to access multiple properties of the same file:

```yaml
formulas:
  # Calculate completion percentage
  completion: '((this.completed_tasks / this.total_tasks) * 100).round(0)'
  
  # Check multiple conditions
  is_urgent: 'this.priority > 3 && this.due < today()'
```

## Property Access in Different Contexts

### In Filters

Access properties directly:

```yaml
filters:
  and:
    - 'status == "active"'
    - 'priority > 2'
    - file.hasTag("project")
```

### In Formulas

Access via property name or `this`:

```yaml
formulas:
  # Direct access
  days_old: '((today() - date(created)) / 86400000).round(0)'
  
  # Via this keyword
  score: 'this.points * this.multiplier'
```

### In Views

List properties to display:

```yaml
views:
  - type: table
    order:
      - file.name           # File property
      - status              # Custom property
      - formula.score       # Formula property
```

## Common Property Patterns

### Status Tracking

```yaml
# In note frontmatter
---
status: in-progress
started: 2024-01-15
updated: 2024-01-20
---

# In base file
properties:
  status:
    displayName: "Status"

formulas:
  days_active: '((date(updated) - date(started)) / 86400000).round(0)'
```

### Rating System

```yaml
# In note frontmatter
---
rating: 4.5
max_rating: 5
---

# In base file
formulas:
  rating_percent: '((rating / max_rating) * 100).round(0).toString() + "%"'
  star_display: 'rating.toString() + " / " + max_rating.toString()'
```

### Multi-Property Calculations

```yaml
# In note frontmatter
---
hours_estimated: 10
hours_actual: 12
hourly_rate: 50
---

# In base file
formulas:
  estimated_cost: 'hours_estimated * hourly_rate'
  actual_cost: 'hours_actual * hourly_rate'
  over_budget: 'actual_cost - estimated_cost'
  variance_percent: '((over_budget / estimated_cost) * 100).round(1).toString() + "%"'
```

### Metadata Enrichment

```yaml
# In note frontmatter
---
pages: 250
---

# In base file
formulas:
  reading_time_min: 'pages * 2'
  reading_time_hours: '(pages * 2 / 60).round(1)'
  page_category: 'if(pages < 100, "Short", if(pages < 300, "Medium", "Long"))'
```

## Property Best Practices

### 1. Consistent Naming

Use consistent naming across notes:
- `snake_case` or `camelCase`
- Descriptive names: `completion_date` not `cd`

### 2. Type Consistency

Keep property types consistent:
- `priority` always a number (1-5)
- `status` always a string ("todo", "done", etc.)
- `due` always a date (YYYY-MM-DD)

### 3. Required vs Optional

Use formulas to handle missing properties:

```yaml
formulas:
  safe_value: 'if(optional_property, optional_property, "N/A")'
  with_default: 'default(rating, 0)'
```

### 4. Property Grouping

Group related properties:

```yaml
# Time tracking
---
started: 2024-01-01
completed: 2024-01-15
estimated_hours: 10
actual_hours: 12
---

# Financial
---
budget: 5000
spent: 4200
currency: USD
---
```
