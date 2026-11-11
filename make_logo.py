#!/usr/bin/env python3
"""
NEW HORIZONS - Travel & Tourism
Logo generator.

Concept: a circular badge showing a golden sun rising over a deep-navy sea,
ringed in navy, paired with a wide-tracked geometric wordmark and tagline.

Renders at 3x and downsamples (LANCZOS) for clean antialiased edges.

Outputs (assets/):
  new-horizons-logo-primary.png    transparent bg, navy wordmark
  new-horizons-logo-reversed.png   navy bg, cream wordmark
  new-horizons-icon.png            square emblem-only mark
  new-horizons-logo-primary.svg    vector lockup
"""

import os
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(ROOT, "assets")
os.makedirs(OUT_DIR, exist_ok=True)

# ---------------------------------------------------------------- palette ----
NAVY     = (11, 37, 69)      # #0B2545  trust / night sky
NAVY_MID = (18, 58, 99)      # #123A63  deep water
OCEAN    = (27, 108, 168)    # #1B6CA8  sea / sky
SKY_TOP  = (20, 80, 140)     # #14508C
SKY_BOT  = (155, 215, 245)   # #9BD7F5
GOLD     = (255, 201, 60)    # #FFC93C  sunrise
CREAM    = (253, 252, 247)   # #FDFCF7
NAVY_DEEP = (6, 20, 38)      # #061426  reversed field (darker than the sea)

HEX = {
    "navy": "#0B2545", "navy_mid": "#123A63", "ocean": "#1B6CA8",
    "sky_top": "#14508C", "sky_bot": "#9BD7F5", "gold": "#FFC93C",
    "cream": "#FDFCF7",
}

# ------------------------------------------------------------------ fonts ----
FONT_PATH = "/System/Library/Fonts/Avenir Next.ttc"
F_BOLD, F_DEMI, F_MED, F_REG = 0, 2, 5, 7

# --------------------------------------------------------------- geometry ----
SS = 3                          # supersample factor
W, H = 1000, 400                # logical canvas
EMBLEM_CX, EMBLEM_CY = 190, 200
OUTER_R, RING_W = 118, 10
CONTENT_R = OUTER_R - RING_W
HORIZON_DY = OUTER_R * 0.06     # horizon sits slightly below centre
SUN_R_RATIO = 0.36
TEXT_X = 350
RIGHT_MARGIN = 55
WORDMARK = "NEW HORIZONS"
TAGLINE = "TRAVEL & TOURISM"


def F(idx, size):
    return ImageFont.truetype(FONT_PATH, max(1, int(round(size))), index=idx)


def vgradient(w, h, top, bottom):
    """Vertical linear gradient as an RGB image."""
    h = max(1, int(h))
    strip = Image.new("RGB", (1, h))
    px = strip.load()
    for y in range(h):
        t = y / max(1, h - 1)
        px[0, y] = tuple(int(round(top[i] + (bottom[i] - top[i]) * t)) for i in range(3))
    return strip.resize((int(w), h), Image.BILINEAR)


def radial_glow(diameter, color, max_alpha=100, power=2.2):
    """Soft radial falloff, returned as RGBA."""
    d = max(2, int(diameter))
    mask = Image.new("L", (d, d), 0)
    md = ImageDraw.Draw(mask)
    c = d / 2.0
    steps = 90
    for i in range(steps, 0, -1):
        t = 1.0 - (i / steps)            # 0 at rim -> 1 at centre
        a = int(max_alpha * (t ** power))
        if a <= 1:
            continue
        r = c * (i / steps)
        md.ellipse([c - r, c - r, c + r, c + r], fill=a)
    out = Image.new("RGBA", (d, d), color + (0,))
    out.putalpha(mask)
    return out


