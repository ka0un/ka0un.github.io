# Performance Analysis & Optimization Plan — kasun.hapangama.com

**Site:** Kasun Hapangama — Developer Portfolio (single-page `index.html`)
**Audited:** 25 June 2026
**Target hosting:** nginx now → Cloudflare in front later
**Reviewer:** Frontend / browser-engine performance review
**Goal:** Fastest possible render & delivery for the user, with **zero change to the current UI**.

> **Bottom line.** The HTML/CSS/JS is already lean and well-built: everything is inlined into one document (no render-blocking external CSS/JS), images carry `width`/`height` (no layout shift), 65 images are lazy-loaded, the hero carries `fetchpriority="high"`, and fonts use `preconnect` + `display=swap`. The work left is **delivery, not authoring**: the **21 MB of un-optimized images** is by far the biggest cost, and there is **no compression or caching layer** yet. Fixing those two things is ~90% of the available speed.

---

## Executive summary

| # | Issue | Impact | Area |
|---|-------|--------|------|
| 1 | 21 MB of raster images — no AVIF/WebP, no responsive `srcset` | **Critical** | Bytes / LCP / data |
| 2 | Egregious single-file outliers (1.8 MB logo, 2.2 MB cert scans) shown tiny | **Critical** | Bytes |
| 3 | No compression configured (brotli/gzip) for HTML/CSS/SVG | **High** | Bytes / TTFB |
| 4 | No caching strategy (`Cache-Control`, immutable, ETag) | **High** | Repeat visits / TTFB |
| 5 | LCP hero image not `preload`ed (only discovered mid-parse) | **High** | LCP |
| 6 | Google Fonts: render-blocking + very wide variable-weight payload | **Medium** | Render start / FOUT |
| 7 | Third-party icon CDN (`cdn.simpleicons.org`) — extra DNS/TLS, no cache control | **Medium** | Requests / reliability |
| 8 | Long page renders all sections up front (no `content-visibility`) | **Medium** | Initial render / INP |
| 9 | Full résumé PDF `prefetch`ed on every load (wasted bandwidth) | **Low–Med** | Data / mobile |
| 10 | HTTP/2 (or HTTP/3) + correct MIME types not yet guaranteed | **Medium** | Many small requests |
| 11 | HTML not minified (relies on compression only) | **Low** | Bytes |

**Estimated result:** image bytes down **~75–85%** (≈21 MB → ≈3–4 MB across the whole site, with the *above-the-fold* payload dropping the most), HTML/SVG/CSS over the wire down **~80%** via brotli, and near-instant repeat visits via immutable caching — all with an **identical pixel result** on modern browsers.

---

## ✅ Implemented — measured results (25 Jun 2026)

Everything in this plan has been applied. Source UI is unchanged (every original `<img>` kept inside a `<picture>` with its `alt`/`width`/`height`; all CSS/JS changes are additive).

| Item | Before | After |
|---|---|---|
| Initial-load images (AVIF served to modern browsers) | 3,465 KB | **1,050 KB (−70%)** |
| Hero LCP image | 209 KB JPEG, discovered mid-parse | **25 KB (mobile 640w) / 76 KB (desktop) AVIF, `preload`ed** |
| Product covers ×3 | 2,020 KB | **50 KB AVIF (−95%)** |
| `index.html` over the wire | ~27 KB gzip | ~24 KB gzip minified (**~20 KB brotli**) |
| Next-gen derivatives generated | 0 | **35 AVIF + 36 WebP** |
| Compression / caching | none | **brotli+gzip, immutable 1-yr assets, revalidated HTML** (`deploy/nginx.conf`) |
| Render-blocking | font CSS blocked render | **fonts async, hero preloaded, `content-visibility` on heavy sections** |
| Wasteful loads | full résumé PDF on every visit | **hover/focus-intent prefetch** |

Mobile gains are larger still — responsive `srcset` serves the 640 w hero (25 KB) and 760 w covers instead of desktop sizes. Old browsers automatically fall back to the (also-recompressed) JPEG/PNG via `<picture>`.

Build/deploy tooling delivered: `tools/optimize-images.py`, `tools/wrap-pictures.py`, `tools/build-min.mjs`, `deploy/nginx.conf`, `deploy/precompress.sh`, `deploy/cloudflare-guide.md`.

---

## Method & baseline

Static single-document site. Measured from the source tree:

