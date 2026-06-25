#!/usr/bin/env python3
"""
optimize-images.py  —  next-gen responsive image pipeline for kasun.hapangama.com

Generates AVIF + WebP (and responsive widths where it matters) next to the
original JPG/PNG, and recompresses a few oversized originals in place. The
original file is always kept as the universal <img> fallback, so old browsers
keep working (see compatibility-analysis.md).

Usage:
    python3 tools/optimize-images.py <group>
    groups: hero team covers moments smalls recompress all

Re-runnable: skips a derivative if it is newer than its source unless --force.
Requires Pillow >= 11 with AVIF support (check: python3 -c "from PIL import features; print(features.check('avif'))").
"""
import os, sys, time
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FORCE = "--force" in sys.argv

AVIF_Q = 55     # AVIF quality (visually ~= JPEG q85, far smaller)
AVIF_SPEED = 6  # 0=slowest/best .. 10=fastest
WEBP_Q  = 78
JPEG_Q  = 82

# --- responsive images: source -> list of output widths (px) -------------
RESPONSIVE = {
    "assets/web/hero.jpg":                       [640, 960, 1209],
    "assets/web/team.jpg":                       [600, 1000],
    "assets/images/sundevs/SunGuard Cover.png":  [760, 1140],
    "assets/images/sundevs/SunPaste Cover.png":  [760, 1140],
    "assets/images/sundevs/SunLinks Cover.png":  [760, 1140],
}

# --- single next-gen size at native (capped) -----------------------------
MOMENTS = ["assets/web/moments/m%d.jpg" % i for i in range(1, 17)]
SMALLS  = [
    "assets/web/badges/oca-java.png", "assets/web/badges/oci-found.png",
    "assets/web/creds/cert-oca-java-t.jpg", "assets/web/creds/cert-oci-ai-t.jpg",
    "assets/web/creds/cert-oci-found-t.jpg", "assets/web/creds/award-cert-t.jpg",
    "assets/web/creds/award-stage-t.jpg",
]
SINGLE_CAP = 1000  # cap native width for single-size next-gen outputs

# --- recompress original in place (lightbox on-demand targets) -----------
RECOMPRESS = [
    "assets/web/creds/award-cert.jpg", "assets/web/creds/award-stage.jpg",
    "assets/web/creds/cert-oca-java.jpg", "assets/web/creds/cert-oci-ai.jpg",
    "assets/web/creds/cert-oci-found.jpg",
    "assets/images/SLIIT_Y2S2_DEanlist/1768031313342.jpeg",
]
# downscale these PNG fallbacks in place to this max width (covers are 1900px)
DOWNSCALE_FALLBACK = {
    "assets/images/sundevs/SunGuard Cover.png": 1140,
    "assets/images/sundevs/SunPaste Cover.png": 1140,
    "assets/images/sundevs/SunLinks Cover.png": 1140,
}
RECOMPRESS_FALLBACK = {  # re-encode JPG fallback in place at this max width
    "assets/web/hero.jpg": 1209,
    "assets/web/team.jpg": 1000,
}

saved = {"orig": 0, "new": 0}

def kb(n): return "%6.0f KB" % (n / 1024.0)

def _open(src):
    im = Image.open(src)
    im.load()
    return im

def _resized(im, width):
    if width and im.width > width:
        h = round(im.height * width / im.width)
        return im.resize((width, h), Image.LANCZOS)
    return im

def _newer(out, src):
    return (not FORCE) and os.path.exists(out) and os.path.getmtime(out) >= os.path.getmtime(src)

def emit(im, out, kind):
    if kind == "avif":
        im.save(out, format="AVIF", quality=AVIF_Q, speed=AVIF_SPEED)
    elif kind == "webp":
        im.save(out, format="WEBP", quality=WEBP_Q, method=6)
    elif kind == "jpg":
        im.convert("RGB").save(out, format="JPEG", quality=JPEG_Q, optimize=True, progressive=True)
    elif kind == "png":
        im.save(out, format="PNG", optimize=True)

def gen_nextgen(src, widths=None):
    """Generate .avif/.webp (suffixed by width if widths given) beside src."""
    full = os.path.join(ROOT, src)
    if not os.path.exists(full):
        print("  MISSING:", src); return
    im = _open(full)
    base, _ = os.path.splitext(full)
    targets = [(w, "-%d" % w) for w in widths] if widths else [(None, "")]
    for w, suf in targets:
        rim = _resized(im, w)
        for kind in ("avif", "webp"):
            out = base + suf + "." + kind
            if _newer(out, full):
                continue
            emit(rim, out, kind)
            print("  +", kb(os.path.getsize(out)), os.path.relpath(out, ROOT))

def recompress_inplace(src, maxw=None, kind=None):
    import io
    full = os.path.join(ROOT, src)
    if not os.path.exists(full):
        print("  MISSING:", src); return
    before = os.path.getsize(full)
    im = _resized(_open(full), maxw)
    ext = os.path.splitext(full)[1].lower()
    k = kind or ("png" if ext == ".png" else "jpg")
    buf = io.BytesIO()
    if k == "png":
        im.save(buf, format="PNG", optimize=True)
    elif k == "jpg":
        im.convert("RGB").save(buf, format="JPEG", quality=JPEG_Q, optimize=True, progressive=True)
    after = buf.tell()
    if after >= before:                      # never let the fallback get bigger
        print("  =", kb(before), "kept original (re-encode was larger)", src)
        saved["orig"] += before; saved["new"] += before
        return
    with open(full, "wb") as fh:
        fh.write(buf.getvalue())
    saved["orig"] += before; saved["new"] += after
    print("  ~", kb(before), "->", kb(after), src)

def run(group):
    t = time.time()
    if group in ("hero", "all"):
        print("[hero]");  gen_nextgen("assets/web/hero.jpg", RESPONSIVE["assets/web/hero.jpg"])
        recompress_inplace("assets/web/hero.jpg", RECOMPRESS_FALLBACK["assets/web/hero.jpg"])
    if group in ("team", "all"):
        print("[team]");  gen_nextgen("assets/web/team.jpg", RESPONSIVE["assets/web/team.jpg"])
        recompress_inplace("assets/web/team.jpg", RECOMPRESS_FALLBACK["assets/web/team.jpg"])
    if group in ("covers", "all"):
        print("[covers]")
        for s in DOWNSCALE_FALLBACK:
            gen_nextgen(s, RESPONSIVE[s])
            recompress_inplace(s, DOWNSCALE_FALLBACK[s])   # shrink the PNG fallback too
    if group in ("moments", "all"):
        print("[moments]")
        for s in MOMENTS: gen_nextgen(s)            # single next-gen size
    if group in ("smalls", "all"):
        print("[smalls: badges + cred thumbs]")
        for s in SMALLS: gen_nextgen(s)
    if group in ("recompress", "all"):
        print("[recompress lightbox originals]")
        for s in RECOMPRESS: recompress_inplace(s, 1200)
    print("-- %s done in %.1fs --" % (group, time.time() - t))
    if saved["orig"]:
        print("   in-place originals: %s -> %s (%.0f%% smaller)" %
              (kb(saved["orig"]), kb(saved["new"]), 100*(1-saved["new"]/saved["orig"])))

if __name__ == "__main__":
    run(sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("-") else "all")
