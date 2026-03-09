/**
 * Shared type definitions for the LeetCode Obsidian skill.
 */

/** LeetCode question data returned from the GraphQL API. */
export interface Question {
	questionId: string;
	title: string;
	titleSlug: string;
	content: string;
	difficulty: string;
	topicTags: { name: string }[];
	hints: string[];
	codeSnippets: { lang: string; langSlug: string; code: string }[];
}

/** Merged configuration from config.toml + CLI args. */
export interface Config {
	// settings
	site: "us" | "cn";
	downloadImages: boolean;
	language: string;
	userAgent: string;

	// paths
	outputDir: string;
	imageDir: string;
	template: string;

	// obsidian
	obsidianEnabled: boolean;
	obsidianVault: string;
	obsidianOpen: boolean;

	// note format
	filenamePattern: string;
	platform: string;
	includeHints: boolean;
	includeSolution: boolean;
	includeComplexity: boolean;

	// api
	graphqlUrl: string;
	graphqlUrlCn: string;
}
