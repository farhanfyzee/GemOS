#!/usr/bin/env python3
"""
Surah Gems — Buying Book generator.

Run `python generate.py` to emit two print-ready PDFs into ./output/:

  * SurahGems_BuyingBook_v{VERSION}_{YYYYMMDD}.pdf
        cover + the system + every numbered ledger page (one bound book).
  * SurahGems_Receipts_v{VERSION}_{YYYYMMDD}.pdf
        every supplier receipt (a separate receipt pad).

The ledger serial (SG-0001, SG-0002, ...) is one continuous, pre-printed run
that never resets. The receipt pad has its own separate run (R-0001, ...).

Fonts (Work Sans, Lora, IBM Plex Mono) are downloaded to ./fonts/ on first run
and reused thereafter; if the download fails (e.g. offline) the script falls
back to the built-in Helvetica / Times / Courier families and never crashes.
"""

import os
import sys
import subprocess
import urllib.request
from datetime import date, datetime

from reportlab.lib.pagesizes import A4, A5, landscape
from reportlab.lib.colors import HexColor, white
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# --------------------------------------------------------------------------- #
# Config block — kept at the top so variants can be versioned and diffed.
# --------------------------------------------------------------------------- #
SERIAL_PREFIX     = "SG-"
START_SERIAL      = 1
ROWS_PER_PAGE     = 10
LEDGER_PAGES      = 50        # emits SG-0001 ... SG-0500, pre-printed
RECEIPT_PAGES     = 50        # separate sequence
RECEIPT_PREFIX    = "R-"
CURRENCY_DEFAULT  = "LKR"
PAGE_SIZE         = "A5"      # A5 | A4
INCLUDE_MEMO_SLIP = False     # see Open decisions (memo / consignment slip)
PURCHASE_MODE     = "single"  # single | parcel  (see Open decisions)

VERSION = "1.0.0"

# --------------------------------------------------------------------------- #
# Palette
# --------------------------------------------------------------------------- #
NAVY     = HexColor("#1A2442")
INK      = HexColor("#1F1F22")
GREY     = HexColor("#6B6B70")
HAIRLINE = HexColor("#9E9EA3")
TINT     = HexColor("#EFEFF1")
WHITE    = white

# --------------------------------------------------------------------------- #
# Paths
# --------------------------------------------------------------------------- #
ROOT       = os.path.dirname(os.path.abspath(__file__))
FONTS_DIR  = os.path.join(ROOT, "fonts")
OUTPUT_DIR = os.path.join(ROOT, "output")

# --------------------------------------------------------------------------- #
# Fonts
# --------------------------------------------------------------------------- #
# Each face lists candidate download URLs (tried in order) and the built-in
# base-14 font to fall back on if every download fails. Primary URLs point at
# real *static* TTFs on GitHub raw; the google/fonts variable fonts are kept as
# a secondary source for the regular/italic faces.
_R = "https://raw.githubusercontent.com"
FONT_SPECS = {
    "WorkSans-Regular": (
        [f"{_R}/weiweihuanghuang/Work-Sans/master/fonts/ttf/WorkSans-Regular.ttf",
         f"{_R}/google/fonts/main/ofl/worksans/WorkSans%5Bwght%5D.ttf"],
        "Helvetica",
    ),
    "WorkSans-Bold": (
        [f"{_R}/weiweihuanghuang/Work-Sans/master/fonts/ttf/WorkSans-Bold.ttf"],
        "Helvetica-Bold",
    ),
    "Lora-Regular": (
        [f"{_R}/cyrealtype/Lora-Cyrillic/master/fonts/ttf/Lora-Regular.ttf",
         f"{_R}/google/fonts/main/ofl/lora/Lora%5Bwght%5D.ttf"],
        "Times-Roman",
    ),
    "Lora-Italic": (
        [f"{_R}/cyrealtype/Lora-Cyrillic/master/fonts/ttf/Lora-Italic.ttf",
         f"{_R}/google/fonts/main/ofl/lora/Lora-Italic%5Bwght%5D.ttf"],
        "Times-Italic",
    ),
    "IBMPlexMono-Regular": (
        [f"{_R}/google/fonts/main/ofl/ibmplexmono/IBMPlexMono-Regular.ttf"],
        "Courier",
    ),
}

