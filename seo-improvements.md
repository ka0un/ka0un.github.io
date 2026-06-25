# SEO Audit & Improvement Plan — kasun.hapangama.com

**Site:** Kasun Hapangama — Developer Portfolio (single-page `index.html`)
**Audited:** 25 June 2026
**Canonical domain (assumed):** `https://kasun.hapangama.com/`
**Reviewer:** SEO technical audit

> Single-page personal-brand portfolio. The bottleneck for this kind of site is **not** keyword competition — it's **discoverability primitives** (crawl files, structured data) and **shareability** (social cards), because most traffic arrives via LinkedIn/GitHub/recruiter shares and branded "Kasun Hapangama" searches. The plan below is prioritised accordingly.

---

## Executive summary

The HTML is hand-crafted and, on the fundamentals, **better than most portfolios**: one `<h1>`, a clean heading hierarchy, a meaningful `<title>` and meta description, `lang="en"`, a skip link, `prefers-reduced-motion` support, keyboard-operable widgets, and *correct* use of empty `alt=""` on decorative icons that already sit next to a text label. Good baseline.

What's missing is almost entirely **technical SEO plumbing and social/structured metadata** — the things that decide how the page is crawled, how it appears when shared, and whether Google can build an entity ("Person") around it. None of these exist yet.

| # | Issue | Severity | Area |
|---|-------|----------|------|
| 1 | No `robots.txt` | High | Crawlability |
| 2 | No `sitemap.xml` | High | Crawlability |
| 3 | No canonical URL | High | Indexing / duplicates |
| 4 | No Open Graph tags | High | Social sharing |
| 5 | No Twitter Card tags | High | Social sharing |
| 6 | No structured data (JSON-LD) | High | Rich results / entity |
| 7 | No favicon / touch icon / manifest | Medium | Branding / SERP / PWA |
| 8 | Images lack `width`/`height` → CLS | Medium | Core Web Vitals |
| 9 | Below-the-fold images not lazy-loaded | Medium | Performance / LCP |
| 10 | No `<main>` landmark | Low | Semantics / a11y |
| 11 | No explicit `robots` / rich-preview meta | Low | SERP control |

---

## Detailed findings & fixes

### 1. No `robots.txt` — High
There is no `/robots.txt`. Crawlers get no guidance and, critically, no pointer to a sitemap. It's the first file Googlebot/Bingbot request.
**Fix:** Add `robots.txt` that allows full crawl and references the sitemap.

### 2. No `sitemap.xml` — High
No XML sitemap exists. Even for one page it speeds up discovery, carries `lastmod`, and is required to submit the site in Google Search Console / Bing Webmaster Tools.
**Fix:** Add `sitemap.xml` for the homepage (with the in-page section anchors documented), reference it from `robots.txt`, and submit it in Search Console.

### 3. No canonical URL — High
No `<link rel="canonical">`. The same content is reachable at `http`/`https`, `www`/non-`www`, with/without trailing slash, and with `#anchor` variants — all of which can dilute or split ranking signals.
**Fix:** Add `<link rel="canonical" href="https://kasun.hapangama.com/">`.

### 4. No Open Graph tags — High
Nothing for `og:title`, `og:description`, `og:image`, `og:url`, `og:type`. When this URL is pasted into **LinkedIn, Facebook, Slack, WhatsApp, Discord**, the unfurled card has no image and a poor title/description — the single biggest lost opportunity for a portfolio that lives on shares.
**Fix:** Add a full Open Graph block + a dedicated 1200×630 share image.

### 5. No Twitter Card tags — High
No `twitter:card`/`title`/`description`/`image`. Shares on X render as a bare link.
**Fix:** Add `summary_large_image` Twitter Card tags (can reuse the OG image).

### 6. No structured data (JSON-LD) — High
No schema.org markup. For a **personal brand**, a `Person`/`ProfilePage` graph is the highest-leverage structured data: it helps Google connect the site to the "Kasun Hapangama" entity, ties together social profiles via `sameAs`, and is eligible for richer presentation.
**Fix:** Embed a `Person` + `ProfilePage` JSON-LD block (name, jobTitle, employer, `knowsAbout`, `sameAs` → LinkedIn/GitHub, `alumniOf`).

### 7. No favicon, apple-touch-icon, or web manifest — Medium
No `favicon.ico`/SVG, no `apple-touch-icon`, no `site.webmanifest`. Browsers and Google show a default globe in tabs, bookmarks, and increasingly in mobile search results.
**Fix:** Ship an SVG favicon + PNG touch icon + `site.webmanifest`, and link them in `<head>`.

### 8. Images have no `width`/`height` → layout shift — Medium (Core Web Vitals)
All 67 `<img>` tags omit intrinsic `width`/`height`. Without them the browser can't reserve space before images load, causing **Cumulative Layout Shift (CLS)** — a ranking signal. The CSS sets `max-width:100%` but **not** `height:auto`, so dimensions must be added together with that CSS rule to stay responsive.
**Fix:** Add `height:auto` to the `img` rule and inject real intrinsic `width`/`height` (read from each file) on every local image.

### 9. Below-the-fold images not lazy-loaded — Medium
The hero is correctly eager with `fetchpriority="high"` (good — it's the LCP element). But ~25 below-the-fold images (skill icons, education/work logos) load eagerly, competing for bandwidth on first paint.
**Fix:** Add `loading="lazy"` + `decoding="async"` to below-the-fold images; leave the hero eager.

### 10. No `<main>` landmark — Low
The page has `<header>`, `<nav>`, and `<section>`s but no `<main>`. Assistive tech and crawlers benefit from an explicit main-content landmark.
**Fix:** Wrap the content sections in `<main>`.

### 11. No explicit robots / rich-preview meta — Low
Default indexing is fine, but there's no `max-image-preview:large` (which enables large image thumbnails in Google results) and no explicit `index,follow`.
**Fix:** Add `<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">`.

---

## What's already done well (leave as-is)

- Single, descriptive `<h1>`; logical `h2`/`h3`/`h4` order.
- `<title>` (35 chars) and meta `description` (134 chars) are both well within limits and keyword-relevant.
- `lang="en"`, `charset`, responsive `viewport`, `theme-color` all present.
- **Decorative `alt=""` is used correctly** — skill icons and company logos each sit beside a visible text label, so empty alt avoids redundant screen-reader output. Do **not** "fix" these.
- External links use `rel="noopener"`; fonts use `display=swap`; reduced-motion is respected.
- Hero image uses `fetchpriority="high"` — correct LCP treatment.

---

## Post-deploy checklist (manual, by owner)

1. Verify the property in **Google Search Console** and **Bing Webmaster Tools**; submit `sitemap.xml`.
2. Confirm the host serves **301 redirects** to a single canonical host (e.g. `www` → non-`www`, `http` → `https`).
3. Validate the share card with the **LinkedIn Post Inspector** and **opengraph.xyz**; validate JSON-LD with **Google Rich Results Test** / **Schema.org validator**.
4. Run **PageSpeed Insights** to confirm CLS ≈ 0 and check LCP after the image-dimension fix.
5. Consider serving images as **WebP/AVIF** (currently mostly JPG/PNG) for a further LCP win.

---

*All code-level items (1–11) are implemented in the working tree as part of this audit (changes are saved but not yet committed — review and commit when ready): edits to `index.html` plus the new `robots.txt`, `sitemap.xml`, `site.webmanifest`, `favicon.svg`/`favicon.ico`, and `assets/` icon + share-image files.*
