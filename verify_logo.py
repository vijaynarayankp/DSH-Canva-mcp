#!/usr/bin/env python3
"""Independent check of the generated logo PNGs (no vision needed).

Verifies: transparent field, text inside the canvas, and that the gold rule
is vertically separated from both the wordmark and the tagline.
"""
import os
from PIL import Image

ROOT = os.path.dirname(os.path.abspath(__file__))
A = os.path.join(ROOT, "assets")

PAL = {
    (11, 37, 69): '#', (18, 58, 99): '%', (27, 108, 168): '+', (20, 80, 140): '=',
    (155, 215, 245): '-', (255, 201, 60): '@', (253, 252, 247): ' ', (255, 255, 255): ' ',
}


def cls(px):
    r, g, b, a = px
    if a < 110:
        return '.'
    best, bd = '?', 1e9
    for c, ch in PAL.items():
        dd = (r - c[0]) ** 2 + (g - c[1]) ** 2 + (b - c[2]) ** 2
        if dd < bd:
            bd, best = dd, ch
    return best


def band_report(img, x0, x1, label):
    """Print an opaque-pixel count per row across the text column range."""
    px = img.load()
    w, h = img.size
    print(f"\n--- row profile of text area x=[{x0},{x1}] : {label} ---")
    bands, run = [], None
    for y in range(h):
        n = sum(1 for x in range(x0, min(x1, w)) if px[x, y][3] > 110)
        if n:
            if run is None:
                run = [y, y]
            else:
                run[1] = y
        elif run is not None:
            bands.append(tuple(run))
            run = None
    if run:
        bands.append(tuple(run))
    for a, b in bands:
        peak = max(sum(1 for x in range(x0, min(x1, w)) if px[x, y][3] > 110)
                   for y in range(a, b + 1))
        print(f"   rows {a:3d}-{b:3d}  height {b-a+1:3d}  peak px/row {peak}")
    return bands


for name in ("new-horizons-logo-primary.png", "new-horizons-logo-reversed.png"):
    im = Image.open(os.path.join(A, name)).convert("RGBA")
    print("=" * 90)
    print(name, im.size)
    small = im.resize((100, 40), Image.BOX)
    sp = small.load()
    for y in range(40):
        print("".join(cls(sp[x, y]) for x in range(100)))

    bbox = im.getbbox()
    print("content bbox:", bbox)
    p = im.load()
    print("corner (2,2) alpha:", p[2, 2][3], " corner (997,2) alpha:", p[997, 2][3])

    bands = band_report(im, 350, 999, name)
    txt = [b for b in bands if b[0] > 120]
    if txt:
        widths = []
        for x in range(350, im.size[0]):
            if any(p[x, y][3] > 110 for y in range(0, im.size[1])):
                widths.append(x)
        print("rightmost opaque pixel in text area:", max(widths) if widths else None,
              "(canvas width %d)" % im.size[0])

# --- explicit geometry assertions on the primary lockup -----------------------
im = Image.open(os.path.join(A, "new-horizons-logo-primary.png")).convert("RGBA")
px = im.load()
w, h = im.size
rule_rows = [y for y in range(h)
             if sum(1 for x in range(0, w) if px[x, y][3] > 110) > 500]
print("\n=== assertions (primary) ===")
print("wide horizontal bands (rule):", rule_rows)
word_rows = [y for y in range(130, 260)
             if any(px[x, y][3] > 110 and px[x, y][0] < 60 for x in range(360, 900))]
tag_rows = [y for y in range(130, 300)
            if any(px[x, y][0] < 80 and px[x, y][2] > 120 for x in range(360, 900))]
print("navy wordmark rows :", (min(word_rows), max(word_rows)) if word_rows else None)
print("blue tagline rows  :", (min(tag_rows), max(tag_rows)) if tag_rows else None)
if rule_rows:
    r0, r1 = min(rule_rows), max(rule_rows)
    print(f"rule band rows     : {r0}-{r1}")
    tag_above = [y for y in tag_rows if y <= r1]
    print("tagline rows overlapping rule:", tag_above)
    print("VERDICT rule/tagline collision:",
          "YES - FIX NEEDED" if tag_above else "no")