# Logical font names, filled in by setup_fonts().
FONT_SANS = FONT_SANS_BOLD = FONT_SERIF = FONT_SERIF_ITALIC = FONT_MONO = None


def _download(url, dest, timeout=25):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        data = resp.read()
    if len(data) < 4 or data[:4] not in (b"\x00\x01\x00\x00", b"true", b"OTTO", b"ttcf"):
        raise ValueError("not a usable TrueType/OpenType file")
    with open(dest, "wb") as fh:
        fh.write(data)


def setup_fonts():
    """Resolve every face to a registered TTF (downloading if needed) or a
    base-14 fallback. Never raises — a font problem must not stop a build."""
    global FONT_SANS, FONT_SANS_BOLD, FONT_SERIF, FONT_SERIF_ITALIC, FONT_MONO
    os.makedirs(FONTS_DIR, exist_ok=True)
    resolved = {}
    for key, (urls, fallback) in FONT_SPECS.items():
        dest = os.path.join(FONTS_DIR, key + ".ttf")
        if not os.path.exists(dest):
            for url in urls:
                try:
                    _download(url, dest)
                    break
                except Exception:
                    continue
        name = fallback
        if os.path.exists(dest):
            try:
                pdfmetrics.registerFont(TTFont(key, dest))
                name = key
            except Exception:
                # Bad/partial file — drop it so a later run can retry.
                try:
                    os.remove(dest)
                except OSError:
                    pass
        resolved[key] = name

    FONT_SANS        = resolved["WorkSans-Regular"]
    FONT_SANS_BOLD   = resolved["WorkSans-Bold"]
    FONT_SERIF       = resolved["Lora-Regular"]
    FONT_SERIF_ITALIC = resolved["Lora-Italic"]
    FONT_MONO        = resolved["IBMPlexMono-Regular"]

    used_real = sum(1 for k, v in resolved.items() if v == k)
    if used_real == len(resolved):
        print("  fonts: Work Sans / Lora / IBM Plex Mono ready")
    elif used_real == 0:
        print("  fonts: download unavailable — using Helvetica / Times / Courier fallback")
    else:
        print(f"  fonts: {used_real}/{len(resolved)} downloaded, rest on base-14 fallback")


# --------------------------------------------------------------------------- #
# Page geometry
# --------------------------------------------------------------------------- #
_BASE = {"A5": A5, "A4": A4}.get(PAGE_SIZE, A5)
PAGE = landscape(_BASE)
PW, PH = PAGE


def serial(prefix, n):
    return f"{prefix}{n:04d}"


# --------------------------------------------------------------------------- #
# Drawing helpers
# --------------------------------------------------------------------------- #
def tracked(c, text, x, y, font, size, color, space, align="left"):
    """Draw letter-spaced ("tracked") text. Canvas has no setCharSpace, so
    glyphs are placed individually."""
    c.setFont(font, size)
    c.setFillColor(color)
    widths = [pdfmetrics.stringWidth(ch, font, size) for ch in text]
    total = sum(widths) + space * max(0, len(text) - 1)
    if align == "center":
        cur = x - total / 2
    elif align == "right":
        cur = x - total
    else:
        cur = x
    for ch, w in zip(text, widths):
        c.drawString(cur, y, ch)
        cur += w + space


def _wrap(text, font, size, max_w):
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if pdfmetrics.stringWidth(trial, font, size) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def paragraph(c, text, x, y, font, size, color, max_w, leading):
    c.setFont(font, size)
    c.setFillColor(color)
    for line in _wrap(text, font, size, max_w):
        c.drawString(x, y, line)
        y -= leading
    return y


def heading(c, text, x, y):
    tracked(c, text.upper(), x, y, FONT_SANS_BOLD, 8.5, NAVY, 1.4)
    return y - 14


