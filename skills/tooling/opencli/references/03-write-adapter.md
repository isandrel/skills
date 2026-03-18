# Step 3: Write the Adapter

## Table of Contents
- [File Location](#file-location)
- [YAML Adapter Templates](#yaml-adapter-templates)
  - [Tier 1: Public API](#tier-1-public-api)
  - [Tier 2: Cookie (navigate + evaluate)](#tier-2-cookie-navigate--evaluate)
  - [Tier 3: With Search Args](#tier-3-with-search-args)
  - [Tier 4: Store Interception (tap)](#tier-4-store-interception-tap)
- [TypeScript Adapter Template](#typescript-adapter-template)
- [Pipeline Step Reference](#pipeline-step-reference)
- [Args Reference](#args-reference)

---

## File Location

```
src/clis/<site>/<name>.yaml     ← YAML adapters (auto-registered)
src/clis/<site>/<name>.ts       ← TypeScript adapters (must import in index.ts)
```

---

## YAML Adapter Templates

### Tier 1: Public API

Use when: `strategy: public`, `browser: false` — direct Node.js fetch.

```yaml
site: v2ex
name: hot
description: V2EX hot topics
domain: www.v2ex.com
strategy: public
browser: false

args:
  limit:
    type: int
    default: 20
    description: Number of results

pipeline:
  - fetch:
      url: https://www.v2ex.com/api/topics/hot.json

  - map:
      rank: ${{ index + 1 }}
      title: ${{ item.title }}
      replies: ${{ item.replies }}

  - limit: ${{ args.limit }}

columns: [rank, title, replies]
```

### Tier 2: Cookie (navigate + evaluate)

Use when: login session needed, cookies sufficient.

```yaml
site: zhihu
name: hot
description: Zhihu hot list
domain: www.zhihu.com
strategy: cookie
browser: true

args:
  limit:
    type: int
    default: 20

pipeline:
  - navigate: https://www.zhihu.com       # establish session / load cookies

  - evaluate: |                           # browser fetch — cookies sent automatically
      (async () => {
        const res = await fetch('/api/v3/feed/topstory/hot-lists/total?limit=50', {
          credentials: 'include'
        });
        const d = await res.json();
        return (d?.data || []).map(item => {
          const t = item.target || {};
          return { title: t.title, heat: item.detail_text || '', answers: t.answer_count };
        });
      })()

  - map:
      rank: ${{ index + 1 }}
      title: ${{ item.title }}
      heat: ${{ item.heat }}
      answers: ${{ item.answers }}

  - limit: ${{ args.limit }}

columns: [rank, title, heat, answers]
```

### Tier 3: With Search Args

Use when: command has a keyword/query argument.

```yaml
site: github
name: search
description: Search GitHub repositories
domain: github.com
strategy: public
browser: false

args:
  query:
    type: str
    description: Search query
  limit:
    type: int
    default: 10

pipeline:
  - fetch:
      url: https://api.github.com/search/repositories?q=${{ args.query }}&per_page=${{ args.limit | default(10) }}
      headers:
        Accept: application/vnd.github.v3+json

  - select: items

  - map:
      rank: ${{ index + 1 }}
      name: ${{ item.full_name }}
      stars: ${{ item.stargazers_count }}
      description: ${{ item.description | default('') }}

  - limit: ${{ args.limit }}

columns: [rank, name, stars, description]
```

### Tier 4: Store Interception (tap)

Use when: Vue + Pinia/Vuex, XHR interception needed.

```yaml
site: xiaohongshu
name: notifications
description: Xiaohongshu notifications
domain: www.xiaohongshu.com
strategy: intercept
browser: true

args:
  type:
    type: str
    default: mentions
    description: "Notification type: mentions, likes, or connections"
  limit:
    type: int
    default: 20

columns: [rank, user, action, content, time]

pipeline:
  - navigate: https://www.xiaohongshu.com/notification
  - wait: 3
  - tap:
      store: notification
      action: getNotification
      args:
        - ${{ args.type | default('mentions') }}
      capture: /you/
      select: data.message_list
      timeout: 8
  - map:
      rank: ${{ index + 1 }}
      user: ${{ item.user_info.nickname }}
      action: ${{ item.title }}
      content: ${{ item.comment_info.content }}
  - limit: ${{ args.limit | default(20) }}
```

---

## TypeScript Adapter Template

Use for: header auth (CSRF/Bearer tokens), complex XHR, GraphQL, or any pipeline that needs custom JS logic.

```typescript
// src/clis/<site>/<name>.ts
import { cli } from '../../registry.js';
import { Strategy } from '../../strategies/index.js';

cli({
  site: 'mysite',
  name: 'trending',
  description: 'Get trending items from mysite',
  domain: 'www.mysite.com',
  strategy: Strategy.HEADER,
  args: {
    limit: { type: 'int', default: 20 },
  },
  columns: ['rank', 'title', 'score'],
  func: async (page, kwargs) => {
    await page.goto('https://www.mysite.com');

    // Extract auth token from cookies / DOM
    const token = await page.evaluate(() => {
      const match = document.cookie.match(/csrf_token=([^;]+)/);
      return match ? match[1] : '';
    });

    const data = await page.evaluate(async (token: string) => {
      const res = await fetch('/api/trending', {
        headers: { 'x-csrf-token': token },
        credentials: 'include',
      });
      return res.json();
    }, token);

    return (data.items || [])
      .slice(0, kwargs.limit)
      .map((item: any, i: number) => ({
        rank: i + 1,
        title: item.title,
        score: item.score,
      }));
  },
});
```

Then register in `src/clis/index.ts`:
```typescript
import './mysite/trending.js';
```

---

## Pipeline Step Reference

| Step | Description | Example |
|---|---|---|
| `fetch` | HTTP GET (Node.js or browser) | `fetch: { url: "https://..." }` |
| `navigate` | Navigate browser to URL | `navigate: https://...` |
| `evaluate` | Run JS in browser page context | `evaluate: \| (async()=>{...})()` |
| `select` | Extract sub-path from data | `select: data.items` |
| `map` | Transform each item's fields | `map: { rank: ${{ index+1 }} }` |
| `filter` | Filter items by condition | `filter: ${{ item.score > 0 }}` |
| `sort` | Sort by field | `sort: { by: score, order: desc }` |
| `limit` | Cap result count | `limit: ${{ args.limit }}` |
| `wait` | Wait N seconds | `wait: 3` |
| `tap` | Call Pinia/Vuex store action | see Tier 4 template above |

---

## Args Reference

```yaml
args:
  myarg:
    type: str | int | float | bool
    default: <value>          # optional; omit to make required
    description: "..."        # shown in --help
```

## Next

Proceed to [Step 4: Test and Verify](04-test-and-verify.md).
