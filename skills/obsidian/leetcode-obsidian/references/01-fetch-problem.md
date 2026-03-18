# Step 1: Fetch the Problem

Run the fetch script to create the base Obsidian note from LeetCode's API.

## Usage

```bash
# By URL
bun scripts/fetch_problem.ts "https://leetcode.com/problems/two-sum/"

# By problem ID
bun scripts/fetch_problem.ts 1

# By slug
bun scripts/fetch_problem.ts two-sum

# Fetch multiple problems
bun scripts/fetch_problem.ts two-sum add-two-numbers 3sum

# Fetch from a batch file (one identifier per line, # for comments)
bun scripts/fetch_problem.ts --batch-file ./problems.txt

# With custom output directory
bun scripts/fetch_problem.ts two-sum --output-dir ~/vault/LeetCode/ --download-images

# Create directly in Obsidian vault and open
bun scripts/fetch_problem.ts two-sum --obsidian --open

# Target a specific vault
bun scripts/fetch_problem.ts two-sum --obsidian --vault "My Vault" --output-dir "LeetCode/"
```

## Options

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

## Output

The script prints progress and the saved file path:

```
🔍 Parsing identifier: two-sum
  → Slug: two-sum
📥 Fetching problem from LeetCode (us)...
  ✅ 1. Two Sum (Easy)
🖼️  Downloading images to: ./Attachments
📝 Rendering note...
✅ Saved: /path/to/1. Two Sum.md
```

## Generated Note Structure

The output `.md` file named `{id}. {title}.md` contains:

- **YAML frontmatter** — link, questionId, platform, difficulty, tags, encountered, completed, created, updated
- **Description** — problem statement (HTML → Markdown)
- **Hints** — collapsible `> [!note]- Hint` callouts
- **Approach** — blank Intuition + Algorithm callouts (filled in Step 3)
- **Solutions** — Python tabs with skeleton code + test runner (filled in Step 3)
- **Complexity** — blank Time/Space table (filled in Step 3)
- **Notes** — empty section

## Gotchas

- LeetCode rate-limits anonymous API requests. If you get HTTP 429 errors, wait a few minutes.
- Some premium-only problems may return empty content.
- The `--download-images` flag needs network access to fetch remote images from LeetCode's CDN.

## Next

If the user asked to solve the problem, proceed to [Step 2: Analyze and Solve](02-analyze-and-solve.md).