def diamond(c, cx, cy, r):
    """A single small line-mark diamond — the only ornament in the whole book."""
    c.setStrokeColor(NAVY)
    c.setLineWidth(1.0)
    p = c.beginPath()
    p.moveTo(cx, cy + r)
    p.lineTo(cx + r * 0.72, cy)
    p.lineTo(cx, cy - r)
    p.lineTo(cx - r * 0.72, cy)
    p.close()
    c.drawPath(p, stroke=1, fill=0)
    c.line(cx - r * 0.72, cy, cx + r * 0.72, cy)          # girdle
    c.line(cx - r * 0.34, cy, cx, cy + r)                  # crown facet
    c.line(cx + r * 0.34, cy, cx, cy + r)                  # crown facet


def fill_page(c, color=WHITE):
    c.setFillColor(color)
    c.rect(0, 0, PW, PH, fill=1, stroke=0)


# --------------------------------------------------------------------------- #
# Page 1 — Cover
# --------------------------------------------------------------------------- #
def draw_cover(c):
    fill_page(c)
    m = 22
    c.setStrokeColor(NAVY)
    c.setLineWidth(1.2)
    c.rect(m, m, PW - 2 * m, PH - 2 * m, fill=0, stroke=1)

    cx = PW / 2
    diamond(c, cx, PH - 104, 15)
    tracked(c, "CEYLON SAPPHIRE & SPINEL", cx, PH - 146, FONT_SANS, 9, GREY, 3, "center")

    c.setFont(FONT_SANS_BOLD, 44)
    c.setFillColor(NAVY)
    c.drawCentredString(cx, PH - 198, "SURAH GEMS")

    c.setStrokeColor(HAIRLINE)
    c.setLineWidth(0.6)
    c.line(cx - 66, PH - 216, cx + 66, PH - 216)

    tracked(c, "BUYING LEDGER", cx, PH - 242, FONT_SANS, 13, INK, 4, "center")
    c.setFont(FONT_SERIF_ITALIC, 12)
    c.setFillColor(GREY)
    c.drawCentredString(cx, PH - 263, "Field record of acquisition")

    c.setFont(FONT_SERIF, 11)
    c.setFillColor(INK)
    c.drawCentredString(cx, m + 72, "Vol. ____________        Year ____________")
    tracked(c, "BERUWALA · CEYLON", cx, m + 50, FONT_SANS, 8, GREY, 2, "center")
    tracked(c, "CONFIDENTIAL — NOT FOR CIRCULATION", cx, m + 30,
            FONT_SANS, 7, HAIRLINE, 2, "center")


# --------------------------------------------------------------------------- #
# Page 2 — The System
# --------------------------------------------------------------------------- #
def draw_header_band(c, line1, line2, right_text=None):
    band_h = 46
    c.setFillColor(NAVY)
    c.rect(0, PH - band_h, PW, band_h, fill=1, stroke=0)
    tracked(c, line1, 30, PH - 19, FONT_SANS, 8, WHITE, 2.5)
    c.setFont(FONT_SANS_BOLD, 15)
    c.setFillColor(WHITE)
    c.drawString(30, PH - 38, line2)
    if right_text:
        tracked(c, right_text, PW - 30, PH - 29, FONT_SANS, 8.5, WHITE, 1.5, "right")
    return band_h


def draw_footer(c, text):
    c.setFont(FONT_SERIF_ITALIC, 8.5)
    c.setFillColor(GREY)
    c.drawCentredString(PW / 2, 16, text)