def build_emblem(scale, ring_color=NAVY):
    """Circular sun-over-sea badge. `scale` maps logical px -> device px."""
    outer = OUTER_R * scale
    ring = max(1, int(round(RING_W * scale)))
    size = int(round(outer * 2))
    cx = cy = size / 2.0
    content_r = outer - ring
    horizon = cy + outer * 0.06

    content = Image.new("RGBA", (size, size), (0, 0, 0, 0))

    # sky
    content.paste(vgradient(size, size, SKY_TOP, SKY_BOT), (0, 0))

    # sunrise glow
    gd = int(content_r * 1.55)
    glow = radial_glow(gd, GOLD, max_alpha=100, power=2.2)
    gx = int(round(cx - gd / 2.0))
    gy = int(round(horizon - gd / 2.0))
    content.alpha_composite(glow, (max(0, gx), max(0, gy)))

    d = ImageDraw.Draw(content)

    # sun disc
    sr = content_r * SUN_R_RATIO
    d.ellipse([cx - sr, horizon - sr, cx + sr, horizon + sr], fill=GOLD)

    # sea (painted last so the sun reads as *rising*)
    sea_top = int(round(horizon))
    if sea_top < size:
        content.paste(vgradient(size, size - sea_top, NAVY, NAVY_MID), (0, sea_top))

    # ripples
    for ry, rw, rt in ((0.20, 0.44, 0.022), (0.44, 0.32, 0.020), (0.68, 0.20, 0.018)):
        y = horizon + content_r * ry
        half = content_r * rw
        th = max(1.0, content_r * rt)
        d.rounded_rectangle([cx - half, y - th, cx + half, y + th],
                            radius=th, fill=SKY_BOT + (255,))

    # clip the artwork to the inner disc
    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).ellipse(
        [cx - content_r, cy - content_r, cx + content_r, cy + content_r], fill=255)
    content.putalpha(mask)

    # ring on top (outside the clip radius, so it survives)
    ImageDraw.Draw(content).ellipse(
        [cx - outer, cy - outer, cx + outer, cy + outer],
        outline=ring_color, width=ring)

    return content


# ------------------------------------------------------------ text helpers ---
def spaced_width(d, text, f, track):
    total = 0.0
    for i, ch in enumerate(text):
        total += d.textlength(ch, font=f)
        if i < len(text) - 1:
            total += track
    return total


def draw_spaced(d, x, y, text, f, fill, track):
    cur = x
    for ch in text:
        d.text((cur, y), ch, font=f, fill=fill, anchor="ls")
        cur += d.textlength(ch, font=f) + track
    return cur - track - x


def cap_height(d, f, sample="H"):
    b = d.textbbox((0, 0), sample, font=f, anchor="ls")
    return b[3] - b[1]


def fit_size(d, text, idx, target_w, track_ratio, lo=8.0, hi=400.0):
    """Largest point size whose tracked width fits target_w."""
    best = lo
    for _ in range(40):
        mid = (lo + hi) / 2.0
        f = F(idx, mid)
        if spaced_width(d, text, f, mid * track_ratio) <= target_w:
            best = mid
            lo = mid
        else:
            hi = mid
    return best


def layout_metrics(scale):
    """Compute every measurement once, in device px, so PNG and SVG agree."""
    probe = ImageDraw.Draw(Image.new("RGBA", (8, 8)))
    text_x = TEXT_X * scale
    avail = (W - TEXT_X - RIGHT_MARGIN) * scale

    ws = fit_size(probe, WORDMARK, F_BOLD, avail, 0.09)
    wf = F(F_BOLD, ws)
    wtrack = ws * 0.09
    ww = spaced_width(probe, WORDMARK, wf, wtrack)
    wch = cap_height(probe, wf)

    ts = ws * 0.34
    tf = F(F_MED, ts)
    tch = cap_height(probe, tf)
    natural = spaced_width(probe, TAGLINE, tf, 0.0)
    ttrack = (ww * 0.62 - natural) / (len(TAGLINE) - 1)
    ttrack = max(ts * 0.12, min(ttrack, ts * 0.70))
    tw = spaced_width(probe, TAGLINE, tf, ttrack)

    rule_t = max(3 * scale, wch * 0.075)
    gap_word = wch * 0.34                        # wordmark baseline -> rule top
    # rule bottom -> tagline baseline. Must include the tagline's cap height,
    # otherwise the rule sits on top of the tagline's ascenders.
    gap_rule = tch * 0.80 + tch
    span = gap_word + rule_t + gap_rule          # wordmark baseline -> tagline baseline

    by1 = (H * scale) / 2.0 - (span - wch) / 2.0  # centres the block vertically
    rule_y = by1 + gap_word
    by2 = rule_y + rule_t + gap_rule

    return dict(scale=scale, text_x=text_x, ws=ws, wf=wf, wtrack=wtrack, ww=ww,
                wch=wch, ts=ts, tf=tf, ttrack=ttrack, tw=tw, tch=tch,
                rule_t=rule_t, rule_y=rule_y, by1=by1, by2=by2)


