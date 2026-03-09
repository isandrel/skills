/**
 * LeetCode GraphQL API client.
 *
 * Handles fetching questions by slug or numeric ID, including
 * HTML→Markdown conversion of problem descriptions.
 */

import TurndownService from "turndown";
import type { Config, Question } from "./types.ts";

/** GraphQL query for problem data — fetches all fields needed for note generation. */
const QUESTION_QUERY = `
query questionData($titleSlug: String!) {
  question(titleSlug: $titleSlug) {
    questionId
    title
    titleSlug
    content
    difficulty
    topicTags { name }
    hints
    codeSnippets { lang langSlug code }
  }
}`;

/** GraphQL query to resolve a numeric ID to a slug. */
const ID_LOOKUP_QUERY = `
query problemsetQuestionList($filters: QuestionListFilterInput) {
  problemsetQuestionList: questionList(
    categorySlug: ""
    limit: 1
    skip: 0
    filters: $filters
  ) {
    questions: data { titleSlug frontendQuestionId: questionFrontendId }
  }
}`;

/** Build request headers from config. */
function headers(cfg: Config): Record<string, string> {
	return {
		Accept: "*/*",
		"User-Agent": cfg.userAgent,
		"Content-Type": "application/json",
	};
}

/** Get the GraphQL endpoint URL for the configured site. */
function graphqlUrl(cfg: Config): string {
	return cfg.site === "cn" ? cfg.graphqlUrlCn : cfg.graphqlUrl;
}

/**
 * Resolve a problem identifier (URL, numeric ID, or slug) to a slug.
 */
export async function resolveIdentifier(
	identifier: string,
	cfg: Config,
): Promise<string> {
	// URL: extract slug from /problems/<slug>/
	const urlMatch = identifier.match(/\/problems\/([^/?#]+)/);
	if (urlMatch) return urlMatch[1];

	// Numeric ID: look up slug via API
	if (/^\d+$/.test(identifier)) {
		return slugFromId(Number(identifier), cfg);
	}

	// Assume slug
	return identifier.trim().toLowerCase();
}

/** Resolve a numeric question ID to its slug. */
async function slugFromId(questionId: number, cfg: Config): Promise<string> {
	const resp = await fetch(graphqlUrl(cfg), {
		method: "POST",
		headers: headers(cfg),
		body: JSON.stringify({
			query: ID_LOOKUP_QUERY,
			variables: { filters: { searchKeywords: String(questionId) } },
		}),
	});

	if (!resp.ok) throw new Error(`HTTP ${resp.status}: ${resp.statusText}`);

	const data = (await resp.json()) as any;
	const questions = data?.data?.problemsetQuestionList?.questions ?? [];
	const match = questions.find(
		(q: any) => q.frontendQuestionId === String(questionId),
	);

	if (!match) throw new Error(`Could not find problem with ID ${questionId}`);
	return match.titleSlug;
}

/** Fetch full question data from LeetCode GraphQL API. */
export async function fetchQuestion(
	slug: string,
	cfg: Config,
): Promise<Question> {
	const resp = await fetch(graphqlUrl(cfg), {
		method: "POST",
		headers: headers(cfg),
		body: JSON.stringify({
			query: QUESTION_QUERY,
			variables: { titleSlug: slug },
		}),
	});

	if (!resp.ok) throw new Error(`HTTP ${resp.status}: ${resp.statusText}`);

	const data = (await resp.json()) as any;
	const question = data?.data?.question;
	if (!question) throw new Error(`Problem '${slug}' not found on LeetCode`);

	// Convert HTML description to Markdown
	if (question.content) {
		question.content = htmlToMarkdown(question.content);
	}

	return question as Question;
}

/** Convert HTML problem description to clean Markdown. */
function htmlToMarkdown(html: string): string {
	const turndown = new TurndownService({
		headingStyle: "atx",
		bulletListMarker: "-",
	});

	let content = turndown.turndown(html);

	// Clean up HTML entities turndown may leave behind
	content = content
		.replace(/&amp;/g, "&")
		.replace(/&lt;/g, "<")
		.replace(/&gt;/g, ">")
		.replace(/&#92;/g, "\\")
		.replace(/&quot;/g, '"')
		.replace(/&#39;/g, "'")
		.replace(/\n{3,}/g, "\n\n")
		.trim();

	return content;
}
