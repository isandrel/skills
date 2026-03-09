/**
 * Image downloader.
 *
 * Downloads images referenced in markdown content and replaces
 * remote URLs with local relative paths.
 */

import { mkdirSync, writeFileSync } from "node:fs";
import { basename, join } from "node:path";
import type { Config } from "./types.ts";

/** Download images from content and replace URLs with local paths. */
export async function downloadImages(
	content: string,
	outputDir: string,
	imageDir: string,
	questionId: string,
	title: string,
	userAgent: string,
): Promise<string> {
	const imgFolder = join(outputDir, imageDir, `${questionId}. ${title}`);
	mkdirSync(imgFolder, { recursive: true });

	const imgPattern = /!\[([^\]]*)\]\(([^)]+)\)/g;
	let updated = content;

	for (const match of content.matchAll(imgPattern)) {
		const [, , imgUrl] = match;
		if (!imgUrl.startsWith("http")) continue;

		const filename = basename(imgUrl).split("?")[0];
		const localPath = join(imgFolder, filename);

		try {
			const resp = await fetch(imgUrl, {
				headers: { "User-Agent": userAgent },
			});
			if (!resp.ok) continue;

			writeFileSync(localPath, Buffer.from(await resp.arrayBuffer()));
			updated = updated.replace(imgUrl, `${basename(imgFolder)}/${filename}`);
			console.log(`  📷 Downloaded: ${filename}`);
		} catch (e) {
			console.warn(`  ⚠️  Failed to download ${imgUrl}: ${e}`);
		}
	}

	return updated;
}
