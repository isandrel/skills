---
name: md-to-email
description: "Transforms Markdown text into professional, styled HTML for emails. Use when you want to send emails with rich formatting (bold, lists, links, code) that look consistent across email clients. Perfect for job applications, newsletters, or professional correspondence where Markdown's simplicity is preferred but HTML's styling is required."
metadata:
  version: 0.1.0
  category: tooling
  author: isandrel
---

# MD to Email

This skill facilitates the creation of beautiful HTML emails from Markdown source. It solves the problem of inconsistent styling when pasting Markdown directly into email clients.

## Workflow

1.  **Draft in Markdown**: Write your email content using standard Markdown syntax.
2.  **Transform to HTML**: Use the provided script or instructions to convert the Markdown into styled HTML.
3.  **Create Draft**: Use a tool like `gmail.createDraft` with `isHtml: true` to send or save the formatted email.

## Transformation Methods

### Method 1: Python Script (Automated)

Run the included transformation script to generate the HTML.

```bash
python scripts/md_to_html.py message.md > message.html
```

The script uses a professional template located in `references/email_template.html`.

### Method 2: Manual (In-Context)

If you cannot run scripts, you can manually wrap your Markdown-converted HTML (which Claude can generate) with the following structure:

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        /* See references/email_template.html for full CSS */
        body { font-family: sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px; }
        /* ... inline styles ... */
    </style>
</head>
<body>
    <!-- YOUR CONVERTED HTML HERE -->
</body>
</html>
```

## Styling Principles

The included template follows these email-safe principles:
- **Max Width**: 600px for readability on desktop and mobile.
- **Typography**: System-default sans-serif stack for fast loading and clean look.
- **Spacing**: Generous margins and line-height for a modern feel.
- **Responsive**: Standard layout that works well on small screens.

## Resources

### scripts/
- `md_to_html.py`: Converts Markdown files to HTML using the `markdown` library and the default template.

### references/
- `email_template.html`: The base HTML/CSS skeleton used for styling.