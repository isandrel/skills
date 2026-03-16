#!/usr/bin/env bun
/**
 * LeetCode Problem Fetcher for Obsidian — CLI entry point.
 *
 * Usage:
 *   bun scripts/fetch_problem.ts <url-or-id-or-slug> [options]
 *
 * All configuration lives in config.toml. CLI flags override config values.
 * Run with --help for all options.
 */

import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { join, resolve } from "node:path";
import { parseArgs } from "node:util";

import {
	loadConfig,
	makeFilename,
	expandHome,
	DEFAULT_CONFIG_PATH,
} from "./lib/config.ts";
import { resolveIdentifier, fetchQuestion } from "./lib/leetcode.ts";
import { renderNote } from "./lib/renderer.ts";
import { downloadImages } from "./lib/images.ts";
import { hasObsidianCli, obsidianCreate } from "./lib/obsidian.ts";

// ---------------------------------------------------------------------------
// CLI argument parsing
// ---------------------------------------------------------------------------

const { values, positionals } = parseArgs({
	args: Bun.argv.slice(2),
	options: {
		"batch-file": { type: "string" },
		"output-dir": { type: "string" },
		"image-dir": { type: "string" },
		"download-images": { type: "boolean", default: false },
		site: { type: "string" },
		template: { type: "string" },
		config: { type: "string" },
		obsidian: { type: "boolean", default: false },
		vault: { type: "string" },
		open: { type: "boolean", default: false },
		help: { type: "boolean", short: "h", default: false },
	},
	allowPositionals: true,
});

if (values.help || (positionals.length === 0 && !values["batch-file"])) {
	console.log(`
Usage: bun scripts/fetch_problem.ts <url-or-id-or-slug> [more-identifiers...] [options]
       bun scripts/fetch_problem.ts --batch-file <path> [options]

Arguments:
  identifier              LeetCode problem URL, numeric ID, or slug
  more-identifiers        Additional problems to fetch in the same run

Options:
  --batch-file <path>     Read identifiers from a file (one per line)
  --output-dir <dir>      Output directory (default: from config)
  --image-dir <dir>       Image subdirectory (default: from config)
  --download-images       Download problem images locally
  --site <us|cn>          LeetCode site (default: from config)
  --template <path>       Custom Nunjucks/Jinja2 template
  --config <path>         Config file path (default: config.toml)
  --obsidian              Create note via Obsidian CLI
  --vault <name>          Obsidian vault name
  --open                  Open note in Obsidian after creation
  -h, --help              Show this help

Examples:
  bun scripts/fetch_problem.ts two-sum
  bun scripts/fetch_problem.ts two-sum add-two-numbers 3sum
  bun scripts/fetch_problem.ts --batch-file ./problems.txt
  bun scripts/fetch_problem.ts 1 --output-dir ~/vault/LeetCode/
  bun scripts/fetch_problem.ts two-sum --obsidian --open
`);
	process.exit(0);
}

// ---------------------------------------------------------------------------
// Main
// ---------------------------------------------------------------------------

// Load config: --config > default config.toml > built-in defaults
const configPath = values.config
	? expandHome(values.config)
	: DEFAULT_CONFIG_PATH;
const cfg = loadConfig(configPath);

// CLI overrides
if (values["output-dir"]) cfg.outputDir = expandHome(values["output-dir"]);
if (values["image-dir"]) cfg.imageDir = values["image-dir"];
if (values["download-images"]) cfg.downloadImages = true;
if (values.site) cfg.site = values.site as "us" | "cn";
if (values.template) cfg.template = expandHome(values.template);
if (values.obsidian) cfg.obsidianEnabled = true;
if (values.vault) cfg.obsidianVault = values.vault;
if (values.open) cfg.obsidianOpen = true;

// Validate template
if (!existsSync(cfg.template)) {
	console.error(`❌ Template not found: ${cfg.template}`);
	process.exit(1);
}