def draw_system(c):
    fill_page(c)
    band_h = draw_header_band(c, "SURAH GEMS", "THE SYSTEM")

    margin, gutter = 30, 26
    col_w = (PW - 2 * margin - gutter) / 2
    left_x = margin
    right_x = margin + col_w + gutter
    top = PH - band_h - 26

    # ----- Left column -------------------------------------------------------
    y = top
    y = heading(c, "How the code works", left_x, y)
    y = paragraph(
        c,
        "One continuous serial, pre-printed and never reset. The meaning of a "
        "stone lives in its row — type, weight, supplier — not in the code. "
        "Read across the line, not into the number.",
        left_x, y, FONT_SERIF, 9.5, INK, col_w, 13)

    y -= 12
    c.setFont(FONT_SANS_BOLD, 30)
    c.setFillColor(NAVY)
    c.drawString(left_x, y - 22, serial(SERIAL_PREFIX, START_SERIAL))
    tracked(c, "→  " + serial(SERIAL_PREFIX, START_SERIAL + 1) + "  →  "
            + serial(SERIAL_PREFIX, START_SERIAL + 2),
            left_x + 132, y - 14, FONT_SANS, 9, GREY, 1)
    y -= 44

    y = heading(c, "In the field", left_x, y)
    y = paragraph(
        c,
        "The number is already printed. Fill the page header once — Place, "
        "Date, Currency — then write each buy on its own line.",
        left_x, y, FONT_SERIF, 9.5, INK, col_w, 13)

    # ----- Right column ------------------------------------------------------
    y = top
    y = heading(c, "One rule for media", right_x, y)
    y = paragraph(
        c,
        "The folder is the serial. Every photo and document for a stone lives "
        "under its number:",
        right_x, y, FONT_SERIF, 9.5, INK, col_w, 13)

    tree = [
        "/Buying/" + serial(SERIAL_PREFIX, START_SERIAL) + "/",
        "├── before/",
        "├── after/",
        "└── docs/",
    ]
    panel_h = len(tree) * 12 + 14
    y -= 4
    c.setFillColor(TINT)
    c.rect(right_x, y - panel_h, col_w, panel_h, fill=1, stroke=0)
    ty = y - 14
    c.setFont(FONT_MONO, 8.5)
    c.setFillColor(NAVY)
    for line in tree:
        c.drawString(right_x + 10, ty, line)
        ty -= 12
    y -= panel_h + 12

    y = heading(c, "What goes where", right_x, y)
    bullets = [
        ("Paper", "the buy moment — asking, my offer, final, supplier code."),
        ("Notion / bench", "recut weight, measurements, AGTL report no., status."),
        ("Never", "duplicate a number. A gap is a void to account for."),
    ]
    for label, rest in bullets:
        c.setFont(FONT_SANS_BOLD, 9)
        c.setFillColor(NAVY)
        c.drawString(right_x, y, label + " —")
        lw = pdfmetrics.stringWidth(label + " — ", FONT_SANS_BOLD, 9)
        y2 = paragraph(c, rest, right_x + lw, y, FONT_SERIF, 9.5, INK,
                       col_w - lw, 12)
        y = min(y - 12, y2) - 3

    y -= 2
    y = heading(c, "Supplier", right_x, y)
    paragraph(
        c,
        "Use a code, never the name. Keep real contacts in a separate, "
        "private list.",
        right_x, y, FONT_SERIF, 9.5, INK, col_w, 13)

    draw_footer(c, "Asking · My offer · Final are your negotiation trail — "
                   "never on the supplier copy.")


# --------------------------------------------------------------------------- #
# Page 3+ — Ledger
# --------------------------------------------------------------------------- #
LEDGER_COLS = [
    ("No.",         58, "left"),
    ("Type / hint", 96, "left"),
    ("ct",          40, "center"),
    ("Asking",      68, "center"),
    ("My offer",    68, "center"),
    ("Final buy",   68, "center"),
    ("Supplier",    62, "left"),
    ("Notes",       None, "left"),
]


