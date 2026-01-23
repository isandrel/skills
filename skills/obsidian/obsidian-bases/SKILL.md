---
name: obsidian-bases
description: "Comprehensive guide for creating and editing Obsidian Bases (.base files) - YAML-based database views for notes. Use when: (1) Creating task trackers, reading lists, or project dashboards, (2) Building table, card, list, or map views, (3) Filtering/sorting notes by properties or tags, (4) Working with formulas and calculated fields, (5) Any database-like organization of notes in Obsidian."
---

# Obsidian Bases

Create and edit valid Obsidian Bases (`.base` files) - YAML-based database views for notes in your vault.

## File Format

Bases use `.base` extension and contain YAML. They can also be embedded in Markdown code blocks.

## Validation Script

Use `scripts/validate.py` to validate base files:

```bash
# Install dependency (first time only)
pip install pyyaml

# Validate a base file
python scripts/validate.py mybase.base
```

The script validates:
- YAML syntax
- Required fields (views, view type, view name)
- Valid view types (table, cards, list, map)
- Filter structure
- Formula syntax
- Property configuration

## Base File Templates

### Minimal Template

```yaml
views:
  - type: table
    name: "All Notes"
    order:
      - file.name
```

### Standard Template

```yaml
filters:
  and:
    - file.hasTag("your-tag")
    - 'file.ext == "md"'

formulas:
  last_modified: 'file.mtime.relative()'

properties:
  formula.last_modified:
    displayName: "Last Modified"

views:
  - type: table
    name: "Main View"
    order:
      - file.name
      - formula.last_modified
```

Copy a template above or from `assets/template/` directory to start creating your own base file.

## CLI Query Tool

