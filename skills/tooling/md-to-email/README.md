# MD to Email Skill

A skill for AI agents to transform Markdown content into professional, styled HTML emails.

## Features

- 📝 **Markdown Support**: Use standard Markdown for drafting.
- 🎨 **Professional Styling**: Clean, modern CSS template.
- 📧 **Email Safe**: Uses inline-compatible styles for broad support.
- 🚀 **Automation Ready**: Simple Python script for batch conversion.

## Installation

This skill requires the `markdown` Python library.

```bash
uv pip install markdown
```

## Usage

### As a User

Ask your agent: "Can you convert this markdown to a beautiful email draft for me?"

### As a Developer

The skill provides a script to generate the HTML:

```bash
python scripts/md_to_html.py my_email.md > my_email.html
```

## Structure

- `SKILL.md`: Instructions for the AI agent.
- `scripts/md_to_html.py`: Transformation engine.
- `references/email_template.html`: Professional HTML/CSS skeleton.
