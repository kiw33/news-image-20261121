#!/usr/bin/env python3
"""Draw the 21 November 2026 world-news image.

A newspaper-style front page: masthead, six story panels with flat
pictograms, and an "Also today" ticker. Rendered with Pillow and the
DejaVu fonts. No network, no randomness, no clock: running the script
twice writes byte-identical PNG output.
"""

import math
import os

from PIL import Image, ImageDraw, ImageFont

CANVAS_W = 1024
CANVAS_H = 1024
EDGE = 28

PAPER = (248, 244, 236)
INK = (22, 30, 46)
MUTED = (96, 104, 116)
BODY_GREY = (56, 62, 74)
NAVY = (26, 56, 92)
CARD = (255, 255, 255)
CARD_LINE = (203, 199, 187)
RED = (176, 42, 34)
TEAL = (16, 120, 104)
GOLD = (194, 138, 26)
SKY = (62, 128, 182)
ORANGE = (212, 108, 28)
GREEN = (46, 128, 66)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def load_font(filename, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, filename), size)


KICKER_FONT = load_font("DejaVuSans-Bold.ttf", 21)
TITLE_FONT = load_font("DejaVuSans-Bold.ttf", 54)
SUB_FONT = load_font("DejaVuSans.ttf", 22)
TAG_FONT = load_font("DejaVuSans-Bold.ttf", 19)
HEAD_FONT = load_font("DejaVuSans-Bold.ttf", 25)
BODY_FONT = load_font("DejaVuSans.ttf", 19)
TICK_FONT = load_font("DejaVuSans.ttf", 18)
TICK_BOLD = load_font("DejaVuSans-Bold.ttf", 18)


def fit_lines(text, font, max_width, draw):
    """Greedy word wrap returning lines that fit max_width."""
    lines = []
    current = ""
    for word in text.split():
        trial = word if not current else current + " " + word
        if draw.textlength(trial, font=font) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


# ---------------------------------------------------------------- icons

def icon_missile_shield(d, x, y, s, color):
    """Cruise missile streaking past a shield."""
    # Shield outline.
    d.polygon([(x + s * 0.52, y + s * 0.06), (x + s * 0.92, y + s * 0.14),
               (x + s * 0.92, y + s * 0.48), (x + s * 0.72, y + s * 0.92),
               (x + s * 0.52, y + s * 0.92), (x + s * 0.52, y + s * 0.48)],
              outline=color, width=5)
    # Star inside the shield.
    cx, cy, r = x + s * 0.72, y + s * 0.46, s * 0.13
    pts = []
    for k in range(10):
        ang = -math.pi / 2 + k * math.pi / 5
        rr = r if k % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    d.polygon(pts, fill=color)
    # Missile body, diagonal.
    d.line([x + s * 0.06, y + s * 0.78, x + s * 0.46, y + s * 0.38],
           fill=RED, width=7)
    d.polygon([(x + s * 0.46, y + s * 0.38), (x + s * 0.36, y + s * 0.34),
               (x + s * 0.40, y + s * 0.44)], fill=RED)
    d.polygon([(x + s * 0.10, y + s * 0.74), (x + s * 0.06, y + s * 0.62),
               (x + s * 0.16, y + s * 0.70)], fill=RED)
    # Flame at the tail.
    d.polygon([(x + s * 0.06, y + s * 0.78), (x - s * 0.04, y + s * 0.90),
               (x + s * 0.12, y + s * 0.86)], fill=ORANGE)


def icon_barrage(d, x, y, s, color):
    """City blocks under a starburst, with two drones above."""
    for bx, bw, bh in [(0.06, 0.24, 0.34), (0.36, 0.26, 0.48),
                       (0.68, 0.26, 0.30)]:
        d.rectangle([x + s * bx, y + s * (0.95 - bh), x + s * (bx + bw),
                     y + s * 0.95], fill=color)
        d.rectangle([x + s * (bx + 0.06), y + s * (0.95 - bh - 0.06),
                     x + s * (bx + bw - 0.06), y + s * (0.95 - bh)],
                    fill=color)
    cx, cy = x + s * 0.50, y + s * 0.34
    for ang in range(0, 360, 24):
        r = math.radians(ang)
        ln = s * (0.20 if ang % 72 == 0 else 0.12)
        d.line([cx, cy, cx + ln * math.cos(r), cy + ln * math.sin(r)],
               fill=GOLD, width=4)
    d.ellipse([cx - s * 0.08, cy - s * 0.08, cx + s * 0.08, cy + s * 0.08],
              fill=RED)
    # Two small drones.
    for dx, dy in [(0.12, 0.10), (0.78, 0.06)]:
        px, py = x + s * dx, y + s * dy
        d.ellipse([px, py, px + s * 0.10, py + s * 0.06], fill=INK)
        d.line([px - s * 0.05, py + s * 0.03, px + s * 0.15, py + s * 0.03],
               fill=INK, width=3)