For running queries and processing base files, use **[obaq](https://github.com/knu/obaq)** - a CLI query processor for Obsidian Bases:

```bash
# Install
npm install -g obaq

# Run query from .base file
obaq -d /path/to/vault -e @file.base

# Output as CSV or Markdown
obaq -d /path/to/vault -e @file.base -f csv
obaq -d /path/to/vault -e @file.base -f md

# Process markdown with base blocks
obaq -d /path/to/vault file.md
```

`obaq` supports:
- Running .base files from command line
- Multiple output formats (JSON, CSV, Markdown)
- Processing markdown files with base code blocks
- All base features (filters, formulas, views)

## Complete Schema

```yaml
# Global filters apply to ALL views
filters:
  # Single filter string OR recursive filter object
  and: []
  or: []
  not: []

# Define formula properties usable across all views
formulas:
  formula_name: 'expression'

# Configure display names for properties
properties:
  property_name:
    displayName: "Display Name"
  formula.formula_name:
    displayName: "Formula Display Name"
  file.ext:
    displayName: "Extension"

# Define custom summary formulas
summaries:
  custom_summary_name: 'values.mean().round(3)'

# Define one or more views
views:
  - type: table | cards | list | map
    name: "View Name"
    limit: 10                    # Optional: limit results
    groupBy:                     # Optional: group results
      property: property_name
      direction: ASC | DESC
    filters:                     # View-specific filters
      and: []
    order:                       # Properties to display in order
      - file.name
      - property_name
      - formula.formula_name
    summaries:                   # Map properties to summary formulas
      property_name: Average
```

## Filter Syntax

### Single Filter

```yaml
filters: 'status == "done"'
```

### AND - All conditions must be true

```yaml
filters:
  and:
    - 'status == "done"'
    - 'priority > 3'
```

### OR - Any condition can be true

```yaml
filters:
  or:
    - file.hasTag("book")
    - file.hasTag("article")
```

### NOT - Exclude matching items

```yaml
filters:
  not:
    - file.hasTag("archived")
```

### Nested Filters

```yaml
filters:
  or:
    - file.hasTag("tag")
    - and:
        - file.hasTag("book")
        - file.hasLink("Textbook")
    - not:
        - file.hasTag("book")
        - file.inFolder("Required Reading")
```

### Filter Operators

| Operator | Description           |
| -------- | --------------------- |
| `==`     | equals                |
| `!=`     | not equal             |
| `>`      | greater than          |
| `<`      | less than             |
| `>=`     | greater than or equal |
| `<=`     | less than or equal    |
| `&&`     | logical and           |
| `\|\|`   | logical or            |
| `!`      | logical not           |

## Properties

Three types of properties:

1. **File Properties** - Built-in properties like `file.name`, `file.path`, `file.mtime`, `file.size`, `file.ext`
2. **Custom Properties** - From YAML frontmatter in notes
3. **Formula Properties** - Calculated using formulas, referenced as `formula.name`

Configure display names:

```yaml
properties:
  status:
    displayName: "Task Status"
  formula.days_remaining:
    displayName: "Days Left"
```

The `this` keyword references the current file's properties in formulas.

## Formula Syntax

Write formulas as single-quoted strings:

```yaml
formulas:
  days_until_due: 'if(due, ((date(due) - today()) / 86400000).round(0), "")'
  is_overdue: 'if(due, date(due) < today() && status != "done", false)'
  priority_label: 'if(priority == 1, "High", if(priority == 2, "Medium", "Low"))'
```

### Common Functions

- **Conditionals**: `if(condition, true_value, false_value)`
- **Date**: `today()`, `date(value)`, `date(value).year`, `date(value).format("format")`
- **Date Arithmetic**: Subtract dates for milliseconds difference
- **String**: `toString()`, `format()`, `contains()`
- **Number**: `round(decimals)`, `min()`, `max()`
- **List**: `length`, `filter()`, `map()`
- **File**: `file.hasTag(tag)`, `file.hasLink(link)`, `file.inFolder(folder)`, `file.links`, `file.tags`
- **Type Checking**: `isType("number")`, `isType("string")`

For complete function reference, see [references/formulas.md](references/formulas.md).

## View Types

### Table View

```yaml
views:
  - type: table
    name: "Tasks"
    order:
      - file.name
      - status
      - due
    groupBy:
      property: status
      direction: ASC
    summaries:
      formula.days_until_due: Average
```

### Cards View

Visual card layout, first property is typically an image:

```yaml
views:
  - type: cards
    name: "Library"
    order:
      - cover           # Image at top
      - file.name
      - author
      - status
```

### List View

Simple list format:

```yaml
views:
  - type: list
    name: "Quick List"
    order:
      - file.name
      - status
```

### Map View

Geographic visualization (requires location data):

```yaml
views:
  - type: map
    name: "Locations"
    order:
      - file.name
      - location
```

## Default Summary Formulas

Use these in `summaries` section:

- `Average` - Mean of numeric values
- `Sum` - Total of numeric values
- `Min` - Minimum value
- `Max` - Maximum value
- `Count` - Number of items

Custom summaries:

```yaml
summaries:
  avgLinks: 'values.filter(value.isType("number")).mean().round(1)'
```

## Common Patterns

### Filter by Tag

```yaml
filters: file.hasTag("project")
```

### Filter by Folder

```yaml
filters: file.inFolder("Projects")
```

### Filter by Date Range

```yaml
filters:
  and:
    - 'file.mtime >= date("2024-01-01")'
    - 'file.mtime <= date("2024-12-31")'
```

### Filter by Property Value

```yaml
filters: 'status == "in-progress"'
```

### Combine Multiple Conditions

```yaml
filters:
  and:
    - file.hasTag("task")
    - 'status != "done"'
    - 'priority >= 2'
```

## Embedding Bases

Embed in Markdown files:

```markdown
![[MyBase.base]]

<!-- Specific view -->
![[MyBase.base#View Name]]
```

## YAML Quoting Rules

- Use single quotes for formulas containing double quotes: `'if(done, "Yes", "No")'`
- Use double quotes for simple strings: `"My View Name"`
- Escape nested quotes properly in complex expressions

## Examples

See complete working examples in the `assets/template/` directory:

- **[task-tracker.base](assets/template/task-tracker.base)** - Task management with formulas and grouping
- **[reading-list.base](assets/template/reading-list.base)** - Reading list with card and table views
- **[project-notes.base](assets/template/project-notes.base)** - Project tracking with link counting
- **[daily-notes.base](assets/template/daily-notes.base)** - Daily notes index with regex filtering

## References

For detailed documentation:

- **[references/filters.md](references/filters.md)** - Complete filter syntax and file functions
- **[references/formulas.md](references/formulas.md)** - All formula functions with examples
- **[references/properties.md](references/properties.md)** - Property types and configuration
- **[references/view-types.md](references/view-types.md)** - All view types with advanced patterns
