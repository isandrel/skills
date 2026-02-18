---
name: md-to-email
description: "Transforms Markdown text into professional, styled HTML for emails. Use when you want to send emails with rich formatting (bold, lists, links, code) that look consistent across email clients. Perfect for job applications, newsletters, or professional correspondence where Markdown's simplicity is preferred but HTML's styling is required."
metadata:
  version: 0.2.0
  category: tooling
  author: isandrel
---

# MD to Email

This skill converts Markdown into styled HTML emails. It solves the problem of inconsistent styling when pasting Markdown directly into email clients.

## Workflow

1. **Draft in Markdown**: Write your email content using standard Markdown syntax.
   - Use trailing double spaces (`  `) at end of lines to force line breaks (e.g. in signatures).
2. **Transform to HTML**: Convert the Markdown into styled HTML using the script and a template.
3. **Preview**: Open the HTML file in a browser to preview.
4. **Use**: Copy-paste the rendered HTML into your email client, or use a tool like `gmail.createDraft` with `isHtml: true`.

## Templates

Two email templates are available in `references/`:

| Template              | Font              | Style                                                 | Best For                                       |
| --------------------- | ----------------- | ----------------------------------------------------- | ---------------------------------------------- |
| `email_template.html` | System sans-serif | Professional, 600px max-width, generous spacing       | Newsletters, formal correspondence             |
| `gmail_template.html` | Arial, 14px       | Minimal, matches Gmail's default "Sans Serif" compose | Everyday Gmail emails, referrals, applications |

## Usage

### Basic (default template)

```bash
python scripts/md_to_html.py message.md > message.html
```

### Gmail-style

```bash
python scripts/md_to_html.py message.md references/gmail_template.html > message.html
```

### Preview in browser

```bash
open message.html
```

## Markdown Tips for Emails

- **Line breaks in signatures**: Use trailing double spaces at end of each line:
  ```markdown
  --  
  **Name**  
  **Title | Company**  
  📧 email@example.com  
  📞 +1 (xxx) xxx-xxxx
  ```
- **Links**: Use `[text](url)` for clickable links.
- **Bold**: Use `**text**` for emphasis.
- **Lists**: Use `1.` for ordered, `-` for unordered.

## Resources

### scripts/
- `md_to_html.py`: Converts Markdown files to HTML using the `markdown` library and a template.

### references/
- `email_template.html`: Professional styled template (600px, system sans-serif).
- `gmail_template.html`: Gmail-matching minimal template (Arial, 14px).