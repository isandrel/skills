# Step 4: Test and Verify

## Process

1. **Build the project** (required after any TypeScript change):
   ```bash
   bun run build
   ```
   YAML adapters don't require a build — changes take effect immediately.

2. **Confirm the command is registered**:
   ```bash
   opencli list | grep <site>
   ```

3. **Run the command** with default args:
   ```bash
   opencli <site> <name>
   ```

4. **Run with verbose mode** to see each pipeline step's input/output:
   ```bash
   opencli <site> <name> -v
   ```

5. **Verify output formats**:
   ```bash
   opencli <site> <name> --json   # JSON
   opencli <site> <name> --csv    # CSV
   opencli <site> <name> --md     # Markdown
   ```

## Debugging Pipeline Steps

In verbose mode (`-v`), each step shows:
```
[navigate] → https://www.zhihu.com ... done
[evaluate] → input: (none)  output: [{title: "...", heat: "...", answers: 42}, ...]
[map]      → input: 50 items  output: 50 items with {rank, title, heat, answers}
[limit]    → input: 50 items  output: 20 items
```

If a step outputs `undefined` or `[]`:
- `fetch` step → check URL and whether auth is needed
- `evaluate` → make sure the function returns a value (e.g., `return data.items`)
- `select` → check the response path (use `--json` on the raw response first)
- `tap` → see debugging section below

## Debugging `tap` Steps (intercept strategy)

1. List available Pinia stores:
   ```bash
   opencli evaluate "Object.keys(window.__pinia?.state?.value || {})"
   ```

2. List actions for a specific store:
   ```bash
   opencli evaluate "Object.keys(window.__pinia?._s?.get('notification') || {})"
   ```

3. Check the `capture` URL pattern matches actual XHR requests (watch Network tab in DevTools)

## Common Pitfalls

| Problem | Fix |
|---|---|
| `evaluate` returns `undefined` | Ensure the IIFE returns a value: `(async () => { return ...; })()` |
| Nested field access fails | Use `item.a?.b` or `${{ item.a \| default('') }}` |
| `select` finds nothing | Log the raw response first with `select: ''` (select root) |
| Cookies not sent | Add a `navigate` step before `fetch`/`evaluate` |
| Missing `navigate`, session 401 | Cookie-based strategies always need `navigate` first |
| TypeScript adapter not found | Did you add `import './site/name.js'` to `src/clis/index.ts`? |

## Next

Proceed to [Step 5: Register and Publish](05-register-and-publish.md).
