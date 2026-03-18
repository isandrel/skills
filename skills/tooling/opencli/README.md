# opencli skill

AI agent skill for creating and managing [OpenCLI](https://github.com/jackwener/opencli) adapters — turn any website into a terminal command by reusing Chrome's logged-in session.

## What This Skill Does

Guides an AI agent through the full adapter development workflow:

1. Discover the target API (`opencli explore`)
2. Select the right authentication strategy (`opencli cascade`)
3. Write a YAML or TypeScript adapter
4. Test and debug with verbose output
5. Register and validate

## Example Prompts

- _"Add a new opencli adapter for reddit's saved posts"_
- _"Create a YAML adapter for HackerNews job listings"_
- _"Which opencli strategy should I use for a site that needs a CSRF token?"_
- _"Debug why my zhihu adapter returns empty results"_
- _"Run opencli cascade on this API endpoint to find the auth strategy"_

## Prerequisites

- [OpenCLI](https://github.com/jackwener/opencli) installed: `npm install -g @jackwener/opencli`
- Chrome with the [Playwright MCP Bridge extension](https://github.com/jackwener/opencli#setup) installed (for browser-based strategies)
- Node.js / Bun for TypeScript adapters

## Skill Structure

```
opencli/
├── SKILL.md                        # Agent instructions + workflow checklist
├── references/
│   ├── 01-discover-api.md          # How to find API endpoints (explore command, manual)
│   ├── 02-choose-strategy.md       # 5-tier auth strategy decision tree
│   ├── 03-write-adapter.md         # Full YAML + TypeScript templates
│   ├── 04-test-and-verify.md       # Debugging pipeline steps
│   └── 05-register-and-publish.md  # Registration (auto YAML vs manual TS import)
└── assets/                         # (reserved for future templates)
```

## Authentication Strategies (Quick Reference)

| Strategy    | When                       | Browser |
| ----------- | -------------------------- | ------- |
| `public`    | Open API, no auth          | No      |
| `cookie`    | Session cookies sufficient | Yes     |
| `header`    | CSRF / Bearer token needed | Yes     |
| `intercept` | Vue + Pinia/Vuex XHR       | Yes     |
| `ui`        | No accessible API          | Yes     |
