---
name: leetcode-obsidian
description: "Fetch LeetCode problems and generate Obsidian-compatible markdown notes with frontmatter, callouts, solution tabs, and test runner. Use when: (1) Fetching a LeetCode problem by URL, ID, or slug, (2) Creating structured coding problem notes for Obsidian, (3) Building a LeetCode study collection. Triggers: 'leetcode', 'lc problem', 'fetch problem', 'coding problem'."
---

# LeetCode Obsidian

Fetch LeetCode problems via GraphQL API and generate structured Obsidian notes.

## Setup

```bash
cd skills/obsidian/leetcode-obsidian
bun install
```

## Usage

Run the script directly with Bun:

```bash
# By URL
bun scripts/fetch_problem.ts "https://leetcode.com/problems/two-sum/"

# By problem ID
bun scripts/fetch_problem.ts 1

# By slug
bun scripts/fetch_problem.ts two-sum

# Fetch multiple problems in one run
bun scripts/fetch_problem.ts two-sum add-two-numbers 3sum

# Fetch from a batch file
bun scripts/fetch_problem.ts --batch-file ./problems.txt

# With options
bun scripts/fetch_problem.ts two-sum --output-dir ~/vault/LeetCode/ --download-images

# Create directly in Obsidian vault and open it
bun scripts/fetch_problem.ts two-sum --obsidian --open

# Target a specific vault
bun scripts/fetch_problem.ts two-sum --obsidian --vault "My Vault" --output-dir "LeetCode/"
```

### Options

| Flag                | Default            | Description                                                           |
| ------------------- | ------------------ | --------------------------------------------------------------------- |
| `--batch-file`      | none               | Read identifiers from a file, one per line (`#` comments supported)   |
| `--output-dir`      | from config or `.` | Directory to save the note (or vault-relative path with `--obsidian`) |
| `--image-dir`       | `Attachments`      | Subdirectory for downloaded images                                    |
| `--download-images` | from config        | Download problem images locally                                       |
| `--site`            | `us`               | LeetCode site: `us` or `cn`                                           |
| `--config`          | `config.toml`      | Custom config file path                                               |
| `--template`        | built-in           | Custom Nunjucks/Jinja2 template                                       |
| `--obsidian`        | from config        | Create note via [Obsidian CLI](https://help.obsidian.md/cli)          |
| `--vault`           | auto               | Obsidian vault name                                                   |
| `--open`            | from config        | Open note in Obsidian after creation                                  |

> **Obsidian CLI**: When `--obsidian` is enabled, notes are created via `obsidian create path=<path> content=<text>` for proper vault indexing. Auto-falls back to file write if CLI is unavailable.

For batch runs, the script processes identifiers sequentially and prints a success/failure summary at the end. You can combine positional identifiers and `--batch-file` in the same invocation.

### Configuration

Edit `config.toml` to set persistent defaults. CLI flags override config values. See the config file for all available options including filename patterns, note format toggles, and Obsidian integration settings.

## Generated Note Format

The script produces a `.md` file named `{id}. {title}.md` with:

- **YAML frontmatter**: link, questionId, platform, difficulty, tags, dates
- **Description**: Problem statement converted from HTML to Markdown
- **Hints**: Rendered as `> [!note]- Hint` Obsidian callouts
- **Approach**: Intuition + Algorithm callouts (blank for user to fill)
- **Solutions**: Python tabs with clean solution + test runner
- **Complexity**: Time/Space table
- **Notes**: Empty section for user notes

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
