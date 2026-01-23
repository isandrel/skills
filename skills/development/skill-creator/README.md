# Skill Creator

**Create professional Agent Skills with proper structure, validation, and packaging.**

A comprehensive toolkit for building modular, reusable Agent Skills that extend Claude's capabilities with specialized knowledge, workflows, and tool integrations.

> **Based on [Dify's skill-creator](https://github.com/langgenius/dify/tree/main/.agents/skills/skill-creator)** with enhancements including:
> - 🎨 Modern validation with `rich` library for beautiful terminal output
> - 📝 Externalized customizable templates
> - ⚙️ TOML-based configuration system
> - 🔍 Prerequisite validation before script execution
> - 📦 Enhanced packaging with configurable options

---

## � Installing This Skill

### Step 1: Get the Skill

```bash
# Navigate to skill-creator directory
cd ~/path/to/skill-creator

# Or clone from repository
git clone <repo-url> skill-creator
cd skill-creator
```

### Step 2: Install Dependencies

```bash
# One-liner: Install all dependencies
pip install pyyaml rich tomli pydantic typer
```

> **Note:** 
> - `rich` provides beautiful terminal output with colors and emojis
> - `pydantic` enables schema validation for configuration and data
> - `typer` provides modern CLI argument parsing
> - `tomli` only needed for Python 3.10 and below (Python 3.11+ has built-in `tomllib`)

### Step 3: (Optional) Install as Agent Skill

If using with Claude Desktop or similar:

```bash
# Copy or symlink to your skills directory
cp -r /path/to/skill-creator ~/.gemini/skills/

# Or create a symlink
ln -s /path/to/skill-creator ~/.gemini/skills/skill-creator
```

### Step 4: Verify Installation

```bash
# Test that scripts work
python scripts/init_skill.py --help

# Should show usage information
```

**That's it!** You're ready to create skills.

---

## 🚀 Quick Start

Now that you've installed skill-creator, create your first skill:

```bash
# 1. Create a new skill
cd /path/to/skill-creator

# 2. Create a new skill
python scripts/init_skill.py my-awesome-skill --path ~/skills

# 3. Edit the generated SKILL.md and customize resources

# 4. Validate your skill
python scripts/validate.py ~/skills/my-awesome-skill

# 5. Package for distribution
python scripts/package_skill.py ~/skills/my-awesome-skill
```

---

## 📦 What's Inside

### Core Files
- **SKILL.md** - Comprehensive 356-line guide on creating effective skills
- **config.toml** - Optional configuration for customization

### Scripts
- **init_skill.py** - Generate new skill scaffolding with templates
- **validate.py** - Validate skill structure and content
- **package_skill.py** - Create distributable .skill files

### Reference Guides
- **workflows.md** - Sequential and conditional workflow patterns
- **output-patterns.md** - Template and example patterns for quality output

---

## 📋 Installation

### Prerequisites
- **Python 3.7+** (required)

### Dependencies

#### Required for validation and packaging:
```bash
pip install pyyaml
```

#### Optional for TOML config support:
```bash
# Python 3.10 and below
pip install tomli

# Python 3.11+ has built-in tomllib (no install needed)
```

### Clone or Download
```bash
# If part of a skills repository
cd /path/to/skills/development/skill-creator

# Or download directly
git clone <repo-url>
```

---

## 💡 Usage Examples

### Example 1: Create a PDF Processing Skill

```bash
# Create skill
python scripts/init_skill.py pdf-helper --path ~/skills --category productivity

# This generates:
# ~/skills/pdf-helper/
# ├── SKILL.md (template with TODOs)
# ├── scripts/example.py
# ├── references/api_reference.md
# └── assets/example_asset.txt
```

**Example prompts to trigger your skill:**
- "Help me rotate this PDF"
- "Extract text from this PDF document"
- "Fill out this PDF form"

### Example 2: Create a Data Analysis Skill

```bash
python scripts/init_skill.py data-analyzer --path ~/skills --author myname
```

**Example prompts:**
- "Analyze these quarterly sales results"
- "Create a summary of this dataset"
- "Find trends in this CSV file"

### Example 3: Validate and Package

```bash
# Validate skill structure
python scripts/validate.py ~/skills/pdf-helper

# Output:
# ✅ Skill is valid!

# Package for distribution
python scripts/package_skill.py ~/skills/pdf-helper

# Output:
# 📦 Packaging skill: ~/skills/pdf-helper
# 🔍 Validating skill...
# ✅ Skill is valid!
# 
#   Added: pdf-helper/SKILL.md
#   Added: pdf-helper/scripts/rotate_pdf.py
#   ...
# ✅ Successfully packaged skill to: dist/pdf-helper.skill
```

---

## ⚙️ Configuration

### Optional config.toml

Customize defaults without editing code:

```toml
[author]
name = "your-name"  # Your name appears in new skills

[defaults]
category = "productivity"  # Default category for skills
version = "0.0.1"         # Starting version

[validation]
min_description_length = 50  # Minimum description length
max_name_length = 64         # Maximum skill name length

[packaging]
output_dir = "dist"              # Where .skill files go
exclude_patterns = [".DS_Store"]  # Files to exclude

[directories]
create_scripts = true      # Include scripts/ directory
create_references = true   # Include references/ directory
create_assets = true       # Include assets/ directory
```

**Note:** All scripts work without config.toml using sensible defaults.

---

## 📖 Documentation

### SKILL.md Guide Covers:
- **Core Principles** - Conciseness, degrees of freedom, progressive disclosure
- **Anatomy of a Skill** - SKILL.md, scripts/, references/, assets/
- **6-Step Workflow** - From understanding to iteration
- **Design Patterns** - High-level guides, domain-specific organization
- **Best Practices** - What to include and exclude

### Reference Files:
- **workflows.md** - How to structure sequential and conditional workflows
- **output-patterns.md** - Templates and examples for consistent output

---

## 🛠️ Script Reference

### init_skill.py

**Purpose:** Create new skill scaffolding

**Syntax:**
```bash
python scripts/init_skill.py <skill-name> --path <output-path> [options]
```

**Options:**
- `--category <name>` - Skill category (overrides config)
- `--author <name>` - Author name (overrides config)

**Example:**
```bash
python scripts/init_skill.py api-client --path ~/skills --category development --author alice
```

**What it creates:**
- ✅ Skill directory with proper name
- ✅ SKILL.md with frontmatter template
- ✅ Example files in scripts/, references/, assets/
- ✅ Helpful TODO comments throughout

---

### validate.py

**Purpose:** Validate skill structure and content

**Syntax:**
```bash
python scripts/validate.py <skill-directory>
```

**Checks:**
- ✅ SKILL.md exists and has valid frontmatter
- ✅ Required fields: name, description
- ✅ Naming conventions (hyphen-case, length limits)
- ✅ No unexpected frontmatter properties
- ✅ Description requirements (length, no angle brackets)

**Example:**
```bash
python scripts/validate.py ~/skills/my-skill

# Success:
# ✅ Skill is valid!

# Failure:
# ❌ Description too short (42 chars). Minimum is 50 chars.
```

---

### package_skill.py

**Purpose:** Create distributable .skill file

**Syntax:**
```bash
python scripts/package_skill.py <skill-directory> [output-dir]
```

**Features:**
- 🔍 Validates skill first (won't package invalid skills)
- 📦 Creates ZIP file with .skill extension
- 🎯 Excludes files per config (e.g., .DS_Store, __pycache__)
- ✅ Configurable compression level

**Example:**
```bash
python scripts/package_skill.py ~/skills/my-skill ./releases

# Output:
# 📦 Packaging skill: ~/skills/my-skill
# 🔍 Validating skill...
# ✅ Skill is valid!
# 
#   Added: my-skill/SKILL.md
#   Added: my-skill/scripts/helper.py
#   Skipped: my-skill/.DS_Store (excluded)
# 
# ✅ Successfully packaged skill to: ./releases/my-skill.skill
```

---

## 🎯 Best Practices

### 1. Write Clear Descriptions
Your SKILL.md description should include:
- What the skill does
- When to use it (specific triggers, scenarios, file types)
- Example use cases

**Good:**
```yaml
description: |
  PDF manipulation toolkit for rotating, extracting text, and filling forms.
  Use when working with PDF files for: (1) Rotating pages, (2) Extracting text,
  (3) Filling form fields, or (4) Analyzing PDF structure.
```

### 2. Use Progressive Disclosure
Keep SKILL.md under 500 lines. Move detailed content to references/:
- API docs → `references/api.md`
- Comprehensive examples → `references/examples.md`
- Schema documentation → `references/schema.md`

### 3. Include Helpful Examples
In generated skills, provide concrete examples:
```python
# scripts/example.py
def rotate_pdf(input_path, output_path, degrees=90):
    """Rotate PDF by specified degrees"""
    # Implementation here
```

### 4. Test Your Scripts
Run scripts before packaging to ensure they work:
```bash
python ~/skills/my-skill/scripts/helper.py
```

---

## 🔧 Troubleshooting

### "PyYAML is required"
```bash
pip install pyyaml
```

### "Could not load config.toml"
Config is optional. Scripts will use defaults. To use config:
```bash
# Python 3.10 and below
pip install tomli
```

### Validation Fails
Read error message carefully. Common issues:
- Description too short (< 50 chars)
- Invalid skill name (must be hyphen-case)
- Missing required fields (name, description)

### Package Won't Create
Ensure skill passes validation first:
```bash
python scripts/validate.py <skill-path>
```

---

## 📁 Directory Structure

```
skill-creator/
├── README.md                    # This file
├── SKILL.md                     # Comprehensive guide (356 lines)
├── config.toml                  # Optional configuration
│
├── scripts/
│   ├── init_skill.py           # Create new skills
│   ├── validate.py       # Validate skills
│   └── package_skill.py        # Package skills
│
└── references/
    ├── workflows.md            # Workflow patterns
    └── output-patterns.md      # Output patterns
```

**Generated skill structure:**
```
my-skill/
├── SKILL.md                    # Skill definition
├── scripts/                    # Executable scripts
│   └── example.py
├── references/                 # Documentation
│   └── api_reference.md
└── assets/                     # Templates, images, etc.
    └── example_asset.txt
```

---

## 🤝 Contributing

When creating skills:
1. Follow the hyphen-case naming convention
2. Include comprehensive descriptions
3. Add helpful examples in references/
4. Test scripts before packaging
5. Keep SKILL.md concise (< 500 lines)

---

## 📝 License

See LICENSE file for details.

---

## 🙋 Support

For questions or issues:
1. Read SKILL.md for comprehensive guidance
2. Check references/ for design patterns
3. Review example prompts above
4. Validate your skill with validate.py

---

**Happy skill creating! 🎉**