def icon_globe_leaf(d, x, y, s, color):
    """Globe with a leaf sprouting from its top."""
    cx, cy, r = x + s * 0.50, y + s * 0.54, s * 0.38
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color, width=5)
    d.ellipse([cx - r * 0.45, cy - r, cx + r * 0.45, cy + r],
              outline=color, width=3)
    d.line([cx - r, cy, cx + r, cy], fill=color, width=3)
    d.arc([cx - r, cy - r * 0.55, cx + r, cy + r * 0.55], 200, 340,
          fill=color, width=3)
    # Leaf.
    lx, ly = x + s * 0.62, y + s * 0.10
    d.pieslice([lx, ly, lx + s * 0.30, ly + s * 0.22], 270, 90,
               fill=GREEN)
    d.line([lx + s * 0.02, ly + s * 0.20, lx + s * 0.28, ly + s * 0.04],
           fill=GREEN, width=3)


def icon_spiral_rain(d, x, y, s, color):
    """Cyclone spiral with rain and a small shelter roof."""
    cx, cy = x + s * 0.46, y + s * 0.42
    for k in range(5):
        r = s * (0.07 + k * 0.075)
        d.arc([cx - r, cy - r, cx + r, cy + r], 30 + k * 55,
              310 + k * 55, fill=color, width=4)
    for k in range(4):
        rx = x + s * (0.08 + k * 0.20)
        d.line([rx, y + s * 0.80, rx - s * 0.04, y + s * 0.96],
               fill=SKY, width=3)
    # Small house roof at lower right.
    hx, hy = x + s * 0.68, y + s * 0.82
    d.polygon([(hx, hy), (hx + s * 0.26, hy), (hx + s * 0.13, hy - s * 0.12)],
              fill=ORANGE)


def icon_kremlin(d, x, y, s, color):
    """Three onion-domed towers with a flag."""
    for tx, tw, th in [(0.08, 0.20, 0.55), (0.38, 0.24, 0.68),
                       (0.70, 0.20, 0.50)]:
        bx0, by0 = x + s * tx, y + s * (0.95 - th)
        d.rectangle([bx0, by0, bx0 + s * tw, y + s * 0.95], fill=color)
        d.ellipse([bx0 - s * 0.03, by0 - s * 0.20, bx0 + s * tw + s * 0.03,
                   by0 + s * 0.06], fill=GOLD)
        d.line([bx0 + s * tw / 2, by0 - s * 0.20, bx0 + s * tw / 2,
                by0 - s * 0.32], fill=color, width=3)
    # Flag on the middle tower.
    fx = x + s * 0.50
    fy = y + s * (0.95 - 0.68) - s * 0.32
    d.polygon([(fx, fy), (fx + s * 0.18, fy + s * 0.04),
               (fx, fy + s * 0.09)], fill=RED)


def icon_broken_lock(d, x, y, s, color):
    """Padlock with a snapped shackle and a warning bolt."""
    d.arc([x + s * 0.30, y + s * 0.08, x + s * 0.70, y + s * 0.48],
          180, 330, fill=color, width=6)
    d.line([x + s * 0.70, y + s * 0.30, x + s * 0.86, y + s * 0.14],
           fill=color, width=6)
    d.rounded_rectangle([x + s * 0.20, y + s * 0.44, x + s * 0.80,
                         y + s * 0.92], radius=8, fill=color)
    # Keyhole bolt.
    d.polygon([(x + s * 0.52, y + s * 0.52), (x + s * 0.44, y + s * 0.70),
               (x + s * 0.56, y + s * 0.70)], fill=GOLD)
    d.rectangle([x + s * 0.48, y + s * 0.68, x + s * 0.52, y + s * 0.82],
                fill=GOLD)
    # Small warning triangle.
    tx, ty = x + s * 0.78, y + s * 0.80
    d.polygon([(tx, ty - s * 0.10), (tx + s * 0.10, ty + s * 0.08),
               (tx - s * 0.10, ty + s * 0.08)], fill=ORANGE)