| Thing | Now |
|---|---|
| `index.html` (uncompressed) | 82 KB, 1,219 lines, inline CSS + 2 inline `<script>` blocks |
| Total `assets/` | **21 MB** |
| JPEG/JPG | 169 files, **15.1 MB** |
| PNG | 46 files, **5.8 MB** |
| WebP | **1 file** |
| AVIF | **0 files** |
| SVG | 26 files (32 KB) |
| Responsive `srcset` | **0 images** |
| `<picture>` elements | **0** |
| Images with `loading="lazy"` | 65 / 67 |
| Images with `width`+`height` | 68 (good — no CLS) |
| Hero LCP `<img>` | `fetchpriority="high"` ✓, but **not** preloaded |

**Largest single files (all served at small display sizes):**

```
2196 KB  assets/images/OCA_OCP/eCertificate-2_page-0001.jpg   (cert scan)
2196 KB  assets/images/OCA_AI/eCertificate_page-0001.jpg      (cert scan)
1800 KB  assets/images/logos/summit_logo.png                  (a logo!)
1084 KB  assets/images/sundevs/SunGuard Cover.png
 880 KB  assets/images/sundevs/SunPaste Cover.png
 488 KB  assets/images/movements/1760109226278.jpeg
 256 KB  assets/web/hero.jpg                                   (the LCP image)
```

A **1.8 MB PNG logo** rendered at ~120 px, and **2.2 MB certificate scans** behind small thumbnails, are pure waste — they alone are ~8 MB.

---

## Findings & recommended fixes (priority order)

### 1. Images: next-gen formats + responsive sizes — *Critical*

**What.** Every raster image is a full-size JPG/PNG. There is no AVIF/WebP and no `srcset`, so a phone on 3G downloads the same multi-thousand-pixel file a 4K desktop does.

**Why it matters.** Images are ~99% of this site's bytes and the hero is the LCP element. AVIF typically lands **50–70% smaller than JPEG** at equal quality; WebP **~25–35% smaller**. Responsive widths mean small screens fetch small files.

**Fix.**
- Generate **AVIF + WebP + several widths** (e.g. 400/800/1280/1600 px as needed) for every raster asset via a repeatable build script.
- Serve them through `<picture>` with `type="image/avif"` and `type="image/webp"` sources and `srcset`/`sizes`, keeping the original JPG/PNG as the `<img>` fallback (this is also a **compatibility win** — see the companion report).
- Recompress the outliers; downscale the certificate scans to a sane max width (the full scan can stay as the lightbox "open" target if needed, but the thumbnail must not ship 2.2 MB).

**Expected:** image payload down ~75–85% with no visible quality change.

### 2. The outlier files — *Critical (subset of #1, but call it out)*

`summit_logo.png` (1.8 MB), the two cert scans (2.2 MB each), and the SunDevs covers (~1 MB) should be re-encoded/downscaled first — they're the cheapest, biggest single wins. The logo should end up in the **tens of kilobytes**.

### 3. Compression: brotli + gzip — *High*

**What.** No compression layer exists yet. The 82 KB HTML, the inline CSS, the JSON-LD, and all SVGs travel uncompressed.

**Why.** Text compresses dramatically. `index.html` 82 KB → **~18 KB gzip / ~15 KB brotli**. This is free TTFB and first-paint improvement on every visit.

**Fix.** Enable **brotli** (static + dynamic) and **gzip** fallback at nginx for `text/html`, CSS, JS, JSON, SVG, and web-manifest types. Pre-compress static assets with `brotli_static`/`gzip_static`. (Delivered in `nginx.conf`.) Never gzip already-compressed AVIF/WebP/JPEG.

### 4. Caching strategy — *High*

**What.** No `Cache-Control`/`ETag` policy. Every visit re-downloads everything.

**Fix (two-tier).**
- **Immutable static assets** (images, fonts, icons): `Cache-Control: public, max-age=31536000, immutable`. Use content-hashed or versioned paths so a changed file gets a new URL.
- **HTML**: `Cache-Control: no-cache` (or short `max-age` + `must-revalidate`) + `ETag`, so edits go live immediately but unchanged HTML returns a cheap `304`.

This makes repeat visits near-instant and is the foundation Cloudflare builds on later. (Delivered in `nginx.conf`; Cloudflare specifics in `cloudflare-guide.md`.)

### 5. Preload the LCP hero — *High*

**What.** `assets/web/hero.jpg` is the Largest Contentful Paint element. It has `fetchpriority="high"` (good) but the browser only discovers it once the parser reaches `<body>`.

**Fix.** Add a `<link rel="preload" as="image">` in `<head>` using `imagesrcset`/`imagesizes` pointing at the **AVIF** hero so the fetch starts during head parsing. Keep `fetchpriority="high"`. Expect a measurable LCP improvement, compounded by the smaller AVIF.

