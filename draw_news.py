"""Draw the 17 November 2026 world-news summary as one 1024x1024 PNG.

Newspaper front-page layout, drawn with Pillow only: photorealistic
illustrations (AI-generated, held in this repository as photo_*.jpg),
big serif headlines, short decks. No network, no randomness, no clock:
running this twice writes byte-identical output. Every photo is cropped
to its panel slot, so nothing can spill over a panel edge, and every text
block is sized to fit inside its panel.

Stories (all reported on Tuesday 17 November 2026):
  hero   US strikes Iran / tanker burning in the Strait of Hormuz
  panel  Ukraine hits the Crimean Bridge; Zaporizhzhia strike kills 40
  panel  Winter rain floods Gaza shelters; UN warns crisis worsens
  panel  COP31 draft: faster fossil-fuel phase-out, $120bn climate finance
  panel  Trump, Xi and Putin to meet Thursday in Shenzhen
  briefs Lebanon airstrikes; Houthi drones at a Saudi pipeline; Trump heeds
         the 'dirty-bomb' report; Oman evacuates 24 seafarers; US loses
         measles-free status; Wall Street falls; Japan scrambles jets;
         India beat Pakistan in the U-19 Asia Cup final; Depardieu admits
         sex-assault charge; UK sanctions firms blocking Gaza aid
"""

from PIL import Image, ImageDraw, ImageFont

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


def fit_photo(path, w, h, y_bias=0.5):
    """Crop a photo to the slot's aspect (vertical bias picks the band),
    then resize to the slot. Deterministic: same file, same bytes."""
    src = Image.open(path).convert("RGB")
    sw, sh = src.size
    th = int(sw * h / w)
    if th > sh:  # source narrower than the slot: crop width instead
        tw = int(sh * w / h)
        x0 = int((sw - tw) * 0.5)
        y0 = 0
    else:
        tw = sw
        x0 = 0
        y0 = int((sh - th) * y_bias)
    return src.crop((x0, y0, x0 + tw, y0 + th)).resize((w, h), Image.LANCZOS)


# ---------------------------------------------------------------- illustrations

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

PHOTO_H = 96


def story_panel(img, d, x, y, w, h, kicker, headline, deck, photo=None,
                photo_bias=0.5, illo=None):
    d.rectangle([x, y, x + w, y + h], outline=INK, width=2)
    if photo:
        img.paste(fit_photo(photo, w - 4, PHOTO_H, photo_bias), (x + 2, y + 2))
    else:
        paste_illo(img, illo, x + 2, y + 2, w - 4, PHOTO_H)
    ty = y + PHOTO_H + 8
    d.text((x + 16, ty), kicker, font=font(SANS_B, 17), fill=RED)
    ty += 26
    ty = para(d, x + 16, ty, headline, font(SERIF_B, 23), INK, w - 32, 26)
    para(d, x + 16, ty + 4, deck, font(SANS, 17), (52, 48, 42), w - 32, 20)


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

    # hero: photo left, headline right
    hx, hy, hw, hh = mx, 148, W - 2 * mx, 240
    d.rectangle([hx, hy, hx + hw, hy + hh], outline=INK, width=2)
    img.paste(fit_photo("photo_hero.jpg", 480, hh - 4), (hx + 2, hy + 2))
    tx = hx + 504
    tw = hw - 504 - 20
    d.text((tx, hy + 16), "THE GULF — WAR ESCALATES", font=font(SANS_B, 19), fill=RED)
    y = para(d, tx, hy + 44, "U.S. STRIKES IRAN AS TANKER BURNS IN HORMUZ",
             font(SERIF_B, 36), INK, tw, 43)
    para(d, tx, y + 10,
         "A fourth tanker is hit by a mine; U.S. jets strike a missile site "
         "on Qeshm Island.",
         font(SANS, 20), (52, 48, 42), tw, 26)

    # row 2
    y2, rh2 = 398, 238
    pw = (W - 2 * mx - 24) // 2
    story_panel(img, d, mx, y2, pw, rh2, "UKRAINE",
                "CRIMEA BRIDGE HIT; 40 KILLED IN ZAPORIZHZHIA",
                "Russian strike kills 40 in Zaporizhzhia; a school aid centre hit, 26 dead.",
                photo="photo_ukraine.jpg")
    story_panel(img, d, mx + pw + 24, y2, pw, rh2, "GAZA",
                "WINTER RAIN FLOODS GAZA SHELTERS",
                "UN warns the shelter, food and sanitation crisis is worsening.",
                photo="photo_gaza.jpg")

    # row 3
    y3, rh3 = 646, 238
    story_panel(img, d, mx, y3, pw, rh3, "CLIMATE — COP31, ANTALYA",
                "DRAFT DEAL: QUIT FOSSIL FUELS FASTER",
                "Deal would raise climate finance for developing nations "
                "to $120bn a year by 2035.",
                photo="photo_climate.jpg", photo_bias=0.35)
    story_panel(img, d, mx + pw + 24, y3, pw, rh3, "DIPLOMACY",
                "TRUMP, XI AND PUTIN TO MEET IN SHENZHEN",
                "First trilateral summit of the three leaders, Thursday at APEC.",
                illo=illo_summit)

    # briefs: ten more stories from the day, two columns, one line each
    by = 892
    rule(d, mx, by, W - 2 * mx, width=2)
    d.text((mx, by + 8), "AROUND THE WORLD — IN BRIEF",
           font=font(SANS_B, 19), fill=RED)
    briefs = [
        ("LEBANON", "Israeli airstrikes hit the south"),
        ("SAUDI ARABIA", "Houthi drones target a pipeline"),
        ("WASHINGTON", "Trump heeds 'dirty-bomb' report"),
        ("OMAN", "24 seafarers evacuated from burning tanker"),
        ("MEASLES", "U.S. loses elimination status"),
        ("MARKETS", "Wall Street falls as AI stocks slide"),
        ("JAPAN", "Jets scrambled as Russian planes intrude"),
        ("CRICKET", "India edge Pakistan in U-19 final"),
        ("FRANCE", "Depardieu admits sex-assault charge"),
        ("LONDON", "UK sanctions firms blocking Gaza aid"),
    ]
    lead_f, rest_f = font(SANS_B, 16), font(SANS, 16)
    for i, (place, text) in enumerate(briefs):
        col = i // 5
        row = i % 5
        bx = mx + col * (pw + 24)
        byy = by + 34 + row * 19
        lead = place + " — "
        d.text((bx, byy), lead, font=lead_f, fill=INK)
        d.text((bx + d.textlength(lead, font=lead_f), byy), text,
               font=rest_f, fill=(52, 48, 42))

    img.save("entry.png", optimize=True)


if __name__ == "__main__":
    main()