def draw_ledger_page(c, page_index):
    fill_page(c)
    band_h = draw_header_band(c, "SURAH GEMS", "BUYING LEDGER",
                              right_text="CEYLON SAPPHIRE & SPINEL")

    L = 24
    R = PW - 24
    table_w = R - L

    # Resolve column widths (one flexible column: Notes).
    fixed = sum(w for _, w, _ in LEDGER_COLS if w is not None)
    flex = table_w - fixed
    widths = [w if w is not None else flex for _, w, _ in LEDGER_COLS]
    xs = [L]
    for w in widths:
        xs.append(xs[-1] + w)

    # ----- Info strip --------------------------------------------------------
    strip_y = PH - band_h - 22
    c.setStrokeColor(HAIRLINE)
    c.setLineWidth(0.6)
    fields = [
        ("Place", 150),
        ("Date", 110),
        (f"Currency ( {CURRENCY_DEFAULT} )", 90),
    ]
    x = L
    for label, line_w in fields:
        tracked(c, label.upper(), x, strip_y + 4, FONT_SANS_BOLD, 7, GREY, 1)
        lx = x + pdfmetrics.stringWidth(label.upper() + "  ", FONT_SANS_BOLD, 7) + 1
        c.line(lx, strip_y, x + line_w, strip_y)
        x += line_w + 14
    tracked(c, f"PAGE No. {page_index + 1} / {LEDGER_PAGES}",
            R, strip_y + 4, FONT_SANS_BOLD, 7.5, NAVY, 1, "right")

    # ----- Table geometry ----------------------------------------------------
    table_top = strip_y - 14
    table_bottom = 30
    colhead_h = 18
    body_h = table_top - colhead_h - table_bottom
    row_h = body_h / ROWS_PER_PAGE
    body_top = table_top - colhead_h

    # Value channel: Asking + My offer + Final buy (indices 3,4,5).
    ch_left = xs[3]
    ch_right = xs[6]

    # Channel tint over the body rows.
    c.setFillColor(TINT)
    c.rect(ch_left, table_bottom, ch_right - ch_left, body_top - table_bottom,
           fill=1, stroke=0)

    # Column-header band tint (full width).
    c.setFillColor(TINT)
    c.rect(L, body_top, table_w, colhead_h, fill=1, stroke=0)

    # Row separators.
    c.setStrokeColor(HAIRLINE)
    c.setLineWidth(0.4)
    for r in range(1, ROWS_PER_PAGE):
        ry = body_top - r * row_h
        c.line(L, ry, R, ry)

    # Light column separators.
    c.setStrokeColor(HAIRLINE)
    c.setLineWidth(0.3)
    for i in range(1, len(xs) - 1):
        if xs[i] in (ch_left, ch_right):
            continue  # navy hairlines drawn below
        c.line(xs[i], table_bottom, xs[i], table_top)

    # Navy hairlines bounding the value channel.
    c.setStrokeColor(NAVY)
    c.setLineWidth(0.9)
    c.line(ch_left, table_bottom, ch_left, table_top)
    c.line(ch_right, table_bottom, ch_right, table_top)

    # Outer border + header underline.
    c.setStrokeColor(NAVY)
    c.setLineWidth(0.9)
    c.rect(L, table_bottom, table_w, table_top - table_bottom, fill=0, stroke=1)
    c.line(L, body_top, R, body_top)

    # Column titles.
    for i, (title, _, align) in enumerate(LEDGER_COLS):
        cx_l, cx_r = xs[i], xs[i + 1]
        ty = body_top + 6
        if align == "center":
            tracked(c, title, (cx_l + cx_r) / 2, ty, FONT_SANS_BOLD, 7.5,
                    NAVY, 0.6, "center")
        else:
            tracked(c, title, cx_l + 5, ty, FONT_SANS_BOLD, 7.5, NAVY, 0.6)

    # Pre-printed serials, top row = first serial on the page.
    base = START_SERIAL + page_index * ROWS_PER_PAGE
    c.setFillColor(NAVY)
    for r in range(ROWS_PER_PAGE):
        row_top = body_top - r * row_h
        baseline = row_top - row_h / 2 - 3
        c.setFont(FONT_SANS, 9)
        c.drawString(xs[0] + 5, baseline, serial(SERIAL_PREFIX, base + r))

    draw_footer(c, "Shaded columns = your numbers. "
                   "Never copy onto the supplier receipt.")


# --------------------------------------------------------------------------- #
# Receipt pad — separate R- sequence, one per page
# --------------------------------------------------------------------------- #
def labeled_rule(c, x, y, w, label):
    tracked(c, label.upper(), x, y, FONT_SANS_BOLD, 7.5, GREY, 1.2)
    c.setStrokeColor(HAIRLINE)
    c.setLineWidth(0.6)
    c.line(x, y - 16, x + w, y - 16)


