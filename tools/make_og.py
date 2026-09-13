#!/usr/bin/env python3
"""
Build the og:image share card for littlestjames.net.

The card is a static PNG because Discord and X fetch it with a crawler that
runs no JavaScript, so nothing on the page can influence it. The only value
on it that can drift is the server version, so this script reads the live
version from the status API and rebuilds the card ONLY when it changes.

Run locally:      python tools/make_og.py
Force a rebuild:  python tools/make_og.py --force
"""

import argparse
import json
import os
import sys
import urllib.request

from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, "assets")
FONT = os.path.join(ROOT, "fonts", "Outfit.ttf")
OUT = os.path.join(ASSETS, "og-image.png")
STATE = os.path.join(ROOT, "tools", "og-state.json")

STATUS_API = "https://api.mcstatus.io/v2/status/java/littlestjames.net"

W, H = 1200, 630
SAFE = 64          # X rounds the card's corners; keep everything inside this

GOLD = (232, 180, 76)
GOLD_SOFT = (243, 208, 138)
SAND = (239, 230, 214)
SAND_DIM = (214, 207, 194)
INK = (11, 15, 15)


# --------------------------------------------------------------------------
# data
# --------------------------------------------------------------------------

def live_version(default="26.2"):
    """Version string from the status API, or the default if unreachable."""
    try:
        req = urllib.request.Request(STATUS_API, headers={"User-Agent": "littlestjames-og/1"})
        with urllib.request.urlopen(req, timeout=20) as r:
            d = json.load(r)
        if not d.get("online"):
            return default
        v = (d.get("version") or {}).get("name_clean") or ""
        v = v.strip()
        # Ignore junk or long modded strings; they would wreck the layout.
        return v if v and len(v) <= 16 else default
    except Exception as e:
        print("  status API unreachable (%s); keeping %r" % (e.__class__.__name__, default))
        return default


