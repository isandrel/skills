/**
 * Note renderer.
 *
 * Renders an Obsidian markdown note from a Nunjucks/Jinja2 template.
 * The template receives the question data and full config for
 * conditional rendering (e.g., toggling hints, solution, complexity).
 */

import { basename, resolve } from "node:path";
import nunjucks from "nunjucks";
import type { Config, Question } from "./types.ts";

/** Render a note from the configured template. */
export function renderNote(question: Question, cfg: Config): string {
	const templateDir = resolve(cfg.template, "..");
	const templateFile = basename(cfg.template);

	const env = new nunjucks.Environment(
		new nunjucks.FileSystemLoader(templateDir),
		{ trimBlocks: false, lstripBlocks: false },
	);

	const now = new Date().toISOString().slice(0, 16); // YYYY-MM-DDTHH:mm

	return env.render(templateFile, { question, now, config: cfg });
}
