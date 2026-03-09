/**
 * Configuration loader.
 *
 * Loads from config.toml with layered overrides:
 *   built-in defaults → config.toml → CLI args
 *
 * All tunables live in config.toml — no magic numbers in source code.
 */

import { existsSync, readFileSync } from "node:fs";
import { resolve } from "node:path";
import { parse as parseToml } from "smol-toml";
import type { Config } from "./types.ts";

export const SKILL_ROOT = resolve(import.meta.dir, "../..");
export const DEFAULT_CONFIG_PATH = resolve(SKILL_ROOT, "config.toml");
export const DEFAULT_TEMPLATE_PATH = resolve(
	SKILL_ROOT,
	"assets",
	"templates",
	"leetcode_note.md.j2",
);

/** Expand ~ to home directory. */
export function expandHome(p: string): string {
	return p.startsWith("~") ? p.replace("~", Bun.env.HOME ?? "") : p;
}

/** Built-in defaults — overridden by config.toml values. */
export function defaultConfig(): Config {
	return {
		site: "us",
		downloadImages: true,
		language: "python3",
		userAgent:
			"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",

		outputDir: ".",
		imageDir: "Attachments",
		template: DEFAULT_TEMPLATE_PATH,

		obsidianEnabled: false,
		obsidianVault: "",
		obsidianOpen: false,

		filenamePattern: "{id}. {title}",
		platform: "LeetCode",
		includeHints: true,
		includeSolution: true,
		includeComplexity: true,

		graphqlUrl: "https://leetcode.com/graphql",
		graphqlUrlCn: "https://leetcode.cn/graphql",
	};
}

/** Load and merge config from a TOML file. */
export function loadConfig(configPath: string = DEFAULT_CONFIG_PATH): Config {
	const cfg = defaultConfig();

	if (!existsSync(configPath)) return cfg;

	let data: Record<string, any>;
	try {
		data = parseToml(readFileSync(configPath, "utf-8"));
	} catch {
		return cfg;
	}

	// settings
	const s = data.settings ?? {};
	if (s.site) cfg.site = s.site;
	if (s.download_images !== undefined) cfg.downloadImages = s.download_images;
	if (s.language) cfg.language = s.language;
	if (s.user_agent) cfg.userAgent = s.user_agent;

	// paths
	const p = data.paths ?? {};
	if (p.output_dir) cfg.outputDir = expandHome(p.output_dir);
	if (p.image_dir) cfg.imageDir = p.image_dir;
	if (p.template) cfg.template = expandHome(p.template);

	// obsidian
	const o = data.obsidian ?? {};
	if (o.enabled !== undefined) cfg.obsidianEnabled = o.enabled;
	if (o.vault) cfg.obsidianVault = o.vault;
	if (o.open_after_create !== undefined) cfg.obsidianOpen = o.open_after_create;

	// note format
	const n = data.note ?? {};
	if (n.filename_pattern) cfg.filenamePattern = n.filename_pattern;
	if (n.platform) cfg.platform = n.platform;
	if (n.include_hints !== undefined) cfg.includeHints = n.include_hints;
	if (n.include_solution !== undefined)
		cfg.includeSolution = n.include_solution;
	if (n.include_complexity !== undefined)
		cfg.includeComplexity = n.include_complexity;

	// api
	const a = data.api ?? {};
	if (a.graphql_url) cfg.graphqlUrl = a.graphql_url;
	if (a.graphql_url_cn) cfg.graphqlUrlCn = a.graphql_url_cn;

	return cfg;
}

/** Generate filename from pattern and question data. */
export function makeFilename(
	pattern: string,
	question: {
		questionId: string;
		title: string;
		titleSlug: string;
		difficulty: string;
	},
): string {
	return (
		pattern
			.replace("{id}", question.questionId)
			.replace("{title}", question.title)
			.replace("{slug}", question.titleSlug)
			.replace("{difficulty}", question.difficulty) + ".md"
	);
}
