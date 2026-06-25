# Compatibility Analysis & Hardening Plan — kasun.hapangama.com

**Site:** Kasun Hapangama — Developer Portfolio (single-page `index.html`)
**Audited:** 25 June 2026
**Support target:** **Modern + graceful degradation** — full fidelity on browsers from ~2018 onward; anything older still gets a **readable, navigable** page (never a blank one).
**Reviewer:** Cross-browser / device-compatibility review
**Constraint:** **No change to the current UI** on modern browsers.

> **Bottom line.** The site uses a lot of genuinely modern CSS/JS, and most of it degrades fine — *except one bug that breaks the entire page.* Every animated element starts at `opacity:0` and is only made visible by a JavaScript `IntersectionObserver`. If JavaScript is disabled, blocked, or the browser is old enough to lack `IntersectionObserver`, **the page renders blank below the hero.** That single issue is the priority. Everything else is prefixes and small fallbacks.

---

## Executive summary

| # | Issue | Severity | Breaks on |
|---|-------|----------|-----------|
| 1 | Content hidden until JS reveal — no `<noscript>` / no `IntersectionObserver` fallback | **Critical** | JS off, old/proxy browsers, IO-less engines |
| 2 | `backdrop-filter` without `-webkit-` prefix | **Medium** | All Safari/iOS up to v18 |
| 3 | `margin-inline` for centering, no logical-prop fallback | **Medium** | Safari <14.1, Chrome <87, older Android |
| 4 | `clamp()` typography with no static fallback (16×) | **Medium** | Safari <13.1, Chrome <79, IE |
| 5 | `aspect-ratio` boxes can collapse without fallback (4×) | **Medium** | Safari <15, Chrome <88 |
| 6 | `gap` in **flexbox** unsupported on older Safari | **Low–Med** | Safari <14.1 |
| 7 | Interactive content (project details/lightbox) is JS-only | **Medium** | JS off (content unreachable) |
| 8 | CSS custom properties power *all* styling (no fallback) | **Low** (below floor) | IE11 |
| 9 | `loading`/`decoding`/`svh`/`overscroll-behavior` no-ops | **Info** | Old browsers (degrade safely) |
| 10 | Next-gen images need a classic fallback | **Handled** | Resolved by `<picture>` work |

**The plan:** fix #1 so content is *guaranteed* visible without JS; add the missing prefixes/fallbacks (#2–#6); document #7–#9. End state: a phone from 2016, a locked-down corporate browser with JS disabled, and a screen reader all get the full content; modern browsers look **exactly** as they do now.

---

## ✅ Implemented — what changed (25 Jun 2026)

| Fix | Implementation |
|---|---|
| **#1 Blank-page bug** | `<html class="no-js">` + an early flip script → `js`; CSS `html:not(.js) .r{opacity:1!important}` reveals everything when JS is off; the reveal script feature-detects `IntersectionObserver` and `try/catch`-falls back to revealing all. **Verified: content is visible with JS disabled.** |
| **#2 backdrop-filter** | Added `-webkit-backdrop-filter` for Safari/iOS. |
| **#3 margin-inline** | Added physical `margin-left/right:auto` (+ `width`/`max-width`) fallback for the main container. |
| **#4 clamp()** | Static `font-size` fallback before every display `clamp()` (hero, section heads, stats, etc.). |
| **#5 aspect-ratio** | `@supports not (aspect-ratio)` gives the thumbnail/cover/photo boxes explicit heights so they don't collapse. |
| **#7–#9** | Documented; `<picture>` JPEG/PNG fallback means old browsers get a format they understand (compat win from the perf work). JS hardened with a safe iterator + null-guards so no missing API aborts the script. |

All changes are additive — modern browsers render byte-for-byte as before. Floor: full fidelity ~2018+, readable/navigable below that.

---

## The critical one, in detail

### 1. Page is blank without JavaScript (or without `IntersectionObserver`) — *Critical*

**The code.**

```css
.r{ opacity:0; transform:translateY(7px); transition:opacity .18s, transform .18s; }
.r.in{ opacity:1; transform:none; }
```
```js
addEventListener('DOMContentLoaded', function(){
  var io = new IntersectionObserver(function(es){ /* adds .in */ });
  document.querySelectorAll('.r').forEach(function(el){ io.observe(el); });
});
```

Almost every section, tile, card, and heading carries class `.r`, so it starts **invisible** and is only revealed when the observer adds `.in`.

**When it fails (blank page):**
- **JavaScript disabled or blocked** — privacy setups, corporate proxies, NoScript, some in-app browsers. There is **no `<noscript>`** path.
- **No `IntersectionObserver`** — IE11, Safari < 12.1, old Android Browser/UC/Opera Mini, KaiOS. `new IntersectionObserver(...)` throws and the script aborts before anything is revealed.
- A JS error anywhere earlier on the page would have the same effect.

The only thing that currently saves *some* users is the `prefers-reduced-motion` rule (it forces `.r` visible) — but that only helps people who set that OS preference.

**The fix (no visual change for anyone else).**
- Put a `no-js` class on `<html>` and have the first inline script swap it to `js` immediately. In CSS, when **not** in `js` mode, force `.r { opacity:1; transform:none; }`. → JS-off users see everything, instantly.
- **Feature-detect** `IntersectionObserver`. If it's missing, just add `.in` to every `.r` (or reveal them) instead of constructing the observer. → old engines see everything.
- Wrap the observer setup in a guard so a failure can never leave content hidden.

This keeps the reveal animation pixel-identical on modern browsers and turns the worst-case from "blank page" into "content visible, just without the fade-in."

---

## Other findings & fixes

### 2. `backdrop-filter` needs `-webkit-` — *Medium*

