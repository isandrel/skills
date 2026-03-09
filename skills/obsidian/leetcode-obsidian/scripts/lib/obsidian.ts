/**
 * Obsidian CLI integration.
 *
 * Creates notes directly in an Obsidian vault using the CLI:
 *   https://help.obsidian.md/cli
 *
 * Falls back gracefully if the CLI is unavailable.
 */

import { execSync } from "node:child_process";

/** Check if the Obsidian CLI is available on PATH. */
export function hasObsidianCli(): boolean {
	try {
		execSync("which obsidian", { stdio: "ignore" });
		return true;
	} catch {
		return false;
	}
}

/**
 * Create a note via `obsidian create`.
 *
 * @param content  - Note content (markdown)
 * @param path     - Vault-relative file path
 * @param vault    - Vault name (optional, uses active vault if empty)
 * @param openAfter - Open the note in Obsidian after creation
 * @returns true if creation succeeded
 */
export function obsidianCreate(
	content: string,
	path: string,
	vault?: string,
	openAfter = false,
): boolean {
	const args: string[] = ["obsidian"];
	if (vault) args.push(`vault=${vault}`);
	args.push("create");
	args.push(`path=${path}`);
	args.push(`content=${content}`);
	args.push("overwrite");
	if (openAfter) args.push("open");

	try {
		execSync(args.join(" "), { stdio: "ignore", timeout: 15_000 });
		return true;
	} catch (e) {
		console.warn(`  ⚠️  Obsidian CLI error: ${e}`);
		return false;
	}
}
