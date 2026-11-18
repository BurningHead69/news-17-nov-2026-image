"""Draw the 17 November 2026 world-news summary as one 1024x1024 PNG.

Newspaper front-page layout, drawn with Pillow only: flat illustrations,
big serif headlines, short decks. No network, no randomness, no clock:
running this twice writes byte-identical output. Every illustration is
drawn on its own layer and pasted, so nothing can spill over a panel edge,
and every text block is sized to fit inside its panel.

Stories (all reported on Tuesday 17 November 2026):
  hero   US strikes Iran / tanker burning in the Strait of Hormuz
  panel  Ukraine hits the Crimean Bridge; Zaporizhzhia strike kills 40
  panel  Winter rain floods Gaza shelters; UN warns crisis worsens
  panel  COP31 draft: faster fossil-fuel phase-out, $120bn climate finance
  panel  Trump, Xi and Putin to meet Thursday in Shenzhen
  strip  US loses measles-free status; Wall Street falls; Japan scrambles jets;
         India beat Pakistan in the U-19 Asia Cup final
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (248, 243, 230)
INK = (22, 20, 17)
RED = (180, 35, 24)
NAVY = (22, 50, 79)
GOLD = (201, 138, 27)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, f, max_w):
    words, lines, cur = text.split(), [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=f) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(d, x, y, text, f, fill, max_w, lh):
    for line in wrap(d, text, f, max_w):
        d.text((x, y), line, font=f, fill=fill)
        y += lh
    return y


def rule(d, x, y, w, width=2, fill=INK):
    d.line([(x, y), (x + w, y)], fill=fill, width=width)


def paste_illo(img, fn, x, y, w, h):
    """Draw fn on its own layer, then paste: clipped to the box, never over."""
    layer = Image.new("RGB", (w, h), PAPER)
    fn(ImageDraw.Draw(layer), 0, 0, w, h)
    img.paste(layer, (x, y))


# ---------------------------------------------------------------- illustrations

def illo_hormuz(d, x, y, w, h):
    """Dusk over the Strait of Hormuz: burning tanker, smoke, jet overhead."""
    bands = [(18, 38, 66), (38, 58, 84), (94, 70, 66), (196, 110, 52), (232, 150, 70)]
    bh = h * 0.55 / len(bands)
    for i, c in enumerate(bands):
        d.rectangle([x, y + i * bh, x + w, y + (i + 1) * bh + 1], fill=c)
    hy = y + h * 0.55
    d.rectangle([x, hy, x + w, y + h], fill=(16, 54, 66))
    for i in range(5):
        yy = hy + 14 + i * 14
        d.line([(x + 20 + i * 37, yy), (x + 150 + i * 37, yy)], fill=(52, 110, 122), width=3)
    tx, ty = x + 60, hy - 52
    d.rectangle([tx, ty, tx + 330, ty + 52], fill=(12, 12, 12))
    d.rectangle([tx + 250, ty - 34, tx + 300, ty], fill=(230, 230, 220))
    for i, c in enumerate([(178, 52, 40), (201, 138, 27), (22, 90, 90)]):
        d.rectangle([tx + 20 + i * 62, ty - 26, tx + 74 + i * 62, ty], fill=c)
    fx = tx + 130
    for (dx, dy, s, c) in [(0, 0, 46, (255, 176, 32)), (-26, 12, 34, (240, 110, 30)),
                           (28, 14, 30, (240, 110, 30)), (0, -26, 30, (255, 214, 90)),
                           (-12, -8, 22, (255, 232, 150))]:
        d.ellipse([fx + dx - s // 2, ty - 46 + dy - s // 2,
                   fx + dx + s // 2, ty - 46 + dy + s // 2], fill=c)
    # two small smoke puffs that stay inside the box
    for (dx, dy, s) in [(0, -24, 26), (12, -44, 30)]:
        d.ellipse([fx + dx - s // 2, ty - 40 + dy - s // 2,
                   fx + dx + s // 2, ty - 40 + dy + s // 2], fill=(70, 66, 62))
    jx, jy = x + w - 130, y + 34
    d.polygon([(jx, jy), (jx + 72, jy + 10), (jx + 96, jy + 16), (jx + 72, jy + 20),
               (jx + 26, jy + 22), (jx + 10, jy + 30), (jx + 2, jy + 18)], fill=(10, 10, 10))
    d.line([(jx - 46, jy + 26), (jx - 6, jy + 18)], fill=(220, 220, 210), width=2)


def illo_bridge(d, x, y, w, h):
    """A bridge broken in the middle, smoke rising from the gap."""
    d.rectangle([x, y, x + w, y + h], fill=(214, 226, 232))
    d.ellipse([x + w - 96, y + 4, x + w - 26, y + 34], fill=(245, 214, 130))
    d.rectangle([x, y + h * 0.68, x + w, y + h], fill=(52, 96, 122))
    for i in range(4):
        yy = y + h * 0.72 + i * 9
        d.line([(x + 16 + i * 53, yy), (x + 130 + i * 53, yy)], fill=(120, 170, 190), width=3)
    mid = x + w // 2
    deck = y + h * 0.52
    for tx in (x + 78, x + w - 108):
        d.rectangle([tx, y + 14, tx + 14, y + h * 0.68], fill=(40, 44, 48))
    d.rectangle([x + 8, deck, mid - 42, deck + 8], fill=(40, 44, 48))
    d.rectangle([mid + 42, deck, x + w - 8, deck + 8], fill=(40, 44, 48))
    d.polygon([(mid - 42, deck + 8), (mid + 42, deck + 8),
               (mid + 18, y + h * 0.68), (mid - 18, y + h * 0.68)], fill=(90, 94, 98))
    for (dx, dy, s) in [(0, -8, 20), (12, -20, 24)]:
        d.ellipse([mid + dx - s // 2, deck + dy - s // 2,
                   mid + dx + s // 2, deck + dy + s // 2], fill=(120, 116, 110))
    d.polygon([(mid, deck - 20), (mid + 5, deck - 6), (mid + 19, deck - 5),
               (mid + 7, deck + 4), (mid + 11, deck + 17),
               (mid, deck + 9), (mid - 11, deck + 17),
               (mid - 7, deck + 4), (mid - 19, deck - 5),
               (mid - 5, deck - 6)], fill=(255, 176, 32))


def illo_gaza(d, x, y, w, h):
    """Rain over tents: grey sky, diagonal rain, three tents, puddle."""
    d.rectangle([x, y, x + w, y + h], fill=(168, 178, 184))
    for i in range(14):
        rx = x + 12 + i * 34
        d.line([(rx, y + 4), (rx - 8, y + 30)], fill=(110, 122, 130), width=2)
    gy = y + h * 0.62
    d.rectangle([x, gy, x + w, y + h], fill=(120, 104, 84))
    d.ellipse([x + 30, gy + 12, x + w - 30, gy + 24], fill=(88, 104, 118))
    th = int(h * 0.42)
    tents = [(x + 36, 92, (196, 178, 138)), (x + 176, 108, (150, 148, 132)),
             (x + 330, 92, (178, 158, 122))]
    for tx, tw, c in tents:
        d.polygon([(tx, gy), (tx + tw // 2, gy - th), (tx + tw, gy)], fill=c)
        d.line([(tx + tw // 2, gy - th), (tx + tw // 2, gy)], fill=(90, 78, 60), width=2)
        d.polygon([(tx + tw // 2 - 13, gy), (tx + tw // 2 + 13, gy),
                   (tx + tw // 2 + 7, gy - 22), (tx + tw // 2 - 7, gy - 22)],
                  fill=(40, 38, 34))


def illo_climate(d, x, y, w, h):
    """Globe with a leaf, and a rising arrow: the COP31 climate deal."""
    d.rectangle([x, y, x + w, y + h], fill=(208, 232, 224))
    cx, cy, r = x + w // 2 - 20, y + h // 2 + 6, 30
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(28, 110, 150))
    d.ellipse([cx - r + 8, cy - r + 8, cx - r + 26, cy - r + 22], fill=(74, 160, 96))
    d.ellipse([cx + 2, cy + 4, cx + 24, cy + 20], fill=(74, 160, 96))
    d.ellipse([cx - r + 14, cy + r - 18, cx - r + 30, cy + r - 6], fill=(74, 160, 96))
    lx, ly = x + w - 78, y + 8
    d.polygon([(lx, ly + 30), (lx + 15, ly), (lx + 36, ly + 20), (lx + 18, ly + 36)],
              fill=(46, 140, 70))
    d.line([(lx + 3, ly + 32), (lx + 33, ly + 4)], fill=(24, 96, 44), width=3)
    ax = x + 22
    d.line([(ax, y + h - 14), (ax + 52, y + 14)], fill=RED, width=5)
    d.polygon([(ax + 52, y + 14), (ax + 36, y + 17), (ax + 49, y + 32)], fill=RED)


def illo_summit(d, x, y, w, h):
    """Three flags side by side: United States, China, Russia."""
    d.rectangle([x, y, x + w, y + h], fill=(226, 230, 236))
    fw, fh = 118, h - 20
    top = y + 8
    ux = x + 24
    for i in range(7):
        d.rectangle([ux, top + i * (fh // 7), ux + fw, top + (i + 1) * (fh // 7) + 1],
                    fill=(178, 34, 52) if i % 2 == 0 else (245, 245, 240))
    d.rectangle([ux, top, ux + 48, top + fh * 4 // 7], fill=(28, 48, 96))
    for r in range(3):
        for c in range(4):
            d.ellipse([ux + 6 + c * 11, top + 4 + r * 10, ux + 11 + c * 11, top + 9 + r * 10],
                      fill=(245, 245, 240))
    cx = x + w // 2 - fw // 2
    d.rectangle([cx, top, cx + fw, top + fh], fill=(222, 41, 16))
    d.polygon([(cx + 16, top + 6), (cx + 20, top + 15), (cx + 29, top + 15),
               (cx + 22, top + 21), (cx + 25, top + 30), (cx + 16, top + 25),
               (cx + 7, top + 30), (cx + 10, top + 21), (cx + 3, top + 15),
               (cx + 12, top + 15)], fill=(255, 222, 0))
    for sx, sy in [(cx + 42, top + 10), (cx + 52, top + 18), (cx + 48, top + 32)]:
        d.ellipse([sx, sy, sx + 7, sy + 7], fill=(255, 222, 0))
    rx = x + w - 24 - fw
    for i, c in enumerate([(245, 245, 240), (0, 57, 166), (213, 0, 50)]):
        d.rectangle([rx, top + i * (fh // 3), rx + fw, top + (i + 1) * (fh // 3) + 1], fill=c)
    for fx in (ux, cx, rx):
        d.rectangle([fx, top, fx + fw, top + fh], outline=(60, 60, 60), width=2)
        d.line([(fx + fw // 2, top + fh), (fx + fw // 2, y + h - 4)], fill=(90, 86, 78), width=3)


# ---------------------------------------------------------------- layout

ILLO_H = 78


def story_panel(img, d, x, y, w, h, kicker, headline, deck, illo):
    d.rectangle([x, y, x + w, y + h], outline=INK, width=2)
    paste_illo(img, illo, x + 2, y + 2, w - 4, ILLO_H)
    ty = y + ILLO_H + 10
    d.text((x + 16, ty), kicker, font=font(SANS_B, 17), fill=RED)
    ty += 26
    ty = para(d, x + 16, ty, headline, font(SERIF_B, 23), INK, w - 32, 27)
    para(d, x + 16, ty + 4, deck, font(SANS, 17), (52, 48, 42), w - 32, 21)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx = 28

    # masthead
    d.text((mx, 26), "THE WORLD IN ONE DAY", font=font(SERIF_B, 58), fill=INK)
    rule(d, mx, 104, W - 2 * mx, width=3)
    d.text((mx, 114), "TUESDAY, 17 NOVEMBER 2026  •  THE DAY'S WORLD NEWS IN ONE IMAGE",
           font=font(SANS_B, 21), fill=RED)
    rule(d, mx, 146, W - 2 * mx, width=2)

    # hero: illustration left, headline right
    hx, hy, hw, hh = mx, 158, W - 2 * mx, 280
    d.rectangle([hx, hy, hx + hw, hy + hh], outline=INK, width=2)
    paste_illo(img, illo_hormuz, hx + 2, hy + 2, 480, hh - 4)
    tx = hx + 504
    tw = hw - 504 - 20
    d.text((tx, hy + 16), "THE GULF — WAR ESCALATES", font=font(SANS_B, 19), fill=RED)
    y = para(d, tx, hy + 44, "U.S. STRIKES IRAN AS TANKER BURNS IN HORMUZ",
             font(SERIF_B, 38), INK, tw, 45)
    para(d, tx, y + 10,
         "A fourth tanker is hit by a mine in a day. U.S. jets hit a missile site "
         "on Qeshm Island. Oman evacuates 24 seafarers.",
         font(SANS, 20), (52, 48, 42), tw, 26)

    # row 2
    y2, rh2 = 450, 252
    pw = (W - 2 * mx - 24) // 2
    story_panel(img, d, mx, y2, pw, rh2, "UKRAINE",
                "UKRAINE HITS CRIMEA BRIDGE; ZAPORIZHZHIA STRUCK",
                "Russian strike kills 40 in Zaporizhzhia; a school aid centre hit, 26 dead.",
                illo_bridge)
    story_panel(img, d, mx + pw + 24, y2, pw, rh2, "GAZA",
                "WINTER RAIN FLOODS GAZA SHELTERS",
                "UN warns the shelter, food and sanitation crisis is worsening.",
                illo_gaza)

    # row 3
    y3, rh3 = 714, 226
    story_panel(img, d, mx, y3, pw, rh3, "CLIMATE — COP31, ANTALYA",
                "DRAFT DEAL: QUIT FOSSIL FUELS FASTER",
                "Deal would raise climate finance for developing nations "
                "to $120bn a year by 2035.",
                illo_climate)
    story_panel(img, d, mx + pw + 24, y3, pw, rh3, "DIPLOMACY",
                "TRUMP, XI AND PUTIN TO MEET IN SHENZHEN",
                "First trilateral summit of the three leaders, Thursday at APEC.",
                illo_summit)

    # bottom strip
    sy = 952
    rule(d, mx, sy, W - 2 * mx, width=2)
    para(d, mx, sy + 10,
         "ALSO ON 17 NOV:  U.S. loses measles-free status  •  Wall Street falls  •  "
         "Japan scrambles jets  •  India win U-19 Asia Cup final",
         font(SANS_B, 18), INK, W - 2 * mx, 24)

    img.save("entry.png", optimize=True)


if __name__ == "__main__":
    main()
