# Filter Reference

Complete reference for filter syntax in Obsidian Bases.

## Filter Operators

| Operator | Description           | Example                                |
| -------- | --------------------- | -------------------------------------- |
| `==`     | equals                | `'status == "done"'`                   |
| `!=`     | not equal             | `'status != "archived"'`               |
| `>`      | greater than          | `'priority > 3'`                       |
| `<`      | less than             | `'pages < 100'`                        |
| `>=`     | greater than or equal | `'rating >= 4'`                        |
| `<=`     | less than or equal    | `'difficulty <= 5'`                    |
| `&&`     | logical and           | `'status == "active" && priority > 2'` |
| `\|\|`   | logical or            | `'type == "bug" \|\| type == "issue"'` |
| `!`      | logical not           | `'!archived'`                          |

## File Functions

### `file.hasTag(tag)`

Check if file has a specific tag.

```yaml
filters: file.hasTag("project")

# Multiple tags
filters:
  and:
    - file.hasTag("project")
    - file.hasTag("active")
```

### `file.hasLink(link)`

Check if file contains a link to another file.

```yaml
filters: file.hasLink("Project Template")

# Check for any of multiple links
filters:
  or:
    - file.hasLink("Template A")
    - file.hasLink("Template B")
```

### `file.inFolder(folder)`

Check if file is in a specific folder.

```yaml
filters: file.inFolder("Projects")

# Nested folder
filters: file.inFolder("Work/Projects")
```

### `/.../matches(value)`

Use regular expressions for pattern matching.

```yaml
# Files with date in name (YYYY-MM-DD)
filters: '/^\d{4}-\d{2}-\d{2}/.matches(file.basename)'

# Files ending with number
filters: '/\d+$/.matches(file.basename)'
```

## Filter Structures

### Single Filter

Simplest form - a single condition as a string:

```yaml
filters: 'status == "active"'
```

### AND Filter

All conditions must be true:

```yaml
filters:
  and:
    - file.hasTag("task")
    - 'status != "done"'
    - 'priority >= 2'
```

### OR Filter

At least one condition must be true:

```yaml
filters:
  or:
    - file.hasTag("urgent")
    - 'priority == 1'
    - 'due < today()'
```

### NOT Filter

Exclude items matching conditions:

```yaml
filters:
  not:
    - file.hasTag("archived")
    - file.hasTag("deleted")
```

### Nested Filters

Combine filter types for complex logic:

```yaml
filters:
  and:
    - file.hasTag("task")
    - or:
        - 'status == "in-progress"'
        - 'status == "review"'
    - not:
        - file.hasTag("blocked")
```

## Common Filter Patterns

### Active Items Only

```yaml
filters:
  and:
    - 'status != "done"'
    - 'status != "archived"'
```

### Recent Files

```yaml
filters: 'file.mtime >= date("2024-01-01")'
```

### Date Range

```yaml
filters:
  and:
    - 'created >= date("2024-01-01")'
    - 'created <= date("2024-12-31")'
```

### Specific File Types

```yaml
filters: 'file.ext == "md"'
```

### Exclude Folders

```yaml
filters:
  not:
    - file.inFolder("Archive")
    - file.inFolder("Templates")
```

### Complex Tag Logic

```yaml
# Has any project tag AND not archived
filters:
  and:
    - or:
        - file.hasTag("project/active")
        - file.hasTag("project/planning")
    - not:
        - file.hasTag("archived")
```

### Property Existence Check

```yaml
# Has the property (not empty/null)
filters: 'due'

# Does not have the property
filters: '!due'
```

### Value in Range

```yaml
filters:
  and:
    - 'priority >= 1'
    - 'priority <= 5'
```

## Combining Global and View Filters

Global filters apply to ALL views, view filters are additional:

```yaml
# Global: only markdown files in Projects folder
filters:
  and:
    - file.inFolder("Projects")
    - 'file.ext == "md"'

views:
  - type: table
    name: "Active"
    # View filter: additionally filter for active status
    filters: 'status == "active"'
  
  - type: table
    name: "Completed"
    # View filter: additionally filter for done status
    filters: 'status == "done"'
```

Both views will only show markdown files from Projects folder, but each with different status.
