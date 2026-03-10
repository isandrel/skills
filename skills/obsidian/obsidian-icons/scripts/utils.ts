/**
 * Minimal TOML parser for simple key-value configs.
 * Handles sections, strings, numbers, booleans, and arrays.
 */
export function parseToml(input: string): Record<string, unknown> {
  const result: Record<string, unknown> = {};
  let currentSection = result;
  const sectionStack: string[] = [];

  for (const rawLine of input.split("\n")) {
    const line = rawLine.trim();

    // Skip empty lines and comments
    if (!line || line.startsWith("#")) continue;

    // Section header [section] or [section.subsection]
    const sectionMatch = line.match(/^\[(.+)]$/);
    if (sectionMatch) {
      const parts = sectionMatch[1].split(".");
      currentSection = result;
      sectionStack.length = 0;

      for (const part of parts) {
        if (!(part in (currentSection as Record<string, unknown>))) {
          (currentSection as Record<string, unknown>)[part] = {};
        }
        currentSection = (currentSection as Record<string, unknown>)[part] as Record<string, unknown>;
        sectionStack.push(part);
      }
      continue;
    }

    // Key = value
    const kvMatch = line.match(/^(\w+)\s*=\s*(.+)$/);
    if (kvMatch) {
      const [, key, rawValue] = kvMatch;
      (currentSection as Record<string, unknown>)[key] = parseValue(rawValue.trim());
    }
  }

  return result;
}

function parseValue(raw: string): unknown {
  // String (double or single quoted)
  const strMatch = raw.match(/^["'](.*)["']$/);
  if (strMatch) return strMatch[1];

  // Boolean
  if (raw === "true") return true;
  if (raw === "false") return false;

  // Array
  if (raw.startsWith("[")) {
    const inner = raw.slice(1, -1).trim();
    if (!inner) return [];
    return inner.split(",").map((s) => parseValue(s.trim()));
  }

  // Number
  const num = Number(raw);
  if (!Number.isNaN(num)) return num;

  return raw;
}
