# Obsidian Bases Skill

Comprehensive guide for creating and editing Obsidian Bases (`.base` files) - YAML-based database views for notes.

## What This Skill Provides

- **Complete base file schema** with all syntax elements
- **Modular validation system** with TOML-based configuration
- **4 working examples** covering different use cases
- **4 comprehensive references** (1,291 lines) for filters, formulas, properties, and view types
- **Template files** for quick project starts

## Use Cases

1. Creating task trackers, reading lists, or project dashboards
2. Building table, card, list, or map views of notes
3. Filtering/sorting notes by properties or tags
4. Working with formulas and calculated fields
5. Any database-like organization of notes in Obsidian

## Structure

```
.agent/skills/obsidian-bases/
├── SKILL.md                    # Main documentation (399 lines)
├── README.md                   # This file
├── scripts/                    # Validation tools
│   ├── config.py              # Configuration loader
│   ├── validate.py            # Main validator
│   ├── validate.toml          # Validation rules
│   └── validators/            # Specialized validators
├── assets/template/           # Example base files
│   ├── task-tracker.base
│   ├── reading-list.base
│   ├── project-notes.base
│   └── daily-notes.base
└── references/                # Detailed syntax guides
    ├── filters.md             # Filter syntax (229 lines)
    ├── formulas.md            # Formula functions (359 lines)
    ├── properties.md          # Property types (367 lines)
    └── view-types.md          # View types (336 lines)
```

## Quick Start

### Validate a Base File

```bash
# Install dependencies
pip install pyyaml tomli

# Validate
python scripts/validate.py mybase.base
```

### Create from Template

Start with a minimal or standard template from SKILL.md, or copy from `assets/template/`.

### Customize Validation

Edit `scripts/validate.toml` to adjust validation rules for your needs.

## Key Features

### Modular Validation System

- **config.py**: TOML-based configuration (no hardcoded values)
- **validators/**: Specialized validators for filters, formulas, properties, views
- **Detailed errors**: Context, examples, and fix suggestions
- **Extensible**: Easy to add new validation rules

### Comprehensive Documentation

- **Complete schema**: All base file syntax in one place
- **Progressive disclosure**: Quick reference in SKILL.md, details in references/
- **Working examples**: 4 different use cases fully implemented
- **All syntax covered**: 1,291 lines of reference documentation

## Examples

The `assets/template/` directory contains:

- **task-tracker.base**: Formulas, grouping, summaries
- **reading-list.base**: Card view, tag filtering
- **project-notes.base**: Custom summaries, folder filtering  
- **daily-notes.base**: Regex filtering, date formatting

## References

Detailed syntax guides in `references/`:

- **filters.md**: All filter operators, file functions, patterns
- **formulas.md**: Complete function reference (date, string, number, list)
- **properties.md**: File properties, custom properties, formulas
- **view-types.md**: Table, cards, list, map with advanced patterns

## Requirements

- Python 3.7+
- pyyaml
- tomli (for Python < 3.11)

## License

This skill follows Obsidian Bases documentation and best practices.
