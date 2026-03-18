# Step 1: Discover the API

Find the API endpoint(s) a website uses before writing an adapter.

## Process

### Automatic Discovery (preferred)

```bash
opencli explore <url> --site <name>
# e.g.:
opencli explore https://news.ycombinator.com --site hackernews
```

Outputs to `.opencli/explore/<site>/`:
- `metadata.json` — domain, framework detected (Vue/React/Pinia/Vuex), auth recommendations
- `endpoints.json` — discovered API endpoints with methods and sample payloads
- `candidates/` — generated YAML candidates (used by `synthesize`)

### Manual Discovery

1. Open the target page in Chrome (logged in)
2. Open DevTools → Network tab → filter by `Fetch/XHR`
3. Perform the action you want to automate (scroll, search, navigate)
4. Find the relevant request — note:
   - URL and query params
   - Request headers (look for `Authorization`, `x-csrf-token`, `Bearer`)
   - Cookie presence (`credentials: include` needed?)
   - Response shape (what path holds the list of items?)

### Framework Detection

`explore` also detects frontend frameworks, which affects strategy choice:

| Detected | Implication |
|---|---|
| Vue + Pinia/Vuex | `intercept` strategy (`tap` step) is available |
| React | Usually `cookie` or `header` strategy |
| None / static | Likely `public` strategy |

## Gotchas

- Some APIs return data only after login — use `navigate` first to establish a session before `fetch`
- Paginated APIs: note the pagination param (e.g., `page`, `offset`, `cursor`) — expose it as an `arg`
- Mobile endpoints (often `/api/v2/` or `/m/`) are sometimes simpler and public

## Next

Proceed to [Step 2: Choose Authentication Strategy](02-choose-strategy.md).