def draw_receipt_page(c, n):
    fill_page(c)
    m = 24
    c.setStrokeColor(NAVY)
    c.setLineWidth(1.0)
    c.rect(m, m, PW - 2 * m, PH - 2 * m, fill=0, stroke=1)

    cx = PW / 2
    c.setFont(FONT_SANS_BOLD, 22)
    c.setFillColor(NAVY)
    c.drawCentredString(cx, PH - 64, "SURAH GEMS")
    tracked(c, "CEYLON SAPPHIRE & SPINEL · BERUWALA, CEYLON",
            cx, PH - 80, FONT_SANS, 7.5, GREY, 2, "center")
    tracked(c, "PURCHASE RECEIPT", cx, PH - 104, FONT_SANS, 11, INK, 3.5, "center")

    # Pre-printed receipt number, top-right inside the border.
    tracked(c, "No. " + serial(RECEIPT_PREFIX, n),
            PW - m - 12, PH - m - 22, FONT_SANS_BOLD, 11, NAVY, 0.5, "right")

    c.setStrokeColor(HAIRLINE)
    c.setLineWidth(0.6)
    c.line(m + 40, PH - 118, PW - m - 40, PH - 118)

    # Fields.
    left = m + 40
    right_col = cx + 30
    field_w_l = cx - 30 - left
    field_w_r = (PW - m - 40) - right_col
    full_w = (PW - m - 40) - left

    y = PH - 150
    labeled_rule(c, left, y, field_w_l, "Date")
    labeled_rule(c, right_col, y, field_w_r, "Weight (approx)")

    y -= 46
    tracked(c, "DESCRIPTION", left, y, FONT_SANS_BOLD, 7.5, GREY, 1.2)
    c.setStrokeColor(HAIRLINE)
    c.setLineWidth(0.6)
    c.line(left, y - 16, left + full_w, y - 16)
    c.line(left, y - 36, left + full_w, y - 36)

    y -= 66
    labeled_rule(c, left, y, field_w_l, "Agreed price")
    labeled_rule(c, right_col, y, field_w_r, "Supplier name")

    # Signatures.
    sig_y = m + 58
    sig_w = full_w / 2 - 20
    c.setStrokeColor(INK)
    c.setLineWidth(0.6)
    c.line(left, sig_y, left + sig_w, sig_y)
    c.line(right_col, sig_y, right_col + sig_w, sig_y)
    tracked(c, "SUPPLIER SIGNATURE", left, sig_y - 11, FONT_SANS, 7, GREY, 1)
    tracked(c, "RECEIVED BY — SURAH GEMS", right_col, sig_y - 11,
            FONT_SANS, 7, GREY, 1)

    c.setFont(FONT_SERIF_ITALIC, 8.5)
    c.setFillColor(GREY)
    c.drawCentredString(cx, m + 14, "Top sheet to the supplier · keep the carbon copy.")


# --------------------------------------------------------------------------- #
# Builders
# --------------------------------------------------------------------------- #
def build_book(path):
    c = canvas.Canvas(path, pagesize=PAGE)
    c.setTitle("Surah Gems — Buying Ledger")
    c.setAuthor("Surah Gems")
    draw_cover(c)
    c.showPage()
    draw_system(c)
    c.showPage()
    for i in range(LEDGER_PAGES):
        draw_ledger_page(c, i)
        c.showPage()
    c.save()


def build_receipts(path):
    c = canvas.Canvas(path, pagesize=PAGE)
    c.setTitle("Surah Gems — Purchase Receipts")
    c.setAuthor("Surah Gems")
    for n in range(START_SERIAL, START_SERIAL + RECEIPT_PAGES):
        draw_receipt_page(c, n)
        c.showPage()
    c.save()


# --------------------------------------------------------------------------- #
# Versioning
# --------------------------------------------------------------------------- #
CHANGELOG = os.path.join(ROOT, "CHANGELOG.md")


