# Step 2: Choose Authentication Strategy

OpenCLI has 5 authentication tiers. **Always use the simplest tier that works** — lower tiers are faster and more reliable.

## Auto-Detection (recommended)

```bash
opencli cascade <api-url>
# e.g.:
opencli cascade https://www.zhihu.com/api/v3/feed/topstory/hot-lists/total
```

Probes PUBLIC → COOKIE → HEADER automatically and reports the simplest working strategy.

## Strategy Decision Tree

```
Can you fetch the URL directly with Node.js (no browser)?
├── YES → strategy: public   (fastest, no browser needed)
└── NO
    Does adding { credentials: 'include' } in browser fetch work?
    ├── YES → strategy: cookie   (navigate first to load session)
    └── NO
        Do you need to inject custom headers (Bearer/CSRF)?
        ├── YES → strategy: header   (TypeScript adapter, extract token from cookies)
        └── NO
            Does the site use Vue + Pinia/Vuex stores?
            ├── YES → strategy: intercept   (use tap step to call store actions)
            └── NO → strategy: ui   (last resort: full DOM automation)
```

## Strategy Comparison

| Strategy    | Speed  | Browser | Complexity | Use When                           |
| ----------- | ------ | ------- | ---------- | ---------------------------------- |
| `public`    | Fast   | No      | Low        | Open APIs, no auth needed          |
| `cookie`    | Medium | Yes     | Low        | Login required, cookies sufficient |
| `header`    | Medium | Yes     | Medium     | CSRF tokens, Bearer tokens needed  |
| `intercept` | Medium | Yes     | High       | Vue/Pinia apps, XHR interception   |
| `ui`        | Slow   | Yes     | Very High  | No accessible API exists           |

## Setting `browser: true/false`

```yaml
browser: false   # strategy: public  (Node.js fetch, no Chrome needed)
browser: true    # all other strategies (Chrome via Playwright MCP Bridge)
```

## Examples

```yaml
# Public API
strategy: public
browser: false

# Cookie-based (navigate to load session first)
strategy: cookie    # (or omit — cookie is default when browser: true)
browser: true

# Header injection (use TypeScript adapter)
strategy: header
browser: true

# Store interception
strategy: intercept
browser: true
```

## Gotchas

- `public` fails if the server checks `Origin` or `Referer` headers
- `cookie` requires navigating to the domain first — always add a `navigate` step
- `header` tokens often expire — extract them dynamically from `document.cookie` in the `evaluate` step
- `intercept` / `tap` requires Vue + Pinia or Vuex; will not work on React apps

## Next

Proceed to [Step 3: Write the Adapter](03-write-adapter.md).
