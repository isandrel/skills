---
name: obsidian-icons
description: "Manage folder and file icons in Obsidian vaults using the Iconize plugin. Use this skill whenever the user mentions folder icons, Iconize, icon packs, icon assignments, or wants to customize how folders/files look in Obsidian's sidebar. Covers: (1) Adding or changing folder/file icons via data.json, (2) Bulk-assigning icons to vault folders, (3) Validating icon names against installed packs, (4) Downloading missing icon SVGs for externally-set icons, (5) Looking up available icon names from Simple Icons, Lucide, Tabler, or other packs. Also trigger when user says 'add icon', 'change icon', 'folder icon', 'SiApple', or any icon pack prefix like Li/Si/Ti/Ri."
---

# Obsidian Icons (Iconize Plugin)

Manage folder and file icons via the Iconize plugin's `data.json` configuration.

## How Icons Work

The Iconize plugin stores icon assignments in:

```
.obsidian/plugins/obsidian-icon-folder/data.json
```

Format: JSON object with a `settings` key and folder/file path → icon ID mappings:

```json
{
  "settings": { ... },
  "Note": "LiNotebookPen",
  "Note/AI": "TiRobot",
  "Obsidian": "SiObsidian"
}
```

Icon IDs use the format `{PackPrefix}{IconName}` in **PascalCase**.

## Icon Packs

Read `config.toml` for the vault-specific icon pack configuration.

### Naming Convention

| Pack | Prefix | Source | Example |
|------|--------|--------|---------|
| Lucide | `Li` | Native/built-in | `LiArchive`, `LiBriefcase` |
| Simple Icons | `Si` | Brand logos | `SiObsidian`, `SiGoogle` |
| Tabler Icons | `Ti` | General icons | `TiRobot`, `TiTemplate` |
| Remix Icons | `Ri` | General icons | `RiBankLine` |
| Boxicons | `Bo` | General icons | `BoBxGroup` |
| Font Awesome Solid | `Fas` | General icons | `FasApple` |
| RPG Awesome | `Ra` | RPG-themed | `RaApple` |
| Icon Brew | `Ib` | Misc | — |
| Octicons | `Oc` | GitHub icons | — |

### Priority Order

When choosing icons, prefer in this order:

1. **Simple Icons** (`Si`) — when a brand/product icon exists
2. **Lucide** (`Li`) — primary generic icons (always available)
3. **Tabler** (`Ti`) — secondary generic icons
4. **Remix** (`Ri`) / **Font Awesome** (`Fas`) — tertiary
5. **Boxicons** (`Bo`) — fallback

Avoid emojis unless explicitly requested.

### Validating Simple Icons Names

Query the Simple Icons source JSON to verify icon names exist:

```bash
curl -s "https://raw.githubusercontent.com/simple-icons/simple-icons/{VERSION}/_data/simple-icons.json" \
  | python3 -c "import json,sys; [print(i['title']) for i in json.load(sys.stdin)['icons'] if 'SEARCH' in i['title'].lower()]"
```

Replace `{VERSION}` with the version from config.toml and `SEARCH` with search term.

## Critical: SVG Caching

**When setting icons via `data.json` externally, the plugin does NOT auto-download SVGs.**

The plugin caches used icon SVGs in `.obsidian/icons/{pack-name}/{IconName}.svg`. Icons set through the Obsidian UI are downloaded automatically, but icons set by editing `data.json` directly will show as raw text (e.g., "SiApple Apple Notes") until the SVG is cached.

### Download Missing SVGs

Run the download script after editing `data.json`:

```bash
bun run scripts/download_icons.ts [vault-path]
```

The script reads `data.json`, checks which SVGs are missing from the cache, and downloads them from the correct source repositories.

### Manual Download

Download individual SVGs using the pack source URLs from config.toml:

```bash
# Simple Icons
curl -s "https://raw.githubusercontent.com/simple-icons/simple-icons/{VERSION}/icons/{slug}.svg" \
  -o ".obsidian/icons/simple-icons/{Name}.svg"

# Lucide Icons
curl -s "https://raw.githubusercontent.com/lucide-icons/lucide/{VERSION}/icons/{slug}.svg" \
  -o ".obsidian/icons/lucide-icons/{Name}.svg"
```

**Important:** The SVG filename must be PascalCase (`Apple.svg`), but the download URL uses lowercase slug (`apple.svg`).

## Obsidian Overwrites External Edits

The Iconize plugin writes `data.json` from memory. If Obsidian is running while you edit `data.json`, your changes will be overwritten on next plugin save.

**Workaround:** Either quit Obsidian before editing, or use the download script to also re-apply the data.json after Obsidian closes.

## Workflow: Bulk Icon Assignment

1. Read current `data.json` to see existing assignments
2. List vault folders (typically top 2 levels)
3. Choose icons following the priority order
4. Update `data.json` with new mappings
5. Run `scripts/download_icons.py` to cache missing SVGs
6. Reload Obsidian (⌘Q → reopen)

## Workflow: Validate All Icons

1. Read `data.json` icon entries
2. For each icon, check if the SVG exists in `.obsidian/icons/{pack}/{Name}.svg`
3. Report missing SVGs
4. Run `scripts/download_icons.py` to download missing ones