ICONS = {
    "missile": icon_missile_shield,
    "barrage": icon_barrage,
    "globe": icon_globe_leaf,
    "spiral": icon_spiral_rain,
    "kremlin": icon_kremlin,
    "lock": icon_broken_lock,
}

STORIES = [
    ("POLAND", "Russian missile lands in Poland", RED,
     "A Kh-101 missile crashes near Nowy Lipowiec; PM Tusk calls it an "
     "\u201cintentional provocation\u201d. NATO jets scramble.", "missile"),
    ("UKRAINE", "Russia\u2019s overnight barrage kills 8", NAVY,
     "400+ drones and 110 missiles hit Ukraine; Kryvyi Rih counts 2 dead, "
     "42 hurt; Kyiv bridges and a Lviv station are hit.", "barrage"),
    ("ANTALYA", "COP31 talks spill into overtime", TEAL,
     "The draft drops every mention of fossil fuels; Panama threatens to "
     "block a weak text as talks run into Saturday.", "globe"),
    ("ODISHA", "Akvan weakens after landfall", SKY,
     "The cyclone crosses near Gopalpur at 70\u201380 km/h; 3.7 lakh people "
     "were evacuated and no deaths are reported.", "spiral"),
    ("PARIS", "Europe ready for Moscow talks", GOLD,
     "France says European leaders will go to Moscow if given a full role "
     "in Ukraine talks; Russia readies an E3 meeting.", "kremlin"),
    ("NEW YORK", "Banks hit in vendor data breach", ORANGE,
     "JPMorgan, Visa and Mastercard confirm vendor breaches after the N0n "
     "gang\u2019s claims; 16,000+ emails leak, cards safe.", "lock"),
]

TICKER = ("ALSO TODAY  \u2022  US approved ~879,000 AI chips for China, "
          "House panel says  \u2022  Pentagon: Iran war has cost $48.3bn  "
          "\u2022  WSJ: US floated NATO membership for Ukraine for Donbas  "
          "\u2022  India 159/1 at stumps in Wellington after Nicholls 175*  "
          "\u2022  Sensex up ~898 points  \u2022  Hyundai unveils 2027 "
          "Elantra")


def draw_panel(d, x, y, w, h, story):
    tag, headline, accent, body, icon = story
    d.rectangle([x, y, x + w, y + h], fill=CARD, outline=CARD_LINE, width=2)
    d.rectangle([x, y, x + w, y + 8], fill=accent)
    ICONS[icon](d, x + 16, y + 30, 104, accent)
    tx = x + 134
    tw = w - 134 - 18
    d.text((tx, y + 24), tag, font=TAG_FONT, fill=accent)
    lines = fit_lines(headline, HEAD_FONT, tw, d)
    ly = y + 52
    for line in lines[:2]:
        d.text((tx, ly), line, font=HEAD_FONT, fill=INK)
        ly += 31
    blines = fit_lines(body, BODY_FONT, tw, d)
    by = ly + 8
    for line in blines[:4]:
        d.text((tx, by), line, font=BODY_FONT, fill=BODY_GREY)
        by += 25


def main():
    img = Image.new("RGB", (CANVAS_W, CANVAS_H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, CANVAS_W, 10], fill=NAVY)
    d.text((EDGE, 30), "THE WORLD IN ONE IMAGE", font=KICKER_FONT, fill=NAVY)
    d.text((EDGE, 62), "SATURDAY 21 NOVEMBER 2026", font=TITLE_FONT, fill=INK)
    d.text((EDGE, 132),
           "Six stories that defined the day \u2014 from Poland to Antalya",
           font=SUB_FONT, fill=MUTED)
    d.line([EDGE, 166, CANVAS_W - EDGE, 166], fill=INK, width=3)

    gx, gy = EDGE, 182
    pw = (CANVAS_W - 2 * EDGE - 16) // 2
    ph = 234
    for i, story in enumerate(STORIES):
        px = gx + (i % 2) * (pw + 16)
        py = gy + (i // 2) * (ph + 14)
        draw_panel(d, px, py, pw, ph, story)

    ty = gy + 3 * ph + 2 * 14 + 12
    d.rectangle([0, ty, CANVAS_W, CANVAS_H], fill=NAVY)
    tlines = fit_lines(TICKER, TICK_FONT, CANVAS_W - 2 * EDGE, d)
    ly = ty + 13
    for line in tlines[:3]:
        d.text((EDGE, ly), line, font=TICK_FONT, fill=CARD)
        ly += 24

    here = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(here, "entry.png")
    img.save(out, format="PNG", optimize=True)


if __name__ == "__main__":
    main()
