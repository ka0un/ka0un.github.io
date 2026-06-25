// build-min.mjs — OPTIONAL. Emit a minified index.min.html while keeping the
// hand-formatted index.html as the readable source of truth. Deploy the .min
// version if you want the last few KB before compression; brotli/gzip (see
// deploy/nginx.conf) already removes most of the whitespace cost on the wire.
//
// Setup once:  npm install --no-save html-minifier-terser
// Run:         node tools/build-min.mjs
//
// Settings are deliberately conservative so the rendered page is byte-identical:
//  - conservativeCollapse keeps a single space, so spacing between inline
//    elements (tags, eyebrows) is preserved.
//  - caseSensitive preserves SVG / camelCase attributes (viewBox, etc.).
//  - minifyJS/minifyCSS use terser + clean-css on the inline blocks.
//  - JSON-LD lives in <script type="application/ld+json"> and is left intact.
import { minify } from "html-minifier-terser";
import { readFileSync, writeFileSync, statSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";

const ROOT = dirname(dirname(fileURLToPath(import.meta.url)));
const SRC = join(ROOT, "index.html");
const OUT = join(ROOT, "index.min.html");

const html = readFileSync(SRC, "utf8");
const min = await minify(html, {
  collapseWhitespace: true,
  conservativeCollapse: true,   // never collapse to zero — keep inline spacing
  removeComments: true,         // drops HTML comments only (JSON-LD is untouched)
  minifyCSS: true,
  minifyJS: true,
  caseSensitive: true,          // keep SVG attribute casing
  keepClosingSlash: true,
  removeAttributeQuotes: false,
  sortAttributes: false,
  sortClassName: false,
});
writeFileSync(OUT, min);

const kb = (p) => (statSync(p).size / 1024).toFixed(1) + " KB";
console.log(`index.html      ${kb(SRC)}`);
console.log(`index.min.html  ${kb(OUT)}   (${(100 * (1 - statSync(OUT).size / statSync(SRC).size)).toFixed(0)}% smaller, before brotli/gzip)`);
