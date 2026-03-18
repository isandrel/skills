---
name: opencli
description: "Create and manage CLI adapters for any website using OpenCLI (github.com/jackwener/opencli). OpenCLI turns any website into a terminal command by reusing Chrome's logged-in session — zero credential risk. Use when: (1) adding a new site/command adapter (YAML or TypeScript), (2) debugging an existing adapter, (3) running built-in commands like explore/synthesize/cascade/generate, (4) choosing an authentication strategy for a website, or (5) writing template expressions for the pipeline."
---

# OpenCLI

OpenCLI transforms any website into a CLI by reusing Chrome's authenticated session via the Playwright MCP Bridge extension. Adapters are ~30-line YAML files (or TypeScript for complex cases).

## Quick Overview

```
opencli list                    # list all commands
opencli <site> <name>           # run a command
opencli <site> <name> -v        # verbose: show each pipeline step
opencli <site> <name> --json    # JSON output
opencli explore <url> --site <name>   # discover APIs
opencli cascade <api-url>             # detect simplest auth strategy
opencli generate <url>                # one-shot: explore + synthesize + register
opencli validate <site>               # validate adapter definitions
```

## Workflow: Creating a New Adapter

Progress:

- [ ] Step 1: Discover the API → Read [references/01-discover-api.md](references/01-discover-api.md)
- [ ] Step 2: Choose authentication strategy → Read [references/02-choose-strategy.md](references/02-choose-strategy.md)
- [ ] Step 3: Write the adapter (YAML or TypeScript) → Read [references/03-write-adapter.md](references/03-write-adapter.md)
- [ ] Step 4: Test and verify → Read [references/04-test-and-verify.md](references/04-test-and-verify.md)
- [ ] Step 5: Register and publish → Read [references/05-register-and-publish.md](references/05-register-and-publish.md)

**Default**: Run Steps 1 → 2 → 3 only (discover, choose, write). **Full workflow**: Run all 5 steps when the user wants a complete, tested, registered adapter.

## YAML vs TypeScript Decision

| Use YAML if…                                                             | Use TypeScript if…                            |
| ------------------------------------------------------------------------ | --------------------------------------------- |
| Purely declarative pipeline (`fetch`, `navigate`, `map`, `limit`, `tap`) | Pipeline includes `evaluate` with embedded JS |
| No custom signing / GraphQL logic                                        | Complex XHR interception or store injection   |
| Most cases — prefer YAML                                                 | Only when YAML is insufficient                |

## Template Expressions (Quick Reference)

Syntax: `${{ <expression> }}`

| Expression       | Example                               |
| ---------------- | ------------------------------------- |
| Arg access       | `${{ args.limit }}`                   |
| Current item     | `${{ item.title }}`                   |
| Zero-based index | `${{ index + 1 }}`                    |
| Raw data         | `${{ data }}`                         |
| Pipe filter      | `${{ args.limit \| default(20) }}`    |
| Fallback         | `${{ item.author \|\| 'Anonymous' }}` |

Filters: `default`, `join`, `upper`, `lower`, `truncate`, `trim`, `replace`, `keys`, `length`, `first`, `last`

## Built-in Site Commands

See `opencli list` for the full list. Notable examples:

| Site          | Commands                                                            |
| ------------- | ------------------------------------------------------------------- |
| bilibili      | `hot`, `search`, `me`, `favorite`, `history`, `feed`, `user-videos` |
| zhihu         | `hot`, `search`, `question`                                         |
| github        | `trending`, `search`                                                |
| hackernews    | `top`                                                               |
| v2ex          | `hot`, `latest`, `topic`                                            |
| twitter       | `trending`                                                          |
| reddit        | `hot`                                                               |
| youtube       | `search`                                                            |
| yahoo-finance | `quote`                                                             |

## Reference Files

| File                                                                | When to Read                                                                    |
| ------------------------------------------------------------------- | ------------------------------------------------------------------------------- |
| [01-discover-api.md](references/01-discover-api.md)                 | Starting a new adapter — need to find the API endpoint                          |
| [02-choose-strategy.md](references/02-choose-strategy.md)           | Unsure which auth strategy (`public`/`cookie`/`header`/`intercept`/`ui`) to use |
| [03-write-adapter.md](references/03-write-adapter.md)               | Writing or editing a YAML/TypeScript adapter (includes full templates)          |
| [04-test-and-verify.md](references/04-test-and-verify.md)           | Testing pipeline steps, debugging verbose output                                |
| [05-register-and-publish.md](references/05-register-and-publish.md) | Registering YAML auto-discovery or adding TS import to index.ts                 |
