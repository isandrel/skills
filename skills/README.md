# Skills Directory

Skills are organized by category. Each skill has its own folder with a `SKILL.md` file.

```
skills/
├── development/          # Developer tools and skill creation
│   └── skill-creator/
├── obsidian/             # Obsidian vault integrations
│   ├── excalidraw-diagram/
│   └── obsidian-bases/
└── tooling/              # General-purpose utilities
    ├── md-to-email/
    └── skill-manager/
```

## Adding a Skill

Place your skill in the appropriate category folder (or create a new one):

```bash
python development/skill-creator/scripts/init_skill.py my-skill \
  --path . --category <category>
```

See [CONTRIBUTING.md](../CONTRIBUTING.md) for quality checklist and naming conventions.
