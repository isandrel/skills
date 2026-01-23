# Formula Reference

Complete reference for formulas in Obsidian Bases.

## Formula Syntax

Formulas are written as single-quoted strings:

```yaml
formulas:
  formula_name: 'expression'
```

Referenced in views as `formula.formula_name`.

## Global Functions

### `if(condition, true_value, false_value)`

Conditional logic:

```yaml
formulas:
  status_label: 'if(status == "done", "✅ Complete", "⏳ Pending")'
  overdue: 'if(due < today(), "Yes", "No")'
  nested: 'if(priority == 1, "High", if(priority == 2, "Medium", "Low"))'
```

### `contains(haystack, needle)`

Check if string contains substring:

```yaml
formulas:
  is_urgent: 'if(contains(file.name, "URGENT"), "🚨", "")'
```

### `default(value, fallback)`

Provide fallback for null/undefined:

```yaml
formulas:
  safe_status: 'default(status, "not set")'
```

## Date Functions

### `today()`

Current date:

```yaml
formulas:
  is_today: 'if(date(created) == today(), "Today", "")'
```

### `date(value)`

Convert to date object:

```yaml
formulas:
  parsed_date: 'date(due)'
  from_string: 'date("2024-01-15")'
```

### Date Fields

Access date components:

```yaml
formulas:
  year: 'date(created).year'
  month: 'date(created).month'
  day: 'date(created).day'
  hour: 'date(created).hour'
  minute: 'date(created).minute'
```

### `format(format_string)`

Format date display:

```yaml
formulas:
  formatted: 'date(created).format("YYYY-MM-DD")'
  long_format: 'date(created).format("MMMM D, YYYY")'
  day_name: 'date(created).format("dddd")'
  time: 'date(created).format("HH:mm")'
```

Common format tokens:
- `YYYY` - 4-digit year
- `MM` - 2-digit month
- `DD` - 2-digit day
- `dddd` - Day name (Monday, Tuesday, etc.)
- `MMMM` - Month name (January, February, etc.)
- `HH:mm` - 24-hour time

### `relative()`

Relative time description:

```yaml
formulas:
  last_modified: 'file.mtime.relative()'
  # Returns: "2 days ago", "3 hours ago", etc.
```

## Date Arithmetic

Subtract dates to get milliseconds difference:

```yaml
formulas:
  # Days until due
  days_until: '((date(due) - today()) / 86400000).round(0)'
  
  # Hours since created
  hours_since: '((today() - date(created)) / 3600000).round(1)'
  
  # Age in days
  age_days: '((today() - date(file.ctime)) / 86400000).round(0)'
```

Constants:
- 1 day = 86400000 milliseconds
- 1 hour = 3600000 milliseconds
- 1 minute = 60000 milliseconds

## String Functions

### `toString()`

Convert to string:

```yaml
formulas:
  page_count: 'pages.toString() + " pages"'
  year_str: 'date(created).year.toString()'
```

### String Concatenation

Use `+` operator:

```yaml
formulas:
  full_name: 'first_name + " " + last_name'
  reading_time: '(pages * 2).toString() + " min"'
```

## Number Functions

### `round(decimals)`

Round to decimal places:

```yaml
formulas:
  rounded: 'price.round(2)'  # 2 decimal places
  whole_number: 'average.round(0)'  # No decimals
```

### `min()` and `max()`

Find minimum or maximum:

```yaml
formulas:
  lowest: 'min(score1, score2, score3)'
  highest: 'max(rating_a, rating_b)'
```

### Math Operations

Standard operators: `+`, `-`, `*`, `/`, `%`

```yaml
formulas:
  total: 'price * quantity'
  average: '(a + b + c) / 3'
  percentage: '(completed / total) * 100'
  remainder: 'value % 10'
```

## List Functions

### `.length`

Get list length:

```yaml
formulas:
  tag_count: 'file.tags.length'
  link_count: 'file.links.length'
```

### `filter(predicate)`

Filter list items:

```yaml
formulas:
  numeric_values: 'list.filter(value.isType("number"))'
  high_scores: 'scores.filter(score > 80)'
```

### `map(transform)`

Transform list items:

```yaml
formulas:
  doubled: 'numbers.map(n * 2)'
  formatted: 'dates.map(date.format("YYYY-MM-DD"))'
```

### `join(separator)`

Join list into string:

```yaml
formulas:
  tag_list: 'file.tags.join(", ")'
  combined: 'items.join(" | ")'
```

## File Functions

### Built-in File Properties

```yaml
formulas:
  # File metadata
  name: 'file.name'
  basename: 'file.basename'
  path: 'file.path'
  ext: 'file.ext'
  
  # Timestamps
  created: 'file.ctime'
  modified: 'file.mtime'
  
  # Size
  file_size: 'file.size'
  
  # Links and tags
  all_links: 'file.links'
  all_tags: 'file.tags'
  outlinks: 'file.outlinks'
  inlinks: 'file.inlinks'
```

### File Functions in Formulas

Access file functions:

```yaml
formulas:
  has_project_tag: 'file.hasTag("project")'
  has_template_link: 'file.hasLink("Template")'
  in_work_folder: 'file.inFolder("Work")'
```

## Type Checking

### `isType(type_name)`

Check value type:

```yaml
formulas:
  is_number: 'value.isType("number")'
  is_string: 'value.isType("string")'
  is_date: 'value.isType("date")'
  is_list: 'value.isType("array")'
```

## Summary Formulas

Special formulas for aggregating values across multiple files:

```yaml
summaries:
  # Use built-in summaries
  total: 'values.sum()'
  average: 'values.mean()'
  minimum: 'values.min()'
  maximum: 'values.max()'
  count: 'values.length'
  
  # Custom summary with filtering
  avg_numeric: 'values.filter(value.isType("number")).mean().round(1)'
  total_pages: 'values.filter(v => v).sum()'
```

## The `this` Keyword

Reference current file's properties:

```yaml
formulas:
  self_reference: 'this.property_name'
  calculated: 'this.price * this.quantity'
```

## Complex Examples

### Priority Score

```yaml
formulas:
  priority_score: 'if(urgent, 10, 0) + if(important, 5, 0) + priority'
```

### Status Badge

```yaml
formulas:
  badge: 'if(status == "done", "✅", if(status == "in-progress", "🔄", if(status == "blocked", "🚫", "⏳")))'
```

### Completion Percentage

```yaml
formulas:
  completion: '((completed_tasks / total_tasks) * 100).round(0).toString() + "%"'
```

### Time Categories

```yaml
formulas:
  time_category: 'if(hours < 1, "Quick", if(hours < 4, "Medium", "Long"))'
```

### Deadline Warning

```yaml
formulas:
  deadline_warning: 'if(due, if((date(due) - today()) / 86400000 < 3, "⚠️ Soon", ""), "")'
```

### Word Count Estimate

```yaml
formulas:
  word_count: '(file.size / 5).round(0)'
```

### Age in Natural Language

```yaml
formulas:
  age: 'if(((today() - date(file.ctime)) / 86400000) < 7, "New", if(((today() - date(file.ctime)) / 86400000) < 30, "Recent", "Old"))'
```
