# Blog Platform Integration Roadmap

Platforms are ordered first by API availability (public, documented REST/GraphQL APIs before
scrape/automation-only), then by audience breadth and popularity.

The goal is wide audience coverage: developers, writers, designers, food & lifestyle creators,
newsletter authors, and business professionals should all find at least one native integration.

---

## Integration tiers

### Tier 1 — Official API, high priority

These platforms expose a public, stable API that maps cleanly onto the BlogHub
[integration contract](./contract.md). They should be built first.

| # | Platform | Auth | API style | Primary audiences | Notes |
|---|----------|------|-----------|-------------------|-------|
| 1 | **Ghost** | Admin API key | REST | Writers, newsletters, indie publishers | Full draft/publish/list. Works for both Ghost.io (hosted) and self-hosted instances. |
| 2 | **WordPress.com** | OAuth 2 / App Password | REST (WP.com v1.1 + WP REST API) | Everyone — food, lifestyle, business, tech | Largest blog platform on the web. App Password covers self-hosted WP via Jetpack or REST API. |
| 3 | **Blogger** | Google OAuth 2 | REST (Blogger API v3) | Cooking, lifestyle, general | Long-tail userbase. Google-hosted, rock-solid API. |
| 4 | **LinkedIn Articles** | OAuth 2 | REST (UGC Posts API) | Business, career, B2B professionals | High-value professional reach. Shares the same article format as other platforms. |
| 5 | **Beehiiv** | API key | REST | Newsletter authors, growth-focused writers | Modern newsletter platform with a clean public API. |
| 6 | **Tumblr** | OAuth 1 / OAuth 2 | REST | Art, design, fandom, lifestyle | Strong visual and creative userbase; supports rich text and image-heavy posts. |
| 7 | **Wix Blog** | Wix API key | REST (Wix Blog API) | Small business, food, recipes | Strong presence in cooking and local-business content. |
| 8 | **WriteFreely / Write.as** | API token | REST | Minimalist writers, Fediverse, privacy-focused | Open-source and ActivityPub-native; useful for users who self-host. |
| 9 | **Drupal** | OAuth 2 / Basic Auth | JSON:API | Enterprise publishers, NGOs, education | Widely used in institutional content sites. |

---

### Tier 2 — API available, narrower audiences

| # | Platform | Auth | API style | Primary audiences | Notes |
|---|----------|------|-----------|-------------------|-------|
| 10 | **Dribbble** | OAuth 2 | REST | Designers, UI/UX | Shot-based (images), not long-form articles. Integrate as a "cross-post cover image" action rather than full article. |
| 11 | **Behance** | Adobe OAuth 2 | REST | Designers, photographers | Project posts rather than articles. Limited API surface. |
| 12 | **Notion** | OAuth 2 / Internal token | REST | Teams, knowledge-base writers | Publish Notion pages as blog posts via export pipeline. |
| 13 | **Telegraph (Telegra.ph)** | Account token | REST | Short-form, anonymous writing | Already somewhat explored in Medium experiment code. Very simple API. |

---

### Tier 3 — No official API (browser automation / scraping)

These require a Playwright-style browser session. They are harder to maintain and must be
clearly marked as `automation` adapters in the plugin manifest.

| # | Platform | Auth | Audiences | Notes |
|---|----------|------|-----------|-------|
| 14 | **Substack** | Cookie session | Newsletters, journalism, opinion | Highest-value in this tier. No public API. Medium pattern applies. |
| 15 | **Mirror.xyz** | Wallet signature (EIP-712) | Web3, crypto writers | Blockchain publishing; auth model is fundamentally different — treat as a separate adapter category. |

---

## Coverage matrix

| Audience | Platforms |
|----------|-----------|
| Developers / Tech | Dev.to ✅, Hashnode ✅, Ghost, WordPress.com, WriteFreely |
| General writing | Medium ✅, Substack, Ghost, WordPress.com, Blogger |
| Newsletters | Medium ✅, Beehiiv, Substack, Ghost |
| Design | Tumblr, Dribbble, Behance |
| Food & Lifestyle | Blogger, Wix Blog, Tumblr, WordPress.com |
| Business / Professional | LinkedIn Articles, Beehiiv, Ghost |
| Privacy / Open-source | WriteFreely, Mirror.xyz |
| Enterprise | WordPress.com, Drupal |

---

## Status tracking

| Platform | Status | Branch |
|----------|--------|--------|
| Medium | ✅ Shipped | `main` |
| Hashnode | ✅ Shipped | `main` |
| Dev.to | ✅ Shipped | `main` |
| Ghost | 🔲 Planned | — |
| WordPress.com | 🔲 Planned | — |
| Blogger | 🔲 Planned | — |
| LinkedIn Articles | 🔲 Planned | — |
| Beehiiv | 🔲 Planned | — |
| Tumblr | 🔲 Planned | — |
| Wix Blog | 🔲 Planned | — |
| WriteFreely | 🔲 Planned | — |
| Substack | 🔲 Planned | — |