```css
#pm{ … backdrop-filter:blur(4px); }   /* project modal */
```
Safari and iOS Safari require **`-webkit-backdrop-filter`** (the unprefixed form only landed in Safari 18, 2024). Today the modal's blur silently does nothing on most Apple devices. **Fix:** add `-webkit-backdrop-filter:blur(4px);` alongside it. (The modal also has an `rgba()` background, so the degradation is graceful even where blur is unsupported — but the prefix restores the intended look on Safari.)

### 3. `margin-inline` centering — *Medium*

```css
.wrap{ width:min(92vw,1180px); margin-inline:auto; }
```
`.wrap` is the main content container. On Safari <14.1 / Chrome <87 / older Android, `margin-inline` is ignored and **the whole layout sticks to the left edge**. **Fix:** add `margin-left:auto; margin-right:auto;` before `margin-inline:auto;` (older browsers use the physical ones; modern browsers use the logical one — identical result).

### 4. `clamp()` typography fallback — *Medium*

`clamp()` is used 16× for fluid headings (hero name, section headers). On Safari <13.1 / Chrome <79 / IE the **entire `font-size` declaration is dropped**, so those elements fall back to the inherited size — the hero name can render at body-text size. **Fix:** precede each critical `clamp()` with a static fallback, e.g. `font-size:3rem; font-size:clamp(2rem,5vw,3.4rem);`. Old browsers take the first; modern browsers take the second. Text is always readable.

### 5. `aspect-ratio` boxes — *Medium*

```css
.cthumb, .certthumb{ aspect-ratio:1.3/1; … }
```
On Safari <15 / Chrome <88 these thumbnails have **no intrinsic height** and can collapse to 0. **Fix:** give them an explicit fallback `height` (or a padding-ratio box) before `aspect-ratio`, so old browsers reserve space and new browsers use the ratio.

### 6. Flexbox `gap` — *Low–Medium*

`gap` is used on flex rows (nav, tag lists). **Flexbox** `gap` is unsupported on Safari <14.1 (grid `gap` is fine). Effect: items touch with no spacing — cosmetic, not breaking. **Fix (optional, targeted):** add a small `margin` fallback on the key flex children (e.g. nav links, tags) for those engines, or accept the minor spacing loss as graceful degradation.

### 7. Interactive content is JS-only — *Medium (content availability)*

The **project detail modal** is built entirely from a JS `PROJECTS` object, and the **image lightbox** needs JS. With JavaScript off:
- The reveal fix (#1) ensures the page and project **cards** are visible and readable.
- But the deeper **project write-ups** (problem/solution/result) and full-size image views **can't open** — that content lives only in JS.

For a portfolio this is usually acceptable degradation (the cards summarize each project). If you want the detail reachable without JS later, the durable pattern is native `<details>`/`<summary>` or per-project anchors. **Documented as a recommendation**, not changed now (it's a content-architecture change, not a bug).

### 8. CSS custom properties power everything — *Low (below support floor)*

Every color/spacing token is a CSS variable (`var(--ink)`, etc.). **IE11 doesn't support custom properties**, so on IE11 the design loses its colors/spacing. Given the agreed **modern + graceful-degradation** floor, IE11 is intentionally below the line (Microsoft itself ended IE11 support in 2022). Noted for completeness; **not** worth the weight of full variable fallbacks. The page remains *textually* readable even there.

### 9. Safe no-ops on old browsers — *Informational*

These already degrade correctly and need no work: `loading="lazy"` / `decoding="async"` (old browsers load eagerly), `min-height:100svh` (a `100vh` fallback is already declared right before it — good), `overscroll-behavior`, `scroll-behavior:smooth`, `:focus-visible` (falls back to normal focus), variable-font axes (fall back to nearest static/system via the existing `Georgia`/`system-ui` font stacks).

### 10. Next-gen images — *Resolved by the performance work*

Introducing AVIF/WebP could have **broken** old browsers — but because the performance plan serves them via `<picture>` with the original JPG/PNG as the `<img>` fallback, **old browsers automatically get the format they understand.** This is the rare change that improves performance *and* compatibility at once. Just keep the `<img>` fallback on every `<picture>`.

---

## Device & accessibility coverage (already solid)

- **Viewport** meta present; layout is fluid (`clamp`, `min()`, grid) → scales across phone→desktop.
- **`prefers-reduced-motion`** respected (animations disabled, content forced visible).
- **`prefers-color-scheme`** — theme color set; design is intentionally one palette (fine).
- **Keyboard**: skip link, `:focus-visible` rings, modals trap/restore focus, cards are `role="button"` + `tabindex` + Enter/Space.
- **Screen readers**: one `<h1>`, clean heading order, `<main>` landmark, decorative icons correctly `alt=""`, modal `aria-hidden` toggled.
- **Touch**: targets are comfortably sized; hover effects have non-hover fallbacks.

The reveal fix (#1) is what makes all of the above actually reachable on the widest set of devices.

---

## Implementation order (what this plan executes)

1. **Reveal fallback** — `no-js`→`js` class flip + `IntersectionObserver` feature-detection *(fixes the blank-page bug)*.
2. **CSS fallbacks** — `-webkit-backdrop-filter`; physical-margin centering; static `font-size` before `clamp()`; height fallback before `aspect-ratio`; targeted flex-`gap` margins.
3. **JS hardening** — guard observer construction, null-check element lookups so a missing API never aborts the script.
4. **Image fallbacks** — `<picture>` keeps original JPG/PNG `<img>` (done as part of the performance work).
5. Verify content is fully visible with JavaScript disabled and on an emulated old engine; confirm modern UI is byte-for-byte unchanged.

*Companion document: `performance-analysis.md` (rendering speed, caching, nginx/Cloudflare).*
