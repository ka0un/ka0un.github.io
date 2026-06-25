#!/usr/bin/env python3
"""
wrap-pictures.py — wrap optimized <img> tags in <picture> with AVIF + WebP
sources, keeping the ORIGINAL <img> untouched as the universal fallback.

Idempotent: skips an <img> that is already inside a <picture>.
Run from repo root:  python3 tools/wrap-pictures.py
"""
import re, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HTML = os.path.join(ROOT, "index.html")

# responsive: html-src -> (widths, sizes)
RESP = {
    "assets/web/hero.jpg":                          ([640, 960, 1209], "100vw"),
    "assets/web/team.jpg":                          ([600, 1000],      "(max-width:900px) 92vw, 490px"),
    "assets/images/sundevs/SunGuard%20Cover.png":   ([760, 1140],      "(max-width:760px) 92vw, 560px"),
    "assets/images/sundevs/SunPaste%20Cover.png":   ([760, 1140],      "(max-width:760px) 92vw, 560px"),
    "assets/images/sundevs/SunLinks%20Cover.png":   ([760, 1140],      "(max-width:760px) 92vw, 560px"),
}
# single next-gen size (no width descriptors)
SINGLE = (["assets/web/moments/m%d.jpg" % i for i in range(1, 17)] + [
    "assets/web/badges/oca-java.png", "assets/web/badges/oci-found.png",
    "assets/web/creds/cert-oca-java-t.jpg", "assets/web/creds/cert-oci-ai-t.jpg",
    "assets/web/creds/cert-oci-found-t.jpg", "assets/web/creds/award-cert-t.jpg",
    "assets/web/creds/award-stage-t.jpg",
    "assets/thumbs/SLIIT_Y2S2_DEanlist/1768031313342.jpg",
])

def base(src):  # strip extension, keep %20 etc.
    return src.rsplit(".", 1)[0]

def wrap_one(html, src, widths, sizes):
    pat = re.compile(r'<img\b[^>]*\bsrc="' + re.escape(src) + r'"[^>]*>')
    out, pos, n = [], 0, 0
    for m in pat.finditer(html):
        before = html[max(0, m.start() - 300):m.start()]
        if "<picture>" in before and "</picture>" not in before:
            continue  # already wrapped
        b = base(src)
        if widths:
            av = ", ".join("%s-%d.avif %dw" % (b, w, w) for w in widths)
            wp = ", ".join("%s-%d.webp %dw" % (b, w, w) for w in widths)
            sz = ' sizes="%s"' % sizes
        else:
            av, wp, sz = b + ".avif", b + ".webp", ""
        sources = ('<source type="image/avif" srcset="%s"%s>'
                   '<source type="image/webp" srcset="%s"%s>' % (av, sz, wp, sz))
        out.append(html[pos:m.start()])
        out.append("<picture>" + sources + m.group(0) + "</picture>")
        pos = m.end(); n += 1
    out.append(html[pos:])
    return "".join(out), n

def main():
    html = open(HTML, encoding="utf-8").read()
    total = 0; missing = []
    for src, (widths, sizes) in RESP.items():
        html, n = wrap_one(html, src, widths, sizes)
        total += n
        if n == 0: missing.append(src)
    for src in SINGLE:
        html, n = wrap_one(html, src, None, None)
        total += n
        if n == 0: missing.append(src)
    open(HTML, "w", encoding="utf-8").write(html)
    print("Wrapped %d <img> tags in <picture>." % total)
    print("Total <picture> in file now:", html.count("<picture>"))
    if missing:
        print("WARNING — not found / already wrapped:")
        for s in missing: print("   ", s)

if __name__ == "__main__":
    main()
