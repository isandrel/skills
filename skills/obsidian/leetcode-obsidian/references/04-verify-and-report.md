# Step 4: Verify Output

Validate the filled note before considering the task complete.

## Checklist

- [ ] **Frontmatter intact** — YAML block is valid, all original fields preserved
- [ ] **Description unchanged** — problem statement was not modified
- [ ] **Hints unchanged** — hint callouts were not modified
- [ ] **Intuition filled** — `> [!abstract]- Intuition` has 1-3 sentence insight (not empty)
- [ ] **Algorithm filled** — `> [!info]- Algorithm` has numbered steps (not just `> 1. `)
- [ ] **Tab 1 code** — clean solution with correct method signature, no test runner
- [ ] **Tab 2 code** — same solution + test runner with `if __name__` block
- [ ] **Method name consistent** — method name in code matches `sol.methodName(...)` in test runner
- [ ] **Test cases valid** — 2-4 tests with correct expected values from problem examples
- [ ] **Complexity filled** — both Time and Space rows have O(...) values and brief notes
- [ ] **4-space indent** — all code inside `[tabs]` is indented 4 spaces
- [ ] **No extra sections** — only Approach, Solutions, and Complexity were edited

## Quick Validation

Read the final note file and confirm:

1. The three sections (Approach, Solutions, Complexity) are filled in
2. The code compiles mentally — no syntax errors or missing imports
3. Test cases match the problem's example inputs/outputs
4. The method signature matches LeetCode's expected signature

## Common Mistakes

| Mistake | Fix |
| --- | --- |
| Wrong method name in test runner | Ensure `sol.methodName(...)` matches the class method |
| Missing 4-space indent in tabs | All content under `- Python` must be indented 4 spaces |
| Test args not wrapped in tuple | Use `((arg1, arg2), expected)` not `(arg1, arg2, expected)` |
| Modified Description or Hints | Only edit Approach, Solutions, Complexity sections |
| Added `from typing import List` at module level | Use lowercase `list[int]` (Python 3.9+) or put import inline |
| Intuition explains steps instead of insight | Intuition = WHY, Algorithm = HOW |

## Done

Report to the user:

```
✅ LeetCode note created and solved!

📍 File: `{filename}`
🧩 Problem: {id}. {title} ({difficulty})
⚡ Approach: {brief approach name, e.g., "Hash Map", "Two Pointers"}
⏱️ Time: {O(...)} | 💾 Space: {O(...)}
```
