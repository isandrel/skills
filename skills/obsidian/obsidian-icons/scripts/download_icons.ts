#!/usr/bin/env bun
/**
 * Download missing icon SVGs for Obsidian Iconize plugin.
 *
 * Reads data.json, checks which icons are missing from the SVG cache,
 * and downloads them from their respective source repositories.
 *
 * Usage: bun run scripts/download_icons.ts [vault-path]
 */

import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { join, resolve } from "node:path";
import { parseToml } from "./utils";

interface PackConfig {
  prefix: string;
  version: string;
  base_url: string;
  index_url?: string;
}

interface Config {
  vault: { path: string; data_json: string; icons_dir: string };
  packs: Record<string, PackConfig>;
}

interface MissingIcon {
  path: string;
  iconId: string;
  iconName: string;
  packName: string;
  packConfig: PackConfig;
  svgPath: string;
}

function loadConfig(skillDir: string): Config {
  const raw = readFileSync(join(skillDir, "config.toml"), "utf-8");
  return parseToml(raw) as unknown as Config;
}

function expandHome(p: string): string {
  return p.startsWith("~/") ? p.replace("~", Bun.env.HOME ?? "") : p;
}

/** Convert PascalCase icon name to lowercase slug (e.g., NotebookPen -> notebook-pen) */
function toSlug(name: string): string {
  return name
    .replace(/([a-z])([A-Z])/g, "$1-$2")
    .replace(/([a-zA-Z])(\d)/g, "$1-$2")
    .toLowerCase();
}

function findMissingIcons(
  data: Record<string, unknown>,
  vaultPath: string,
  config: Config,
): MissingIcon[] {
  const iconsDir = join(vaultPath, config.vault.icons_dir);
  const packs = config.packs ?? {};

  // Build prefix -> pack mapping (longest prefix first)
  const prefixMap = new Map<string, [string, PackConfig]>();
  for (const [packName, packConfig] of Object.entries(packs)) {
    prefixMap.set(packConfig.prefix, [packName, packConfig]);
  }
  const prefixes = [...prefixMap.keys()].sort((a, b) => b.length - a.length);

  const missing: MissingIcon[] = [];

  for (const [path, iconId] of Object.entries(data).sort()) {
    if (path === "settings" || typeof iconId !== "string") continue;

    for (const prefix of prefixes) {
      if (iconId.startsWith(prefix)) {
        const iconName = iconId.slice(prefix.length);
        const [packName, packConfig] = prefixMap.get(prefix)!;
        const svgPath = join(iconsDir, packName, `${iconName}.svg`);

        if (!existsSync(svgPath)) {
          missing.push({ path, iconId, iconName, packName, packConfig, svgPath });
        }
        break;
      }
    }
  }

  return missing;
}

async function downloadIcon(icon: MissingIcon): Promise<boolean> {
  const { base_url, version } = icon.packConfig;
  if (!base_url) return false;

  const slugs = [toSlug(icon.iconName), icon.iconName.toLowerCase()];
  const seen = new Set<string>();

  for (const slug of slugs) {
    if (seen.has(slug)) continue;
    seen.add(slug);

    const url = base_url.replace("{version}", version).replace("{slug}", slug);

    try {
      const res = await fetch(url);
      if (res.ok) {
        const svg = await res.text();
        if (svg.includes("<svg")) {
          const dir = join(icon.svgPath, "..");
          mkdirSync(dir, { recursive: true });
          writeFileSync(icon.svgPath, svg);
          return true;
        }
      }
    } catch {
      continue;
    }
  }

  return false;
}

async function main() {
  const skillDir = resolve(import.meta.dir, "..");
  const config = loadConfig(skillDir);

  const vaultPath = Bun.argv[2]
    ? expandHome(Bun.argv[2])
    : expandHome(config.vault.path);

  if (!existsSync(vaultPath)) {
    console.error(`✗ Vault not found: ${vaultPath}`);
    process.exit(1);
  }

  const dataPath = join(vaultPath, config.vault.data_json);
  const data = JSON.parse(readFileSync(dataPath, "utf-8"));
  const missing = findMissingIcons(data, vaultPath, config);

  if (missing.length === 0) {
    console.log("✓ All icon SVGs are cached");
    return;
  }

  console.log(`Found ${missing.length} missing icon(s):\n`);

  let success = 0;
  const failed: MissingIcon[] = [];

  for (const icon of missing) {
    process.stdout.write(`  ${icon.iconId} (${icon.packName})... `);
    if (await downloadIcon(icon)) {
      console.log("✓");
      success++;
    } else {
      console.log("✗");
      failed.push(icon);
    }
  }

  console.log(`\n${"─".repeat(40)}`);
  console.log(`Downloaded: ${success}/${missing.length}`);

  if (failed.length > 0) {
    console.log(`Failed: ${failed.length}`);
    for (const icon of failed) {
      console.log(`  - ${icon.iconId} (${icon.path})`);
    }
    console.log("\nTip: Set failed icons via Obsidian UI (right-click → Change Icon)");
  }
}

main();