# ---------------------------------------------------------------- builders ---
def build_lockup(filename, bg=None, word_color=NAVY, tag_color=OCEAN,
                 rule_color=GOLD, ring_color=NAVY):
    scale = SS
    img = Image.new("RGBA", (W * scale, H * scale), (0, 0, 0, 0))
    if bg is not None:
        img.paste(Image.new("RGB", (W * scale, H * scale), bg), (0, 0))

    emblem = build_emblem(scale, ring_color=ring_color)
    img.alpha_composite(emblem, (
        int(EMBLEM_CX * scale - emblem.width / 2),
        int(EMBLEM_CY * scale - emblem.height / 2)))

    m = layout_metrics(scale)
    d = ImageDraw.Draw(img)

    d.rectangle([m["text_x"], m["rule_y"], m["text_x"] + m["ww"], m["rule_y"] + m["rule_t"]],
                fill=rule_color)
    draw_spaced(d, m["text_x"], m["by1"], WORDMARK, m["wf"], word_color, m["wtrack"])
    draw_spaced(d, m["text_x"], m["by2"], TAGLINE, m["tf"], tag_color, m["ttrack"])

    out = img.resize((W, H), Image.LANCZOS)
    path = os.path.join(OUT_DIR, filename)
    out.save(path)
    return path


def build_icon(filename, size_logical=512, pad_ratio=0.055, bg=None, ring_color=NAVY):
    S = size_logical * SS
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    if bg is not None:
        img.paste(Image.new("RGB", (S, S), bg), (0, 0))
    target_d = S * (1 - 2 * pad_ratio)
    emb = build_emblem(target_d / (2 * OUTER_R), ring_color=ring_color)
    img.alpha_composite(emb, (int((S - emb.width) / 2), int((S - emb.height) / 2)))
    out = img.resize((size_logical, size_logical), Image.LANCZOS)
    path = os.path.join(OUT_DIR, filename)
    out.save(path)
    return path