def read_state():
    try:
        with open(STATE, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


# --------------------------------------------------------------------------
# drawing helpers
# --------------------------------------------------------------------------

def font(size, weight="Black"):
    f = ImageFont.truetype(FONT, size)
    try:
        f.set_variation_by_name(weight)
    except Exception:
        pass
    return f


def text_w(draw, s, f):
    return draw.textbbox((0, 0), s, font=f)[2]


def radial_glow(size, colour, peak_alpha):
    """Soft radial falloff, built small and scaled up so it stays smooth."""
    n = 96
    g = Image.new("L", (n, n), 0)
    px = g.load()
    c = (n - 1) / 2.0
    for y in range(n):
        for x in range(n):
            d = (((x - c) ** 2 + (y - c) ** 2) ** 0.5) / c
            px[x, y] = 0 if d >= 1 else int(peak_alpha * (1 - d) ** 2.2)
    g = g.resize((size, size), Image.LANCZOS)
    layer = Image.new("RGBA", (size, size), colour + (0,))
    layer.putalpha(g)
    return layer


def notched(draw, box, n, fill):
    """The site's clip-path corner cut, as a polygon."""
    x0, y0, x1, y1 = box
    draw.polygon(
        [(x0 + n, y0), (x1 - n, y0), (x1, y0 + n), (x1, y1 - n),
         (x1 - n, y1), (x0 + n, y1), (x0, y1 - n), (x0, y0 + n)],
        fill=fill,
    )


def tracked(draw, s, f, cx, y, fill, tracking):
    """Pillow has no letter-spacing, so place each glyph by hand."""
    widths = [text_w(draw, ch, f) for ch in s]
    total = sum(widths) + tracking * (len(s) - 1)
    x = cx - total / 2
    for ch, w in zip(s, widths):
        draw.text((x, y), ch, font=f, fill=fill)
        x += w + tracking
    return total


def cover(img, w, h):
    """Scale-and-crop to fill exactly w x h without distorting."""
    scale = max(w / img.width, h / img.height)
    img = img.resize((max(1, round(img.width * scale)), max(1, round(img.height * scale))), Image.LANCZOS)
    left = (img.width - w) // 2
    top = (img.height - h) // 2
    return img.crop((left, top, left + w, top + h))


# --------------------------------------------------------------------------
# the card
# --------------------------------------------------------------------------

def build(version):
    # Background: the purpose-made art if it exists, else the hero photo.
    bg_path = None
    for cand in ("og-bg.png", "og-bg.jpg", "hero.jpg"):
        p = os.path.join(ASSETS, cand)
        if os.path.exists(p):
            bg_path = p
            break
    if not bg_path:
        raise SystemExit("no background art found in assets/")
    print("  background: %s" % os.path.basename(bg_path))

    card = cover(Image.open(bg_path).convert("RGB"), W, H).convert("RGBA")

    # Readability scrim, heavier at the top where the type sits.
    scrim = Image.new("RGBA", (W, H))
    sd = ImageDraw.Draw(scrim)
    for y in range(H):
        t = y / (H - 1)
        sd.line([(0, y), (W, y)], fill=(5, 8, 8, int(225 - 95 * t)))
    card = Image.alpha_composite(card, scrim)

    glow_size = 900
    card.alpha_composite(radial_glow(glow_size, GOLD, 78), ((W - glow_size) // 2, -120))

    d = ImageDraw.Draw(card)

    # --- logo ---
    logo = Image.open(os.path.join(ASSETS, "icon.png")).convert("RGBA")
    lh = 132
    lw = round(logo.width * (lh / logo.height))
    card.alpha_composite(logo.resize((lw, lh), Image.LANCZOS), ((W - lw) // 2, 52))

    # --- wordmark: Little (cream) + StJames (gold) ---
    fw = font(78, "Black")
    a, b = "Little", "StJames"
    wa, wb = text_w(d, a, fw), text_w(d, b, fw)
    x = (W - (wa + wb)) / 2
    y = 200
    d.text((x, y), a, font=fw, fill=SAND)
    d.text((x + wa, y), b, font=fw, fill=GOLD)

    # --- JOIN NOW ---
    fj = font(23, "Bold")
    tracked(d, "JOIN NOW", fj, W / 2, 306, GOLD_SOFT, 7)

    # --- address chip ---
    fc = font(42, "Black")
    label = "LittleStJames.net"
    cw = text_w(d, label, fc)
    chip_w = cw + 96
    chip_h = 82
    cx0 = (W - chip_w) / 2
    cy0 = 344
    notched(d, (cx0, cy0, cx0 + chip_w, cy0 + chip_h), 16, GOLD)
    bbox = d.textbbox((0, 0), label, font=fc)
    d.text((cx0 + (chip_w - cw) / 2 - bbox[0],
            cy0 + (chip_h - (bbox[3] - bbox[1])) / 2 - bbox[1]),
           label, font=fc, fill=INK)

    # --- meta line, carrying the live version ---
    fm = font(24, "Bold")
    tracked(d, "JAVA EDITION  ·  SURVIVAL  ·  %s" % version,
            fm, W / 2, 476, SAND_DIM, 3)

    # --- hairline frame, inside the safe area ---
    d.rectangle([34, 34, W - 35, H - 35], outline=(232, 180, 76, 70), width=2)

    card.convert("RGB").save(OUT, "PNG", optimize=True)
    print("  wrote %s (%s bytes)" % (os.path.relpath(OUT, ROOT), os.path.getsize(OUT)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true", help="rebuild even if the version is unchanged")
    args = ap.parse_args()

    prev = read_state()
    version = live_version(default=prev.get("version", "26.2"))
    print("  live version: %s   (card was built for: %s)" % (version, prev.get("version", "never")))

    if not args.force and prev.get("version") == version and os.path.exists(OUT):
        print("  unchanged - nothing to do")
        return 0

    build(version)
    with open(STATE, "w", encoding="utf-8") as f:
        json.dump({"version": version}, f, indent=2)
        f.write("\n")
    print("  state updated")
    return 0


if __name__ == "__main__":
    sys.exit(main())