def update_changelog():
    """Ensure CHANGELOG.md carries an entry for the current VERSION."""
    today = date.today().isoformat()
    marker = f"## v{VERSION}"
    if os.path.exists(CHANGELOG):
        with open(CHANGELOG, encoding="utf-8") as fh:
            body = fh.read()
        if marker in body:
            return
        entry = (f"\n{marker} — {today}\n"
                 f"- Regenerated buying book and receipt pad.\n")
        with open(CHANGELOG, "a", encoding="utf-8") as fh:
            fh.write(entry)
        print(f"  CHANGELOG: appended v{VERSION}")
    else:
        last = START_SERIAL + LEDGER_PAGES * ROWS_PER_PAGE - 1
        header = (
            "# Changelog\n\n"
            "All notable changes to the Surah Gems buying book generator.\n\n"
            f"{marker} — {today}\n"
            f"- Initial release. A5 landscape buying ledger (cover + the system "
            f"+ {LEDGER_PAGES} numbered pages, "
            f"{serial(SERIAL_PREFIX, START_SERIAL)}…{serial(SERIAL_PREFIX, last)}) "
            f"and a matching supplier receipt pad "
            f"({serial(RECEIPT_PREFIX, START_SERIAL)}…"
            f"{serial(RECEIPT_PREFIX, START_SERIAL + RECEIPT_PAGES - 1)}).\n"
            "- Continuous pre-printed serials, shaded value channel, "
            "supplier-safe receipt.\n"
            "- Google Fonts auto-download with offline base-14 fallback.\n"
        )
        with open(CHANGELOG, "w", encoding="utf-8") as fh:
            fh.write(header)
        print(f"  CHANGELOG: created with v{VERSION}")


def ensure_git_tag():
    """Tag v{VERSION} if we are in a git repo with a commit and no such tag.
    Best-effort and never fatal — the build matters more than the tag."""
    if not os.path.isdir(os.path.join(ROOT, ".git")):
        return
    try:
        existing = subprocess.run(["git", "tag", "--list", f"v{VERSION}"],
                                  cwd=ROOT, capture_output=True, text=True)
        if existing.stdout.strip():
            return
        head = subprocess.run(["git", "rev-parse", "HEAD"],
                              cwd=ROOT, capture_output=True, text=True)
        if head.returncode != 0:
            print(f"  git: no commit yet — create v{VERSION} after the first commit")
            return
        subprocess.run(["git", "tag", f"v{VERSION}"], cwd=ROOT, check=True)
        print(f"  git: tagged v{VERSION}")
    except Exception as exc:
        print(f"  git: skipped tag ({exc})")


# --------------------------------------------------------------------------- #
# Main
# --------------------------------------------------------------------------- #
def main():
    print(f"Surah Gems buying book — v{VERSION}")
    setup_fonts()
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    stamp = datetime.now().strftime("%Y%m%d")
    book = os.path.join(OUTPUT_DIR,
                        f"SurahGems_BuyingBook_v{VERSION}_{stamp}.pdf")
    receipts = os.path.join(OUTPUT_DIR,
                            f"SurahGems_Receipts_v{VERSION}_{stamp}.pdf")

    build_book(book)
    build_receipts(receipts)

    last = START_SERIAL + LEDGER_PAGES * ROWS_PER_PAGE - 1
    print(f"  ledger:   {serial(SERIAL_PREFIX, START_SERIAL)}…"
          f"{serial(SERIAL_PREFIX, last)} "
          f"({LEDGER_PAGES} pages × {ROWS_PER_PAGE} rows)")
    print(f"  receipts: {serial(RECEIPT_PREFIX, START_SERIAL)}…"
          f"{serial(RECEIPT_PREFIX, START_SERIAL + RECEIPT_PAGES - 1)} "
          f"({RECEIPT_PAGES} pages)")
    print(f"  → {os.path.relpath(book, ROOT)}")
    print(f"  → {os.path.relpath(receipts, ROOT)}")

    update_changelog()
    ensure_git_tag()
    print("Done.")


if __name__ == "__main__":
    sys.exit(main())