def build_svg(filename="new-horizons-logo-primary.svg"):
    """Vector twin of the primary lockup, using the same computed metrics."""
    m = layout_metrics(1.0)
    cx, cy = EMBLEM_CX, EMBLEM_CY
    horizon = cy + HORIZON_DY
    sr = CONTENT_R * SUN_R_RATIO
    gd = CONTENT_R * 1.55 / 2.0
    ripples = []
    for ry, rw, rt in ((0.20, 0.44, 0.022), (0.44, 0.32, 0.020), (0.68, 0.20, 0.018)):
        y = horizon + CONTENT_R * ry
        half = CONTENT_R * rw
        ripples.append(
            f'    <rect x="{cx-half:.2f}" y="{y - CONTENT_R*rt:.2f}" '
            f'width="{2*half:.2f}" height="{2*CONTENT_R*rt:.2f}" '
            f'rx="{CONTENT_R*rt:.2f}" fill="{HEX["sky_bot"]}"/>')

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <title>New Horizons - Travel &amp; Tourism</title>
  <defs>
    <linearGradient id="nhSky" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{HEX['sky_top']}"/>
      <stop offset="1" stop-color="{HEX['sky_bot']}"/>
    </linearGradient>
    <linearGradient id="nhSea" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{HEX['navy']}"/>
      <stop offset="1" stop-color="{HEX['navy_mid']}"/>
    </linearGradient>
    <radialGradient id="nhGlow">
      <stop offset="0" stop-color="{HEX['gold']}" stop-opacity="0.72"/>
      <stop offset="1" stop-color="{HEX['gold']}" stop-opacity="0"/>
    </radialGradient>
    <clipPath id="nhDisc">
      <circle cx="{cx}" cy="{cy}" r="{CONTENT_R}"/>
    </clipPath>
  </defs>

  <!-- emblem -->
  <g clip-path="url(#nhDisc)">
    <rect x="{cx-CONTENT_R}" y="{cy-CONTENT_R}" width="{2*CONTENT_R}" height="{2*CONTENT_R}" fill="url(#nhSky)"/>
    <circle cx="{cx}" cy="{horizon:.2f}" r="{gd:.2f}" fill="url(#nhGlow)"/>
    <circle cx="{cx}" cy="{horizon:.2f}" r="{sr:.2f}" fill="{HEX['gold']}"/>
    <rect x="{cx-CONTENT_R}" y="{horizon:.2f}" width="{2*CONTENT_R}" height="{cy+CONTENT_R-horizon:.2f}" fill="url(#nhSea)"/>
{chr(10).join(ripples)}
  </g>
  <circle cx="{cx}" cy="{cy}" r="{OUTER_R - RING_W/2}" fill="none" stroke="{HEX['navy']}" stroke-width="{RING_W}"/>

  <!-- wordmark -->
  <g font-family="Avenir Next, Avenir, Helvetica Neue, Arial, sans-serif">
    <rect x="{m['text_x']:.2f}" y="{m['rule_y']:.2f}" width="{m['ww']:.2f}" height="{m['rule_t']:.2f}" fill="{HEX['gold']}"/>
    <text x="{m['text_x']:.2f}" y="{m['by1']:.2f}" font-size="{m['ws']:.2f}" font-weight="700"
          letter-spacing="{m['wtrack']:.2f}" fill="{HEX['navy']}"
          textLength="{m['ww']:.2f}" lengthAdjust="spacing">{WORDMARK}</text>
    <text x="{m['text_x']:.2f}" y="{m['by2']:.2f}" font-size="{m['ts']:.2f}" font-weight="500"
          letter-spacing="{m['ttrack']:.2f}" fill="{HEX['ocean']}"
          textLength="{m['tw']:.2f}" lengthAdjust="spacing">{TAGLINE.replace('&', '&amp;')}</text>
  </g>
</svg>
'''
    path = os.path.join(OUT_DIR, filename)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(svg)
    return path


if __name__ == "__main__":
    made = [
        build_lockup("new-horizons-logo-primary.png"),
        build_lockup("new-horizons-logo-reversed.png", bg=NAVY_DEEP, word_color=CREAM,
                     tag_color=SKY_BOT, rule_color=GOLD, ring_color=CREAM),
        build_icon("new-horizons-icon.png"),
        build_icon("new-horizons-icon-reversed.png", bg=NAVY_DEEP, ring_color=CREAM),
        build_svg(),
    ]
    probe = ImageDraw.Draw(Image.new("RGBA", (8, 8)))
    m = layout_metrics(1.0)
    print(f"wordmark size {m['ws']:.1f}px  width {m['ww']:.1f}px  cap {m['wch']:.1f}px")
    print(f"tagline  size {m['ts']:.1f}px  width {m['tw']:.1f}px  track {m['ttrack']:.1f}px")
    print(f"baselines  word {m['by1']:.1f}  tagline {m['by2']:.1f}  rule_y {m['rule_y']:.1f}")
    for p in made:
        if p.lower().endswith(".svg"):
            print("wrote", p, os.path.getsize(p), "bytes")
        else:
            im = Image.open(p)
            print("wrote", p, im.size, im.mode)
