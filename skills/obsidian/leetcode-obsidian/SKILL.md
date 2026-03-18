---
name: leetcode-obsidian
description: "Fetch LeetCode problems and generate Obsidian-compatible markdown notes with frontmatter, callouts, solution tabs, and test runner. Optionally solve with the most optimal approach. Use when: (1) Fetching a LeetCode problem by URL, ID, or slug, (2) Creating structured coding problem notes for Obsidian, (3) Building a LeetCode study collection, (4) Solving a LeetCode problem with optimal solution. Triggers: 'leetcode', 'lc problem', 'fetch problem', 'coding problem', 'solve leetcode'."
---

# LeetCode Obsidian

Fetch LeetCode problems via GraphQL API and generate structured Obsidian notes, optionally solved with the most optimal approach.

## Setup

```bash
cd skills/obsidian/leetcode-obsidian
bun install
```

## Workflow

Progress:
- [ ] Step 1: Fetch the problem → Read [references/01-fetch-problem.md](references/01-fetch-problem.md)
- [ ] Step 2: Analyze and solve → Read [references/02-analyze-and-solve.md](references/02-analyze-and-solve.md)
- [ ] Step 3: Fill the note sections → Read [references/03-fill-note-sections.md](references/03-fill-note-sections.md)
- [ ] Step 4: Verify and report → Read [references/04-verify-and-report.md](references/04-verify-and-report.md)

**Fetch only** (default): Run Step 1 only.
**Fetch and solve**: Run Steps 1 → 2 → 3 → 4 when user asks to solve (e.g., "fetch and solve", "solve leetcode", "lc solve").

## Configuration

Edit `config.toml` to set persistent defaults. CLI flags override config values. See the config file for all available options including filename patterns, note format toggles, and Obsidian integration settings.

## Template Customization

The note template is at `assets/templates/leetcode_note.md.j2` (Nunjucks/Jinja2 compatible). Available template variables:

| Variable              | Type   | Example                              |
| --------------------- | ------ | ------------------------------------ |
| `question.questionId` | str    | `"1"`                                |
| `question.title`      | str    | `"Two Sum"`                          |
| `question.titleSlug`  | str    | `"two-sum"`                          |
| `question.difficulty` | str    | `"Easy"`                             |
| `question.content`    | str    | Markdown description                 |
| `question.topicTags`  | list   | `[{"name": "Array"}, ...]`           |
| `question.hints`      | list   | `["Consider using a hash map", ...]` |
| `config`              | Config | Full config object                   |
| `now`                 | str    | `"2026-03-09T16:00"`                 |
