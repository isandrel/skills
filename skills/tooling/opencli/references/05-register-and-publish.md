# Step 5: Register and Publish

## YAML Adapters (automatic)

YAML adapters in `src/clis/<site>/<name>.yaml` are **auto-discovered** — no manual registration needed.

Verify with:
```bash
opencli list        # should show <site> <name>
opencli validate <site>   # checks adapter integrity
```

## TypeScript Adapters (manual)

Add an import to `src/clis/index.ts`:

```typescript
// src/clis/index.ts
import './mysite/trending.js';   // ← add this line
```

Then rebuild:
```bash
bun run build
opencli list | grep mysite
```

## Full Validation Run

```bash
opencli validate <site>   # validate adapter schema
opencli verify <site>     # validate + smoke test (makes a real request)
```

## Done

Report to the user:
```
✅ Adapter registered!
📍 File: src/clis/<site>/<name>.yaml
⚡ Run: opencli <site> <name>
```
