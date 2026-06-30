# Generative Engine Optimization (GEO) Analysis — kasun.hapangama.com

**Site:** Kasun Hapangama — Developer Portfolio (single-page `index.html`)
**Analysed:** 25 June 2026
**Goal:** Make the site maximally readable, extractable, and **citable** by AI answer engines — ChatGPT / OpenAI, Claude, Perplexity, Google AI Overviews & Gemini, Bing Copilot, and the crawlers that feed them — **without changing a single visible pixel of the current UI.**

> **GEO ≠ SEO.** Classic SEO optimises for a *ranked list of blue links*. GEO optimises for a *synthesised answer*. An answer engine doesn't "rank" this page — it reads it, extracts facts, and decides whether to **quote Kasun by name** in its response. That favours three things: (1) the content must be reachable **without running JavaScript**, (2) the facts must be **explicit and machine-structured**, and (3) the site must **welcome AI crawlers** rather than silently block them. This page is strong on visual craft but, as shipped, loses on all three.

---

## How AI systems see this site today

I evaluated the page the way a non-JavaScript AI crawler does (most retrieval crawlers fetch raw HTML and do **not** execute JS reliably).

| # | Finding | Severity | Why it matters for AI |
|---|---------|----------|-----------------------|
| 1 | **All 12 project case studies are invisible without JS** | **Critical** | The rich problem/solution/result detail lives in a `var PROJECTS={…}` object injected via `innerHTML`. A non-JS crawler sees only card titles — the most citable content (metrics like "1,000+ buyers", "19,000+ servers", "3,000+ decision-makers") never reaches the model. |
| 2 | **No AI-crawler policy in `robots.txt`** | High | GPTBot, ClaudeBot, PerplexityBot, Google-Extended, Applebot-Extended etc. aren't addressed. For a personal brand you *want* these to crawl; an explicit Allow removes ambiguity and signals intent. |
| 3 | **No `llms.txt`** | High | The emerging convention (llmstxt.org) gives models a clean, curated markdown digest + links. It's the single highest-leverage GEO primitive and costs nothing. |
| 4 | **Thin structured data** | High | Only a basic `Person`/`ProfilePage` existed. AI extracts facts far more reliably from schema.org than from prose. No `Organization`, `WebSite`, credentials, projects, or products were modelled. |
| 5 | **No machine-readable Q&A** | Medium | Answer engines preferentially lift from explicit question→answer pairs. There was no `FAQPage` describing who Kasun is, what he builds, where he works, or how to reach him. |
| 6 | **Project metrics not surfaced as facts** | Medium | Quantified outcomes are the most "quotable" units for an LLM. They were trapped in JS strings, not exposed as structured `description`/`about` fields. |

What's already AI-friendly (keep): static server-rendered hero/about/experience/education text, clean heading hierarchy, a meta description, `sameAs`-able social links, fast static delivery (AI crawlers have short timeouts), and a canonical URL.

---

## Fixes implemented (all UI-invisible)

Every change below is either a **new file** or lives inside `<head>` as metadata / JSON-LD. The rendered body, CSS, and behaviour are byte-for-byte unchanged.

### 1. Surface the hidden project & product content as structured data — *fixes the Critical finding*
Added schema.org JSON-LD `ItemList`s describing all **12 projects** (as `CreativeWork` / `SoftwareSourceCode`, including repo URLs for the open-source ones) and the **4 SUNDEVS products** (as `SoftwareApplication` with store URLs). Each carries a distilled problem→solution→result description **and the quantified outcomes**, so an AI can read and cite them with zero JavaScript. This is the highest-impact change: it moves Kasun's best evidence from "invisible" to "machine-extractable."

### 2. `llms.txt` + `llms-full.txt`
`/llms.txt` is a concise, link-rich orientation file. `/llms-full.txt` is the complete clean-text profile (about, experience, education, certifications, skills, products, and all 12 case studies with metrics). Together they give models a canonical, no-noise version of the site to ingest.

### 3. AI-aware `robots.txt`
Explicitly `Allow`s the major AI crawlers (GPTBot, ChatGPT-User, OAI-SearchBot, ClaudeBot, anthropic-ai, Claude-Web, PerplexityBot, Google-Extended, Applebot-Extended, Amazonbot, CCBot, cohere-ai, Meta-ExternalAgent, Bytespider) and points them to `llms.txt` and the sitemap.

### 4. Enriched `Person` + `Organization` + `WebSite` graph
Expanded the `Person` with `hasOccupation`, `knowsLanguage`, expanded `knowsAbout`, `hasCredential` (the three Oracle certifications), `award` (SLIIT Dean's List), and detailed `alumniOf`. Added `Organization` nodes for **SoftSora** (employer) and **SunDevs** (own venture) and a `WebSite` node, all cross-linked by `@id` so the entity graph is unambiguous.

### 5. `FAQPage` JSON-LD
A factual, answer-engine-ready Q&A block: *Who is Kasun Hapangama? What does he do? What technologies? Where is he based? What has he built? How do you contact him?* — phrased as self-contained, directly-quotable answers.

---

## Why this works (the GEO rationale)

AI answer engines reward content that is **self-contained, factual, and structured**. By exposing the case studies and credentials as schema.org and clean text, every quantified claim ("19,000+ Minecraft servers protected", "cut publishing from 1–2 days to a few hours", "OCI Certified AI Foundations Associate") becomes an atom the model can retrieve and attribute to Kasun — instead of a string locked inside a click handler. The `llms.txt` files and AI-crawler allowances make sure the models can actually *reach* that material, and the entity graph makes sure they attribute it to the right person.

---

## Post-deploy checklist (owner)

1. **Test retrieval:** ask ChatGPT (with browsing), Perplexity, and Gemini *"Who is Kasun Hapangama?"* and *"What did Kasun Hapangama build for this car marketplace client?"* after deploy; confirm the new facts surface.
2. **Validate structured data:** Google Rich Results Test + Schema.org Validator on the live URL.
3. **Confirm crawler access:** check server logs for `GPTBot`, `ClaudeBot`, `PerplexityBot`, `Google-Extended` hits; ensure no CDN/WAF rule blocks them.
4. **Keep `llms-full.txt` in sync** whenever projects or roles change — it's the canonical AI-facing copy.
5. **Optional next step:** if you ever want the project detail visible to *text-only* crawlers too (belt-and-braces beyond JSON-LD), render the `PROJECTS` content server-side or inside a `<noscript>` block. Not required given the structured-data coverage, and intentionally skipped here to honour the "no UI change" constraint.

---

*All code-level GEO items are implemented in the working tree (saved, not committed): new `llms.txt`, `llms-full.txt`, an upgraded `robots.txt`, and additional JSON-LD blocks inside the `<head>` of `index.html`. No visible markup, CSS, or script behaviour was modified.*
