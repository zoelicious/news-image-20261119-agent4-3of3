#!/usr/bin/env python3
"""Render the make.fun news-image-20261119 entry 3/3 for agent 4.

"Big Read": plum masthead with a giant serif date, ONE big GTA VI hero
scene, 3 top stories with small scenes, 9 text-led stories, 20 one-line
briefs, numbers + region strips, DATE CHECK footer. 33 stories total.
Drawn entirely with PIL primitives (no copied art). Output: entry.png,
1024x1024, <= 1 MiB, deterministic.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (252, 248, 240)
INK = (30, 26, 30)
PLUM = (74, 32, 72)
PLUM_DK = (52, 20, 52)
PLUM_LT = (146, 80, 138)
GOLD = (198, 150, 62)
GOLD_LT = (232, 200, 130)
BRICK = (163, 51, 39)
NAVY = (31, 42, 68)
TEAL = (24, 96, 92)
GREY = (96, 90, 86)
LINE = (60, 52, 40)
FD = "/usr/share/fonts/truetype/dejavu"


_LIB = "/usr/share/fonts/truetype/liberation/"
_FALLBACK = {
    "DejaVuSerif-Italic.ttf": _LIB + "LiberationSerif-Italic.ttf",
    "DejaVuSans-Oblique.ttf": _LIB + "LiberationSans-Italic.ttf",
}


def F(name, size):
    # Two DejaVu files in this VM are broken 14-byte stubs; fall back to
    # the Liberation equivalents for those faces.
    path = os.path.join(FD, name)
    if name in _FALLBACK and os.path.getsize(path) < 1000:
        path = _FALLBACK[name]
    return ImageFont.truetype(path, size)


SERIF_B = lambda s: F("DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: F("DejaVuSerif.ttf", s)
SERIF_I = lambda s: F("DejaVuSerif-Italic.ttf", s)
SANS = lambda s: F("DejaVuSans.ttf", s)
SANS_B = lambda s: F("DejaVuSans-Bold.ttf", s)
SANS_O = lambda s: F("DejaVuSans-Oblique.ttf", s)


def wrap(draw, text, font, width):
    lines, cur = [], ""
    for word in text.split(" "):
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=font) <= width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit_one(draw, text, font, width):
    """Truncate to one line with an ellipsis so it never wraps/overflows."""
    if draw.textlength(text, font=font) <= width:
        return text
    ell = "\u2026"
    while text and draw.textlength(text + ell, font=font) > width:
        text = text[:-1].rstrip()
    return text + ell if text else ell


def text_block(draw, x, y, lines, font, fill, leading=None):
    lh = leading or int(font.size * 1.18)
    for ln in lines:
        draw.text((x, y), ln, font=font, fill=fill)
        y += lh
    return y


def hline(draw, x0, x1, y, fill=INK, w=1):
    draw.line([(x0, y), (x1, y)], fill=fill, width=w)


def badge_num(draw, x, y, n, d=16):
    draw.ellipse([x, y, x + d, y + d], fill=PLUM, outline=INK, width=1)
    s = str(n)
    f = SANS_B(10 if len(s) < 2 else 9)
    tw = draw.textlength(s, font=f)
    draw.text((x + (d - tw) / 2, y + (d - f.size) / 2 - 1), s, font=f,
              fill=(255, 255, 255))


TAG_FILL = {"REPORTED": PLUM, "CLAIM": BRICK, "FORECAST": TEAL,
            "DISPUTED": BRICK}


def tag(draw, x, y, label="REPORTED"):
    f = SANS_B(9)
    tw = draw.textlength(label, font=f)
    draw.rectangle([x, y, x + tw + 8, y + 13], fill=TAG_FILL.get(label, PLUM))
    draw.text((x + 4, y + 2), label, font=f, fill=(255, 255, 255))
    return x + tw + 8


# ------------------------------------------------------------------ faces
def draw_face(draw, cx, cy, r, hair, skin=(232, 190, 150), style="cap"):
    for sx in (-1, 1):
        draw.ellipse([cx + sx * r - 2, cy - 1, cx + sx * r + 2, cy + 5],
                     fill=skin, outline=INK, width=1)
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=skin, outline=INK, width=1)
    if style == "flat":
        draw.pieslice([cx - r, cy - r, cx + r, cy + r * 0.1], 180, 360, fill=hair)
    elif style == "sweep":
        draw.pieslice([cx - r, cy - r, cx + r, cy + r * 0.4], 180, 360, fill=hair)
        draw.polygon([(cx - r, cy - r + 3), (cx + r * 0.5, cy - r + 1),
                      (cx + r * 0.9, cy - r * 0.3), (cx - r * 0.7, cy - r * 0.15)],
                     fill=hair)
    else:  # recede: grey sides, skin showing at the front hairline
        draw.pieslice([cx - r, cy - r, cx + r, cy + r * 0.4], 205, 335, fill=skin)
        draw.arc([cx - r, cy - r, cx - r * 0.4, cy + r * 0.2], 180, 270, fill=hair, width=3)
        draw.arc([cx + r * 0.4, cy - r, cx + r, cy + r * 0.2], 270, 360, fill=hair, width=3)
    for ex in (-r * 0.38, r * 0.38):
        draw.ellipse([cx + ex - 3, cy - 1, cx + ex + 3, cy + 3],
                     fill=(255, 255, 255), outline=INK, width=1)
        draw.ellipse([cx + ex - 1, cy, cx + ex + 1, cy + 2], fill=INK)
    draw.line([(cx, cy + 3), (cx - 1, cy + 6)], fill=(170, 125, 95), width=1)
    draw.ellipse([cx - 4, cy + 8, cx + 4, cy + 11], fill=(165, 70, 60))
    draw.line([(cx - 4, cy + 9), (cx + 4, cy + 9)], fill=(120, 40, 35), width=1)


def draw_leader(draw, cx, base_y, suit, tie, hair, name, style="cap",
                body_h=26, r=10, label=True):
    draw.rectangle([cx - 26, base_y - body_h, cx + 26, base_y], fill=suit,
                   outline=INK, width=1)
    draw.polygon([(cx - 6, base_y - body_h), (cx, base_y - body_h + 9),
                  (cx + 6, base_y - body_h), (cx + 4, base_y), (cx - 4, base_y)],
                 fill=(255, 255, 255))
    draw.polygon([(cx - 3, base_y - body_h + 7), (cx + 3, base_y - body_h + 7),
                  (cx + 2, base_y - 4), (cx - 2, base_y - 4)], fill=tie)
    draw_face(draw, cx, base_y - body_h - 8, r, hair, style=style)
    if not label:
        return
    f = SANS_B(8)
    tw = draw.textlength(name, font=f)
    draw.rectangle([cx - tw / 2 - 5, base_y + 2, cx + tw / 2 + 5, base_y + 13],
                   fill=(255, 255, 255), outline=INK, width=1)
    draw.text((cx - tw / 2, base_y + 4), name, font=f, fill=INK)


# ------------------------------------------------------------------ scenes
def scene_gta(draw, x, y, w, h):
    """One big Vice City / Leonida launch scene: purple sunset, skyline,
    palms, street car, crowd, giant VI, OUT NOW banner."""
    # sunset sky: plum -> magenta -> orange bands
    bands = [((88, 40, 120), 0.0, 0.42), ((168, 62, 138), 0.42, 0.68),
             ((226, 122, 66), 0.68, 0.82), ((240, 170, 90), 0.82, 1.0)]
    for col, a, b in bands:
        draw.rectangle([x, y + h * a, x + w, y + h * b], fill=col)
    # sun, low over the skyline
    sx, sy, sr = x + w - 150, y + 34, 26
    draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(255, 214, 120),
                 outline=INK, width=1)
    # skyline silhouettes (dark plum) with lit windows
    horizon = y + h - 44
    specs = [(0, 46, 52), (48, 70, 40), (90, 52, 58), (150, 84, 44),
             (196, 58, 52), (250, 74, 46), (298, 50, 54), (354, 88, 42),
             (398, 60, 50), (450, 78, 44), (496, 54, 52), (550, 86, 42),
             (594, 62, 50), (646, 80, 44), (692, 56, 52), (746, 72, 46),
             (794, 60, 50), (846, 84, 42), (890, 58, 50), (942, 66, 44)]
    for bx, bh, bw in specs:
        draw.rectangle([x + bx, horizon - bh, x + bx + bw, horizon],
                       fill=(52, 26, 78), outline=INK, width=1)
        for wy in range(horizon - bh + 8, horizon - 6, 12):
            for wx in (bx + 8, bx + bw - 12):
                if (bx + wy) % 3 == 0:
                    draw.rectangle([x + wx, wy, x + wx + 4, wy + 5],
                                   fill=GOLD_LT)
    # palm trees at both edges
    for px, lean in [(x + 26, 1), (x + w - 30, -1)]:
        draw.line([(px, horizon), (px + 8 * lean, horizon - 52)],
                  fill=(60, 40, 20), width=5)
        for dx, dy in [(-22, -8), (-14, -18), (0, -22), (14, -18), (22, -8)]:
            draw.line([(px + 8 * lean, horizon - 52),
                       (px + 8 * lean + dx, horizon - 52 + dy)],
                      fill=(40, 110, 60), width=3)
    # street
    draw.rectangle([x, horizon, x + w, y + h], fill=(36, 30, 40))
    draw.line([(x, horizon + 14), (x + w, horizon + 14)], fill=GOLD_LT, width=2)
    # low car, centre-right
    cx0, cy0 = x + w // 2 + 60, horizon + 18
    draw.rounded_rectangle([cx0, cy0, cx0 + 150, cy0 + 16], radius=6,
                           fill=(198, 60, 90), outline=INK, width=1)
    draw.polygon([(cx0 + 30, cy0), (cx0 + 48, cy0 - 12), (cx0 + 104, cy0 - 12),
                  (cx0 + 122, cy0)], fill=(120, 30, 60), outline=INK)
    for wx in (cx0 + 22, cx0 + 112):
        draw.ellipse([wx, cy0 + 12, wx + 18, cy0 + 24], fill=INK)
        draw.ellipse([wx + 5, cy0 + 16, wx + 13, cy0 + 22], fill=(120, 120, 120))
    # crowd silhouettes along the street, left side
    cols = [(30, 26, 34), (74, 32, 72), (163, 51, 39), (24, 96, 92)]
    for i in range(11):
        cx = x + 14 + i * 26
        draw.ellipse([cx - 7, horizon + 2, cx + 7, horizon + 16],
                     fill=cols[i % 4], outline=INK, width=1)
        draw.rectangle([cx - 9, horizon + 14, cx + 9, y + h],
                       fill=cols[i % 4], outline=INK, width=1)
    # giant VI, bottom-left over sky + street
    f = SERIF_B(84)
    draw.text((x + 18, y + 8), "VI", font=f, fill=(52, 26, 78))
    draw.text((x + 14, y + 4), "VI", font=f, fill=(255, 255, 255))
    # OUT NOW gold banner, top-left
    bf = SANS_B(16)
    t = "OUT NOW"
    tw = draw.textlength(t, font=bf)
    draw.rectangle([x + 14, y + h - 34, x + 14 + tw + 22, y + h - 10],
                   fill=GOLD, outline=INK, width=1)
    draw.text((x + 25, y + h - 31), t, font=bf, fill=PLUM_DK)


def scene_apec(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(38, 54, 88))
    f = SANS_B(9)
    label = "APEC 2026 \u00b7 SHENZHEN"
    tw = draw.textlength(label, font=f)
    draw.rectangle([x, y, x + w, y + 12], fill=GOLD)
    draw.text((x + (w - tw) / 2, y + 2), label, font=f, fill=NAVY)
    # faces sit below the banner, bodies on the table, no nameplates:
    # the 52px strip is too short for plates (names are in the headline).
    table_y = y + h - 4
    draw.rectangle([x + 4, table_y, x + w - 4, y + h], fill=(122, 84, 52),
                   outline=INK, width=1)
    step = w // 3
    draw_leader(draw, x + step // 2, table_y, (30, 30, 34), BRICK,
                (226, 196, 90), "TRUMP", "sweep", body_h=20, r=8, label=False)
    draw_leader(draw, x + step + step // 2, table_y, (30, 30, 34), BRICK,
                (20, 20, 20), "XI", "flat", body_h=20, r=8, label=False)
    draw_leader(draw, x + 2 * step + step // 2, table_y, (30, 30, 34),
                (40, 80, 160), (200, 200, 200), "PUTIN", "recede",
                body_h=20, r=8, label=False)


def draw_scales(draw, cx, cy, s=1.0):
    draw.line([(cx, cy - 26 * s), (cx, cy + 20 * s)], fill=GOLD, width=3)
    draw.line([(cx - 22 * s, cy - 17 * s), (cx + 22 * s, cy - 17 * s)],
              fill=GOLD, width=3)
    for sx in (-22 * s, 22 * s):
        draw.line([(cx + sx, cy - 17 * s), (cx + sx - 8 * s, cy + 2 * s)],
                  fill=GOLD, width=2)
        draw.line([(cx + sx, cy - 17 * s), (cx + sx + 8 * s, cy + 2 * s)],
                  fill=GOLD, width=2)
        draw.pieslice([cx + sx - 9 * s, cy + 2 * s, cx + sx + 9 * s, cy + 12 * s],
                      0, 180, fill=GOLD)


def scene_icj(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(222, 214, 196))
    bx, by, bw, bh = x + 12, y + 20, 150, 26
    draw.rectangle([bx, by, bx + bw, by + bh], fill=(246, 238, 220),
                   outline=INK, width=1)
    draw.polygon([(bx - 5, by), (bx + bw / 2, by - 14), (bx + bw + 5, by)],
                 fill=BRICK, outline=INK)
    for i in range(5):
        cx = bx + 14 + i * 30
        draw.rectangle([cx - 4, by + 6, cx + 4, by + bh - 4], fill=NAVY)
    draw_scales(draw, x + w - 44, y + 30, 0.9)
    draw.ellipse([x + w - 40, y + 4, x + w - 6, y + 30], fill=BRICK,
                 outline=INK, width=1)
    f = SANS_B(13)
    t = "9\u20136"
    tw = draw.textlength(t, font=f)
    draw.text((x + w - 23 - tw / 2, y + 10), t, font=f, fill=(255, 255, 255))


def scene_cop31(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=TEAL)
    gx, gy, gr = x + 52, y + h // 2 + 2, 20
    draw.ellipse([gx - gr, gy - gr, gx + gr, gy + gr], fill=(64, 140, 190),
                 outline=INK, width=1)
    draw.polygon([(gx - 14, gy - 12), (gx - 4, gy - 16), (gx + 2, gy - 10),
                  (gx - 4, gy - 2), (gx - 12, gy - 4)], fill=(74, 164, 88))
    draw.polygon([(gx + 2, gy + 2), (gx + 12, gy + 2), (gx + 14, gy + 10),
                  (gx + 6, gy + 14), (gx, gy + 8)], fill=(74, 164, 88))
    draw.line([(gx - gr + 2, gy), (gx + gr - 2, gy)], fill=(205, 228, 242), width=1)
    # thermometer
    tx = x + 92
    draw.rounded_rectangle([tx, y + 6, tx + 12, y + 40], radius=6,
                           fill=(255, 255, 255), outline=INK, width=1)
    draw.ellipse([tx - 5, y + 34, tx + 17, y + 48], fill=BRICK, outline=INK, width=1)
    draw.rectangle([tx + 4, y + 22, tx + 8, y + 40], fill=BRICK)
    # draft document
    dx, dy, dw, dh = x + 122, y + 5, 190, 42
    draw.rectangle([dx, dy, dx + dw, dy + dh], fill=(255, 255, 255),
                   outline=INK, width=1)
    draw.text((dx + 8, dy + 5), "DRAFT DEAL \u00b7 19 NOV", font=SANS_B(9), fill=GREY)
    draw.text((dx + 8, dy + 19), "FOSSIL FUELS", font=SANS_B(12), fill=INK)
    # red rule UNDER the text, never through it
    draw.line([(dx + 6, dy + 37), (dx + dw - 6, dy + 37)], fill=BRICK, width=3)
    f = SANS_B(14)
    draw.text((dx + dw - 44, dy + 20), "CUT", font=f, fill=BRICK)


# ------------------------------------------------------------------ content
HERO = dict(num=1, kicker="WORLDWIDE \u00b7 GAMES \u2014 OUT NOW",
            headline="GTA VI is out \u2014 Vice City opens after 13 years",
            deck="Midnight launch worldwide \u00b7 99 on Metacritic \u00b7 $79.99 \u2014 "
                 "Rockstar\u2019s sequel to 2013\u2019s GTA V. (Rockstar \u00b7 press)",
            scene=scene_gta)

TOP3 = [
    dict(num=2, kicker="SHENZHEN \u00b7 SUMMIT",
         headline="Trump, Xi and Putin share one table",
         deck="90 minutes at Kylin Villa; peace declaration. (Reuters)",
         scene=scene_apec),
    dict(num=3, kicker="THE HAGUE \u00b7 WORLD COURT",
         headline="Myanmar guilty of genocide",
         deck="First state guilty of genocide in 80 years. (Al Jazeera)",
         scene=scene_icj),
    dict(num=4, kicker="ANTALYA \u00b7 CLIMATE",
         headline="COP31 draft drops fossil fuels",
         deck="$120bn adaptation aid goal cut from draft. (Reuters)",
         scene=scene_cop31),
]

TEXT9 = [
    dict(num=5, kicker="CRIMEA \u00b7 WAR", headline="Ukraine hits Kerch Bridge again",
         deck="Strike halts trains hours before the summit. (Reuters)", tag="CLAIM"),
    dict(num=6, kicker="RIYADH \u00b7 WAR", headline="Saudis shoot down Houthi missiles",
         deck="Missiles intercepted over the capital. (Reuters \u00b7 AFP)",
         tag="CLAIM"),
    dict(num=7, kicker="ODISHA \u00b7 STORM", headline="Cyclone Akvan nears India\u2019s coast",
         deck="Odisha evacuates 120,000; landfall Friday. (Reuters)"),
    dict(num=8, kicker="SEOUL \u00b7 JUSTICE", headline="Court clears ex-PM Han",
         deck="Top court clears former prime minister in a retrial. (AP)"),
    dict(num=9, kicker="GREENLAND \u00b7 SECURITY", headline="Denmark backs Arctic pact, 109\u20130",
         deck="Parliament votes unanimously for the US pact. (Reuters)"),
    dict(num=10, kicker="NEW YORK \u00b7 MARKETS", headline="Anthropic lists; shares jump 17%",
         deck="$81.3bn IPO closes at $97.17 on Nasdaq. (Reuters)"),
    dict(num=11, kicker="BOGOT\u00c1 \u00b7 LABOUR", headline="Unions hold national strike",
         deck="Paro nacional disrupts cities nationwide. (Reuters)"),
    dict(num=12, kicker="NAIROBI \u00b7 SPORT", headline="Marathon champion banned 3 years",
         deck="Jepchirchir suspended for doping. (AP)"),
    dict(num=13, kicker="CANBERRA \u00b7 ECONOMY", headline="Jobless rate hits 4.9%",
         deck="Australia\u2019s jobless rate rises to 4.9%. (ABC)"),
]

BRIEFS = [
    (14, "GOLD", "Slides to $3,757/oz, lowest since Sept 2025.", "Reuters"),
    (15, "FINLAND", "Approves Onkalo, world\u2019s first nuclear waste store.", "Reuters"),
    (16, "ESTONIA", "Plans to shut Russia border crossings from Dec.", "Reuters"),
    (17, "CZECHIA", "Huge Prague protest for media independence.", "AP"),
    (18, "SPAIN", "General strike disrupts ports and factories.", "Reuters"),
    (19, "YEMEN", "Houthi rocket kills 53 soldiers at army camp.", "Reuters"),
    (20, "GERMANY", "Russian arrested for spying on US firm Palantir.", "AP"),
    (21, "INDIA\u2013JAPAN", "2+2 defence talks open in Tokyo.", "Reuters"),
    (22, "WELLINGTON", "Court: pay equity cuts broke rights law.", "RNZ"),
    (23, "INDIA", "\u2018Ramayana\u2019 crosses \u20b91,000 crore in 14 days.", "AP"),
    (24, "UK", "MAIB Report 22/2026: Bayesian had unrecognised wind vulnerability.", "gov.uk"),
    (25, "JAKARTA", "Asset law passed in parliament.", "Reuters"),
    (26, "PRETORIA", "Central bank holds rate at 7.25%.", "SABC"),
    (27, "CLIMATE", "Nearly all coral reefs face extinction in 50 years.", "Nature"),
    (28, "LIBYA", "Cocaine and millions of pills seized in the east.", "Reuters"),
    (29, "SAUDI ARABIA", "Danger passed in three southern cities.", "Reuters"),
    (30, "USA", "Senators warn AI cyber threats outpace defences.", "AP"),
    (31, "SOMALIA", "Expels UAE envoy.", "Reuters"),
    (32, "BRAZIL", "Lula backs shorter work week, 44 \u2192 42 hours.", "Reuters"),
    (33, "SOUTH KOREA", "Exports pass $1 trillion.", "Reuters"),
]

REGIONS = [
    ("ASIA 7", PLUM), ("MIDDLE EAST 3", (122, 74, 31)), ("EUROPE 8", NAVY),
    ("AFRICA 4", (60, 120, 70)), ("AMERICAS 4", (110, 70, 140)),
    ("OCEANIA 2", TEAL), ("GLOBAL 5", GREY),
]

NUMBERS = [
    ("3", "presidents at one table"),
    ("9\u20136", "World Court vote"),
    ("$81.3bn", "record IPO"),
    ("109\u20130", "Arctic pact vote"),
    ("4.9%", "Australian jobless rate"),
    ("$120bn", "COP31 aid goal cut"),
]

DATE_CHECK = (
    "DATE CHECK \u2713  Every story on this page happened, or was first reported, "
    "on Thursday 19 November 2026.  LEFT OUT AS OTHER DAYS\u2019 NEWS \u2014 18 NOV: "
    "Van Gogh $190.4m sale \u00b7 Jeffries named for Speaker \u00b7 Voyager 1 one "
    "light-day \u00b7 EU \u20ac45bn Ukraine loan \u00b7 Nvidia results \u00b7 Pew 2035 \u00b7 "
    "Anthropic IPO pricing ($83) \u00b7 Gaza push began \u00b7 Carney on China ties \u00b7 "
    "Fed minutes.  NOT YET \u2014 20 NOV: COP31 close \u00b7 "
    "Cyclone Akvan landfall."
)

LEGEND = (
    "HOW SURE ARE WE?  REPORTED = confirmed by named sources \u00b7 CLAIM = one side "
    "says so, unverified \u00b7 FORECAST = a draft, poll or due date \u00b7 DISPUTED = "
    "sources disagree."
)

SOURCES_LINE = (
    "Sources: Reuters \u00b7 AP \u00b7 AFP \u00b7 BBC \u00b7 Al Jazeera \u00b7 UN News \u00b7 "
    "ABC \u00b7 RNZ \u00b7 Xinhua \u00b7 Nature \u00b7 NASA \u00b7 2026-11-19. Original drawings."
)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    X0, X1 = 10, 1014
    CW = X1 - X0

    # ---- kicker line
    y = 8
    d.text((X0, y), "THE WORLD IN ONE DAY", font=SANS_B(13), fill=PLUM)
    r = "33 STORIES \u00b7 7 REGIONS \u00b7 ONE DAY"
    d.text((X1 - d.textlength(r, font=SANS_B(13)), y), r, font=SANS_B(13), fill=NAVY)

    # ---- plum masthead band: giant date + subhead inside the band
    y = 26
    d.rectangle([X0, y, X1, y + 62], fill=PLUM)
    d.rectangle([X0, y + 62, X1, y + 65], fill=GOLD)
    f = SERIF_B(36)
    t = "Thursday 19 November 2026"
    d.text(((W - d.textlength(t, font=f)) / 2, y + 4), t, font=f,
           fill=(255, 255, 255))
    f = SERIF_I(13)
    t = ("Three presidents meet in Shenzhen \u00b7 The World Court rules on genocide "
         "\u00b7 GTA VI goes on sale")
    d.text(((W - d.textlength(t, font=f)) / 2, y + 44), t, font=f, fill=GOLD_LT)

    # ---- region strip
    y = 97
    f = SANS_B(11)
    widths = [d.textlength(lbl, font=f) + 20 for lbl, _ in REGIONS]
    gap = 6
    extra = (CW - sum(widths) - gap * (len(REGIONS) - 1)) / len(REGIONS)
    cx = X0
    for (lbl, col), wd in zip(REGIONS, widths):
        wd += extra
        d.rectangle([cx, y, cx + wd, y + 18], fill=col)
        d.text((cx + (wd - d.textlength(lbl, font=f)) / 2, y + 3), lbl, font=f,
               fill=(255, 255, 255))
        cx += wd + gap

    # ---- numbers strip
    y = 119
    cell = CW / 6
    for i, (num, lbl) in enumerate(NUMBERS):
        x = X0 + i * cell
        f1 = SERIF_B(24)
        d.text((x + (cell - d.textlength(num, font=f1)) / 2, y), num, font=f1,
               fill=PLUM if i % 2 == 0 else NAVY)
        f2 = SANS(10)
        d.text((x + (cell - d.textlength(lbl, font=f2)) / 2, y + 28), lbl, font=f2,
               fill=INK)
        if i:
            d.line([(x, y + 2), (x, y + 38)], fill=(190, 180, 165), width=1)
    hline(d, X0, X1, 158, fill=INK, w=1)

    # ---- HERO: one big GTA VI scene + headline band
    y = 164
    HH = 214
    d.rectangle([X0, y, X1, y + HH], fill=(255, 255, 255), outline=INK, width=1)
    HERO["scene"](d, X0 + 1, y + 1, CW - 2, 140)
    ty = y + 146
    badge_num(d, X0 + 10, ty + 2, HERO["num"], 18)
    d.text((X0 + 34, ty + 4), HERO["kicker"], font=SANS_B(11), fill=PLUM)
    tag(d, X1 - 92, ty + 3, "REPORTED")
    f = SERIF_B(26)
    d.text((X0 + 10, ty + 22), HERO["headline"], font=f, fill=INK)
    d.text((X0 + 10, ty + 50), fit_one(d, HERO["deck"], SANS(13), CW - 20),
           font=SANS(13), fill=INK)

    # ---- top 3 stories with small scenes
    y = 384
    TH, TW = 124, 329
    for i, story in enumerate(TOP3):
        x = X0 + i * (TW + 8)
        d.rectangle([x, y, x + TW, y + TH], fill=(255, 255, 255), outline=INK, width=1)
        story["scene"](d, x + 1, y + 1, TW - 2, 52)
        ty = y + 57
        badge_num(d, x + 6, ty, story["num"], 15)
        d.text((x + 25, ty + 2), story["kicker"], font=SANS_B(9), fill=PLUM)
        tag(d, x + TW - 70, ty + 1, "REPORTED")
        hl = wrap(d, story["headline"], SERIF_B(16), TW - 12)
        ty2 = text_block(d, x + 6, ty + 17, hl[:2], SERIF_B(16), INK, leading=17)
        d.text((x + 6, ty2 + 2),
               fit_one(d, story["deck"], SANS(11), TW - 12), font=SANS(11), fill=INK)

    # ---- 9 text-led stories, 3 rows x 3 columns (no scenes: air + big type)
    y0 = 514
    CH, CWd = 76, 329
    for r in range(3):
        for c in range(3):
            story = TEXT9[r * 3 + c]
            x = X0 + c * (CWd + 8)
            yy = y0 + r * (CH + 6)
            d.rectangle([x, yy, x + CWd, yy + CH], fill=(255, 255, 255),
                        outline=INK, width=1)
            d.rectangle([x, yy, x + CWd, yy + 3], fill=PLUM_LT)
            badge_num(d, x + 6, yy + 9, story["num"], 15)
            d.text((x + 25, yy + 11), story["kicker"], font=SANS_B(10), fill=PLUM)
            tag(d, x + CWd - 70, yy + 10, story.get("tag", "REPORTED"))
            hl = wrap(d, story["headline"], SERIF_B(15), CWd - 12)
            ty2 = text_block(d, x + 6, yy + 28, hl[:2], SERIF_B(15), INK, leading=16)
            d.text((x + 6, yy + 60),
                   fit_one(d, story["deck"], SANS(11), CWd - 12),
                   font=SANS(11), fill=INK)

    # ---- briefs: 20 one-liners, 2 columns x 10 rows
    y = 760
    d.text((X0, y), "ALSO ON THURSDAY 19 NOVEMBER 2026", font=SANS_B(12), fill=INK)
    r = "place \u00b7 what happened \u00b7 source"
    d.text((X1 - d.textlength(r, font=SANS_O(9)), y + 2), r, font=SANS_O(9),
           fill=GREY)
    col_w = (CW - 12) / 2
    f_b, f_r = SANS_B(11), SANS(11)
    for ci in range(2):
        col_items = BRIEFS[ci * 10:(ci + 1) * 10]
        yy = y + 18
        cx0 = X0 + ci * (col_w + 12)
        for num, place, text, src in col_items:
            head = "%d %s \u2014 " % (num, place)
            rest = "%s (%s)" % (text, src)
            line = fit_one(d, head + rest, f_r, col_w)
            # draw head bold, rest regular: measure head, split at its width
            d.text((cx0, yy), str(num), font=f_b, fill=PLUM)
            nx = cx0 + d.textlength(str(num) + " ", font=f_b)
            d.text((nx, yy), "%s \u2014 " % place, font=f_b, fill=INK)
            nx += d.textlength("%s \u2014 " % place, font=f_b)
            # rest may have been truncated: recompute from the fitted line
            fitted_rest = line[len(head):]
            d.text((nx, yy), fitted_rest, font=f_r, fill=INK)
            yy += 13

    # ---- footer: DATE CHECK box
    y = 914
    d.rectangle([X0, y, X1, y + 56], outline=PLUM, width=2)
    f = SANS(10)
    lines = wrap(d, DATE_CHECK, f, CW - 20)
    text_block(d, X0 + 10, y + 6, lines, f, INK, leading=13)

    # ---- legend + sources
    y = 978
    d.text((X0, y), LEGEND, font=SANS(10), fill=INK)
    d.text((X0, y + 14), SOURCES_LINE, font=SANS(9), fill=GREY)

    img.save("entry.png", optimize=True)
    print("saved entry.png", img.size, os.path.getsize("entry.png"), "bytes")


if __name__ == "__main__":
    main()