function parseBatchFile(batchFilePath: string): string[] {
	const filepath = expandHome(batchFilePath);
	if (!existsSync(filepath)) {
		throw new Error(`Batch file not found: ${filepath}`);
	}

	return readFileSync(filepath, "utf-8")
		.split(/\r?\n/)
		.map((line) => line.trim())
		.filter((line) => line && !line.startsWith("#"));
}

function writeNote(noteContent: string, filename: string): void {
	if (cfg.obsidianEnabled && hasObsidianCli()) {
		const notePath =
			cfg.outputDir !== "." ? `${cfg.outputDir}/${filename}` : filename;
		console.log("🔮 Creating note via Obsidian CLI...");
		const success = obsidianCreate(
			noteContent,
			notePath,
			cfg.obsidianVault || undefined,
			cfg.obsidianOpen,
		);
		if (success) {
			console.log(`✅ Created in Obsidian: ${notePath}`);
			return;
		}

		console.log("  ↪ Falling back to file write...");
	} else if (cfg.obsidianEnabled) {
		console.warn("⚠️  Obsidian CLI not found, writing to disk instead");
	}

	const outDir = resolve(cfg.outputDir);
	mkdirSync(outDir, { recursive: true });
	const filepath = join(outDir, filename);
	writeFileSync(filepath, noteContent, "utf-8");
	console.log(`✅ Saved: ${filepath}`);
}

async function fetchAndWriteProblem(identifier: string): Promise<void> {
	console.log(`🔍 Parsing identifier: ${identifier}`);
	const slug = await resolveIdentifier(identifier, cfg);
	console.log(`  → Slug: ${slug}`);

	console.log(`📥 Fetching problem from LeetCode (${cfg.site})...`);
	const question = await fetchQuestion(slug, cfg);
	console.log(
		`  ✅ ${question.questionId}. ${question.title} (${question.difficulty})`,
	);

	if (cfg.downloadImages && question.content) {
		console.log(`🖼️  Downloading images to: ${join(cfg.outputDir, cfg.imageDir)}`);
		question.content = await downloadImages(
			question.content,
			cfg.outputDir,
			cfg.imageDir,
			question.questionId,
			question.title,
			cfg.userAgent,
		);
	}

	console.log("📝 Rendering note...");
	const noteContent = renderNote(question, cfg);
	const filename = makeFilename(cfg.filenamePattern, question);
	writeNote(noteContent, filename);
}

let identifiers = [...positionals];
if (values["batch-file"]) {
	try {
		identifiers = identifiers.concat(parseBatchFile(values["batch-file"]));
	} catch (e: any) {
		console.error(`❌ ${e.message}`);
		process.exit(1);
	}
}

identifiers = identifiers.map((identifier) => identifier.trim()).filter(Boolean);

if (identifiers.length === 0) {
	console.error("❌ No problem identifiers provided");
	process.exit(1);
}

const seen = new Set<string>();
identifiers = identifiers.filter((identifier) => {
	if (seen.has(identifier)) return false;
	if (!identifier) return false;
	seen.add(identifier);
	return true;
});

const failures: { identifier: string; message: string }[] = [];
for (const [index, identifier] of identifiers.entries()) {
	if (identifiers.length > 1) {
		console.log(
			`\n=== [${index + 1}/${identifiers.length}] ${identifier} ===`,
		);
	}

	try {
		await fetchAndWriteProblem(identifier);
	} catch (e: any) {
		const message = e?.message ?? String(e);
		failures.push({ identifier, message });
		console.error(`❌ Failed for '${identifier}': ${message}`);
	}
}

if (identifiers.length > 1) {
	console.log(
		`\n📦 Batch complete: ${identifiers.length - failures.length}/${identifiers.length} succeeded`,
	);
}

if (failures.length > 0) {
	for (const failure of failures) {
		console.error(`  - ${failure.identifier}: ${failure.message}`);
	}
	process.exit(1);
}
