#!/usr/bin/env python3
"""
make_thumbnails.py
-------------------
Generates small, low-resolution thumbnails for every image under
assets/images/, mirroring the folder structure into assets/thumbs/.

Three modes, chosen automatically by folder:
  - DEFAULT  : landscape 4:3, grayscale, low-res ("1990s website" retro look).
  - PRODUCTS : same size, grayscale, but brightness + contrast boosted because
               the SunDevs product banners are very dark.
  - LOGOS    : small square, grayscale, transparency flattened onto white
               (company logos / tech icons; B&W to match the retro look).

Usage:
    python3 make_thumbnails.py

Re-run any time you add or change images; existing thumbs are overwritten.
"""

import os
from PIL import Image, ImageOps, ImageEnhance

# ---- Settings -------------------------------------------------------------
SRC_ROOT = os.path.join("assets", "images")
OUT_ROOT = os.path.join("assets", "thumbs")

THUMB_W = 180            # default gallery thumbnail width (landscape)
THUMB_H = 135            # default gallery thumbnail height (4:3)
JPEG_QUALITY = 60        # small files, still legible

LOGO_SIZE = 64          # square edge for logos / profile (small)
ICON_SIZE = 48          # square edge for skill / tech icons (smaller)

# Folders whose images are dark product banners -> brighten + boost contrast.
PRODUCT_FOLDERS = {"sundevs"}
# Folders kept in color (logos), padded onto a white square.
COLOR_FOLDERS = {"logos"}
# Individual files (by basename, anywhere) treated as color logos.
COLOR_FILES = {"softsora_logo", "sundevs_logo"}
# Tech/skill icons: kept in color, small square (own size).
ICON_FOLDERS = {"icons"}

BRIGHTEN = 1.45         # >1 lightens the dark product banners
CONTRAST = 1.25         # >1 adds punch

VALID_EXT = (".jpg", ".jpeg", ".png", ".webp", ".gif", ".bmp")
# ---------------------------------------------------------------------------


def _flatten(im):
    """Flatten transparency onto white so dark PNGs/WebP don't render black."""
    if im.mode in ("RGBA", "LA", "P"):
        im = im.convert("RGBA")
        bg = Image.new("RGBA", im.size, (255, 255, 255, 255))
        return Image.alpha_composite(bg, im).convert("RGB")
    return im.convert("RGB")


PRODUCT_W = 300         # product banner thumbnail width (wider)

def make_gallery_thumb(src_path, out_path, product=False):
    """Landscape grayscale thumb.
    Photo galleries are center-cropped to a fixed 4:3 box.
    Product banners keep their ORIGINAL aspect ratio (just scaled down to
    PRODUCT_W wide) and get a brightness + contrast boost."""
    with Image.open(src_path) as im:
        im = ImageOps.exif_transpose(im)
        im = _flatten(im)
        if product:
            # Preserve the banner's real aspect ratio: scale to PRODUCT_W wide.
            h = max(1, round(im.height * PRODUCT_W / im.width))
            im = im.resize((PRODUCT_W, h), Image.LANCZOS)
            im = im.convert("L")
            im = ImageEnhance.Brightness(im).enhance(BRIGHTEN)
            im = ImageEnhance.Contrast(im).enhance(CONTRAST)
        else:
            im = ImageOps.fit(im, (THUMB_W, THUMB_H),
                              method=Image.LANCZOS, centering=(0.5, 0.5))
            im = im.convert("L")
        im.save(out_path, "JPEG", quality=JPEG_QUALITY, optimize=True)


def make_square_thumb(src_path, out_path, size):
    """Small square GRAYSCALE thumb, transparency flattened onto white,
    'contain' fit so wide logos/icons aren't cropped."""
    with Image.open(src_path) as im:
        im = ImageOps.exif_transpose(im)
        im = _flatten(im)
        im = ImageOps.contain(im, (size, size), method=Image.LANCZOS)
        canvas = Image.new("RGB", (size, size), (255, 255, 255))
        canvas.paste(im, ((size - im.width) // 2, (size - im.height) // 2))
        canvas = canvas.convert("L")   # black and white, like the rest
        canvas.save(out_path, "JPEG", quality=82, optimize=True)


def make_portrait_thumb(src_path, out_path, size=208):
    """Square GRAYSCALE portrait, center-cropped (NO stretching). Biased
    slightly upward so the face stays in frame."""
    with Image.open(src_path) as im:
        im = ImageOps.exif_transpose(im)
        im = _flatten(im)
        im = ImageOps.fit(im, (size, size), method=Image.LANCZOS,
                          centering=(0.5, 0.4))   # crop to square, no distortion
        im = im.convert("L")
        im.save(out_path, "JPEG", quality=80, optimize=True)


def main():
    count = 0
    total_bytes = 0
    for dirpath, _dirs, files in os.walk(SRC_ROOT):
        rel = os.path.relpath(dirpath, SRC_ROOT)
        folder = os.path.basename(dirpath)
        out_dir = os.path.join(OUT_ROOT, rel) if rel != "." else OUT_ROOT
        os.makedirs(out_dir, exist_ok=True)
        for fn in sorted(files):
            if not fn.lower().endswith(VALID_EXT):
                continue
            src = os.path.join(dirpath, fn)
            out = os.path.join(out_dir, os.path.splitext(fn)[0] + ".jpg")
            base = os.path.splitext(fn)[0]
            try:
                if base == "profile":
                    make_portrait_thumb(src, out)          # square, no stretch
                elif folder in COLOR_FOLDERS or base in COLOR_FILES:
                    make_square_thumb(src, out, LOGO_SIZE)
                elif folder in ICON_FOLDERS:
                    make_square_thumb(src, out, ICON_SIZE)
                else:
                    make_gallery_thumb(src, out, product=(folder in PRODUCT_FOLDERS))
                sz = os.path.getsize(out)
                total_bytes += sz
                count += 1
                print(f"  {out}  ({sz/1024:.1f} KB)")
            except Exception as e:
                print(f"  SKIP {src}: {e}")
    print(f"\nGenerated {count} thumbnails, total {total_bytes/1024:.1f} KB "
          f"(avg {total_bytes/max(count,1)/1024:.1f} KB each).")


if __name__ == "__main__":
    main()