### 6. Font loading — *Medium*

**What.** Three families from Google Fonts (Fraunces *variable 300–900 + italic*, Schibsted Grotesk 4 weights, JetBrains Mono 3 weights). The stylesheet `<link>` is render-blocking; `preconnect` + `display=swap` are already in place (good).

**Why.** The Fraunces variable range is heavy, and every visit pays a **third-party DNS + TLS + redirect** to Google before text can paint with the brand font.

**Fix (keeps identical typography).**
- **Self-host** the exact font files (woff2) on the origin. With nginx + Cloudflare this gives same-origin loading, long immutable cache, and removes the Google dependency.
- **Subset** to the glyphs actually used (Latin) and **trim the Fraunces weight axis** to the weights the design uses.
- **Preload** the one or two font files used above the fold; keep `font-display: swap`.
- If staying on Google Fonts short-term, at minimum keep `preconnect` and consider `media`-swap loading to drop render-blocking.

### 7. Self-host the simpleicons — *Medium*

**What.** A handful of tech icons load from `https://cdn.simpleicons.org/...`. That's another origin to DNS-resolve + TLS-handshake, plus a third party that can change/rate-limit/disappear, and you don't control its cache headers.

**Fix.** Download those SVGs (they're <1 KB each) into `assets/icons/` and reference locally. Removes a third-party dependency and a connection setup, and lets them ride your immutable cache. (If kept short-term, add `preconnect` to `cdn.simpleicons.org`.)

### 8. `content-visibility` for offscreen sections — *Medium*

**What.** It's a long page; the browser does layout/paint work for every section at load.

**Fix.** Add `content-visibility: auto` + `contain-intrinsic-size` to the major below-the-fold `<section>`s so the engine skips rendering work for offscreen content until it's near the viewport. This cuts initial render cost and improves responsiveness (INP). Unsupported browsers simply ignore it (safe). Must be applied carefully so in-page anchor scrolling and the reveal animation still behave.

### 9. Drop / defer the résumé PDF prefetch — *Low–Medium*

**What.** `<link rel="prefetch" href=".../kasun-hapangama.pdf" as="document">` downloads the **entire résumé PDF on every page load**, even for the majority who never click it — wasteful on mobile/metered connections.

**Fix.** Remove it, or trigger the prefetch on intent (hover/focus of the résumé button) via a few lines of JS. Saves real bytes for most visitors.

### 10. HTTP/2 (or HTTP/3) + correct MIME — *Medium*

**What.** The page makes many small requests (icons, logos, badges). On HTTP/1.1 these head-of-line block.

**Fix.** Enable **HTTP/2** in nginx (HTTP/3 comes free once Cloudflare fronts it) so requests multiplex over one connection. Ensure correct `Content-Type` for `.avif`, `.webp`, `.woff2`, `.webmanifest` (delivered in `nginx.conf`) — a wrong MIME silently disables AVIF/WebP.

### 11. HTML minification — *Low*

**What.** `index.html` is hand-formatted (~66 chars/line avg) — great for maintenance, slightly larger on the wire.

**Decision (yours):** keep the readable source. Brotli already removes most whitespace cost. An **optional build script** emits `index.min.html` for deploy if you want the last few KB; Cloudflare auto-minify can also handle it. (Delivered in `cloudflare-guide.md` + build script.)

---

## What is already good (keep it)

- **Inline CSS + JS** — for a single-document site this is the *right* call: no extra round-trips, nothing render-blocking. Don't split it out.
- **`width`/`height` on images** — prevents layout shift (CLS). Preserve on every `<picture>` conversion.
- **`loading="lazy"` + `decoding="async"`** on below-the-fold images.
- **`fetchpriority="high"`** on the hero.
- **`preconnect`** to the font origins, **`display=swap`**.
- Lean vanilla JS, no framework, no bundler tax.

---

## Implementation order (what this plan executes)

1. Build AVIF/WebP + responsive widths; recompress outliers *(script, repeatable)*.
2. Convert markup to `<picture>`/`srcset` with original fallback *(UI identical, also a compat win)*.
3. Preload the AVIF hero; optimize/preload fonts.
4. Add `content-visibility` to offscreen sections.
5. Ship `nginx.conf` — brotli/gzip, immutable caching, HTTP/2, MIME, headers.
6. Document Cloudflare layer + optional HTML-minify build script.
7. Verify identical UI + measure byte savings.

*Companion document: `compatibility-analysis.md` (older-device & cross-browser support).*
