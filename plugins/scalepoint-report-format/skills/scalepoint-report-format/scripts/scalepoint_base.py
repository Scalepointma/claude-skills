"""
ScalePoint M&A PDF Base — Colors, Constants, Shared Helpers
===========================================================
All other scalepoint_*.py modules import from here.

Brand: deep forest green (#0A2D2A) + gold (#CB9D43) with olive/teal secondaries.
Typography: Times (serif, display) + Helvetica (sans, body) pairing — a
high-fidelity stand-in for Libre Baskerville + a legible body face.
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import HexColor, Color

__all__ = [
    # Colors
    'DEEP_GREEN', 'DEEP_GREEN_DK', 'GOLD', 'GOLD_LIGHT', 'GOLD_DEEP',
    'OLIVE', 'TEAL', 'WHITE', 'NEAR_WHITE', 'CREAM',
    'BODY_COLOR', 'SECONDARY_COLOR', 'LIGHT_TEXT', 'BORDER_COLOR',
    'BG_LIGHT', 'CALLOUT_GOLD_BG', 'CALLOUT_TEAL_BG', 'CALLOUT_OLIVE_BG',
    'ACCENT_ROTATION', 'get_accent_color', 'LABEL_GOLD', 'LABEL_SIZE', 'SEPIA',
    # Dimensions
    'W', 'H', 'MARGIN', 'CONTENT_W', 'CORNER_R', 'ACCENT_W', 'PAGE_BG',
    'HEADER_H', 'HEADER_ACCENT_H', 'HEADER_GAP', 'CONTENT_TOP',
    'FOOTER_H', 'FOOTER_ACCENT_H', 'FOOTER_SAFETY', 'FOOTER_ZONE_TOP',
    'CONTENT_HEIGHT',
    # Spacing
    'PAD_SECTION_TITLE_TOP', 'GAP_SECTION_TO_KICKER', 'GAP_KICKER_TO_SUBHEAD',
    'GAP_SUBHEAD_TO_BODY', 'GAP_BODY_TO_ELEMENT', 'GAP_ELEMENT_TO_ELEMENT',
    'GAP_NEW_SECTION_ABOVE', 'GAP_CARD_INTERNAL_PAD',
    # Font minimums
    'MIN_FONT_BODY', 'MIN_FONT_CARD_BODY', 'MIN_FONT_TABLE_BODY',
    'MIN_FONT_STAT_NUMBER', 'MIN_FONT_STAT_LABEL',
    # Font families
    'FONT_DISPLAY', 'FONT_DISPLAY_BOLD', 'FONT_DISPLAY_ITALIC',
    'FONT_BODY', 'FONT_BODY_BOLD', 'FONT_BODY_ITALIC',
    # Helpers
    '_draw_shadow', '_wrap_text', '_wrap_and_draw',
    'measure_text_height', 'draw_body_text', 'clean_text', 'assert_no_em_dash',
    'will_fit', 'remaining_height',
    'ASSET_MAP', 'discover_assets', 'trim_image', 'image_ratio',
    'spaced', 'draw_descriptor',
    'HexColor', 'Color', 'letter',
]

# =============================================================================
# BRAND COLORS — ScalePoint M&A
# =============================================================================
# Primary
DEEP_GREEN    = HexColor("#0A2D2A")   # forest/navy — backgrounds, dark text
DEEP_GREEN_DK = HexColor("#061C1A")   # deeper variant for back cover
GOLD          = HexColor("#CB9D43")   # primary accent, dominant highlight
GOLD_DEEP     = HexColor("#D7A848")   # mid of gold gradient
GOLD_LIGHT    = HexColor("#F6E279")   # light end of gold gradient (accents only)

# Secondary
OLIVE = HexColor("#869846")
TEAL  = HexColor("#18766A")

# Neutrals
WHITE       = HexColor("#FFFFFF")
NEAR_WHITE  = HexColor("#F7F5EF")   # warm near-white (cream-adjacent)
CREAM       = HexColor("#FAF8F2")   # page background — warm paper feel

# Text
BODY_COLOR      = HexColor("#0A2D2A")   # body copy is deep green, not black
SECONDARY_COLOR = HexColor("#4A5B58")   # muted green-grey for footnotes
LIGHT_TEXT      = HexColor("#8A9995")   # very light for footer micro-copy
BORDER_COLOR    = HexColor("#D9D4C6")   # warm cream border

# Backgrounds
BG_LIGHT         = CREAM
CALLOUT_GOLD_BG  = HexColor("#FBF4DE")
CALLOUT_TEAL_BG  = HexColor("#E3EFEC")
CALLOUT_OLIVE_BG = HexColor("#EEF1DF")

# RULE 3 (2026-07): accent discipline. The old random gold/teal/olive rotation
# looked cheap. Default accent is a SINGLE consistent GOLD everywhere.
# To break up gold deliberately, use the explicit palette helpers:
#   card_grid_rows(..., row_colors=[GOLD, DEEP_GREEN, OLIVE])   (one colour per ROW)
#   cards_by_column(..., col_colors=[GOLD, DEEP_GREEN, OLIVE])  (one colour per COLUMN)
#   draw_stat_row(..., accent_color=DEEP_GREEN)                 (whole row, e.g. 2nd stat row)
# Never a per-card random mix.
ACCENT_ROTATION = [GOLD]

# RULE 22: THE standard hero/stat descriptor — ALL CAPS, this gold, 8pt,
# letter-spaced — identical everywhere (cover badges, stat boxes, value cards).
LABEL_GOLD = HexColor("#A9803A")
LABEL_SIZE = 8

# Sepia / warm off-white — cover hero-badge faces (rule 11)
SEPIA = HexColor("#F1E9D6")


def get_accent_color(index, prev_color=None):
    """Accent colour for auto-styled elements: always GOLD (rule 3).
    Signature kept for backward compatibility."""
    return GOLD


# =============================================================================
# PAGE CONSTANTS
# =============================================================================
W, H = letter  # 612 x 792
MARGIN = 50
CONTENT_W = W - 2 * MARGIN  # 512pt
CORNER_R = 10   # ScalePoint uses slightly tighter corners than EcoClaim
ACCENT_W = 5    # accent bar width (the visible sliver)

PAGE_BG = CREAM   # warm paper feel on every interior page

# Header — minimal (gold hairline); branding lives in the footer
HEADER_H = 36
HEADER_ACCENT_H = 2
HEADER_GAP = 18
CONTENT_TOP = H - HEADER_H - HEADER_ACCENT_H - HEADER_GAP  # ~736

# Footer — the "ScalePoint signature": icon left + deep-green bar + gold segment right
FOOTER_H = 30
FOOTER_ACCENT_H = 1.5
FOOTER_SAFETY = 20
FOOTER_ZONE_TOP = FOOTER_H + FOOTER_ACCENT_H + FOOTER_SAFETY  # ~52

CONTENT_HEIGHT = CONTENT_TOP - FOOTER_ZONE_TOP  # ~684

# =============================================================================
# SPACING CONSTANTS
# =============================================================================
PAD_SECTION_TITLE_TOP = 18
GAP_SECTION_TO_KICKER = 14
GAP_KICKER_TO_SUBHEAD = 12
GAP_SUBHEAD_TO_BODY   = 14
GAP_BODY_TO_ELEMENT   = 16
GAP_ELEMENT_TO_ELEMENT = 20
GAP_NEW_SECTION_ABOVE  = 36
GAP_CARD_INTERNAL_PAD  = 16

MIN_FONT_BODY         = 10
MIN_FONT_CARD_BODY    = 9.5
MIN_FONT_TABLE_BODY   = 9
MIN_FONT_STAT_NUMBER  = 30
MIN_FONT_STAT_LABEL   = 8

# =============================================================================
# FONT FAMILIES
# =============================================================================
# Display face: Libre Baskerville if the bundled TTFs are present in
# assets/fonts/ (registered below), else Times as a high-fidelity stand-in.
# Body copy / tables / bullets / footnotes — sans for readability at small sizes.
FONT_DISPLAY        = "Times-Roman"
FONT_DISPLAY_BOLD   = "Times-Bold"
FONT_DISPLAY_ITALIC = "Times-Italic"

FONT_BODY         = "Helvetica"
FONT_BODY_BOLD    = "Helvetica-Bold"
FONT_BODY_ITALIC  = "Helvetica-Oblique"


def _register_display_fonts():
    """Register bundled Libre Baskerville TTFs if present; fall back to Times."""
    global FONT_DISPLAY, FONT_DISPLAY_BOLD, FONT_DISPLAY_ITALIC
    import os
    fonts_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             "..", "assets", "fonts")
    ttfs = {
        "LibreBaskerville":        "LibreBaskerville-Regular.ttf",
        "LibreBaskerville-Bold":   "LibreBaskerville-Bold.ttf",
        "LibreBaskerville-Italic": "LibreBaskerville-Italic.ttf",
    }
    try:
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfbase.ttfonts import TTFont
        for name, fn in ttfs.items():
            path = os.path.join(fonts_dir, fn)
            if not os.path.isfile(path):
                raise FileNotFoundError(fn)
            pdfmetrics.registerFont(TTFont(name, path))
        FONT_DISPLAY        = "LibreBaskerville"
        FONT_DISPLAY_BOLD   = "LibreBaskerville-Bold"
        FONT_DISPLAY_ITALIC = "LibreBaskerville-Italic"
    except Exception:
        print("NOTE: Libre Baskerville TTFs not available; using Times for display type.")


_register_display_fonts()


# =============================================================================
# SHADOW HELPER
# =============================================================================
def _draw_shadow(c, x, y, w, h, radius=CORNER_R, offset=2, opacity=0.06):
    """Draw a subtle drop shadow behind a card."""
    shadow_color = Color(0, 0, 0, opacity)
    c.saveState()
    c.setFillColor(shadow_color)
    c.setStrokeColor(shadow_color)
    c.roundRect(x + offset, y - offset, w, h, radius, fill=1, stroke=0)
    c.restoreState()


# =============================================================================
# TEXT HELPERS
# =============================================================================
def _wrap_text(c, text, max_width, font, size):
    """Wrap text into lines. Returns list of line strings. Does NOT draw."""
    words = text.split()
    lines = []
    current_line = ""
    for word in words:
        test = f"{current_line} {word}".strip()
        if c.stringWidth(test, font, size) <= max_width:
            current_line = test
        else:
            if current_line:
                lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)
    return lines


def measure_text_height(c, text, max_width, font=None, size=10, leading=13):
    """Calculate wrapped text height WITHOUT drawing. Use during planning."""
    if not text:
        return 0
    if font is None:
        font = FONT_BODY
    lines = _wrap_text(c, text, max_width, font, size)
    return len(lines) * leading


def _wrap_and_draw(c, text, x, y, max_width, font, size, leading, color,
                   max_lines=None):
    """Wrap text to max_width and draw line by line. Returns y after last line."""
    c.setFont(font, size)
    c.setFillColor(color)

    lines = _wrap_text(c, text, max_width, font, size)
    if max_lines:
        lines = lines[:max_lines]

    cur_y = y
    for line in lines:
        if cur_y < FOOTER_ZONE_TOP:
            print(f"WARNING: text truncated at y={cur_y:.0f} (footer zone). "
                  f"Content lost: '{line[:40]}...'")
            break
        c.drawString(x, cur_y, line)
        cur_y -= leading

    return cur_y


def draw_body_text(c, x, y, text, max_width=None):
    """Draw body text (10pt deep-green sans). Returns y after text."""
    if max_width is None:
        max_width = CONTENT_W
    return _wrap_and_draw(c, text, x, y, max_width,
                          FONT_BODY, 10, 13, BODY_COLOR)


# =============================================================================
# SPATIAL SAFETY
# =============================================================================
def will_fit(y_current, element_height):
    """Check if element_height fits above the footer zone."""
    return (y_current - element_height) >= FOOTER_ZONE_TOP


def remaining_height(y_current):
    """Points of content space remaining above the footer zone."""
    return max(0, y_current - FOOTER_ZONE_TOP)


# =============================================================================
# ASSET DISCOVERY
# =============================================================================
ASSET_MAP = {
    "logo-primary":    ["logo-primary-horizontal.png"],
    "logo-stacked":    ["logo-stacked-on-dark.png"],
    "logo-white":      ["logo-white.png"],
    "icon-fullcolor":  ["icon-fullcolor.png"],
    "icon-gold":       ["icon-gold.png"],
    "pattern-light":   ["pattern-light.png"],
    "cover-bg":        ["cover-bg.jpg", "cover-bg.png"],  # optional override
}


def trim_image(img_path, tolerance=30, pad=8):
    """RULE 4 (root-cause fix): auto-trim transparent AND solid-background
    padding from a logo/icon PNG. The stacked logo ships 2560x1538 with only
    ~714x497 of content — placed untrimmed it renders ~3x too small.
    Returns the path to a cached trimmed copy (same directory or temp)."""
    import os, tempfile
    try:
        from PIL import Image
    except ImportError:
        return img_path
    base, ext = os.path.splitext(os.path.basename(img_path))
    for cache_dir in (os.path.dirname(img_path), tempfile.gettempdir()):
        cached = os.path.join(cache_dir, f"{base}_trim.png")
        if os.path.isfile(cached):
            return cached
    try:
        img = Image.open(img_path).convert("RGBA")
        # 1) alpha-trim
        bbox = img.getbbox()
        if bbox:
            img = img.crop(bbox)
        # 2) solid-background trim (diff vs corner pixel)
        px = img.load()
        w, h = img.size
        bg = px[0, 0]
        minx, miny, maxx, maxy = w, h, -1, -1
        for yy in range(0, h, 2):
            for xx in range(0, w, 2):
                p = px[xx, yy]
                if p[3] > 10 and (abs(p[0]-bg[0]) + abs(p[1]-bg[1]) + abs(p[2]-bg[2]) > tolerance or bg[3] <= 10):
                    if xx < minx: minx = xx
                    if xx > maxx: maxx = xx
                    if yy < miny: miny = yy
                    if yy > maxy: maxy = yy
        if maxx > minx and maxy > miny and (maxx - minx) < w - 4:
            img = img.crop((max(0, minx - pad), max(0, miny - pad),
                            min(w, maxx + pad + 1), min(h, maxy + pad + 1)))
        out = None
        for cache_dir in (os.path.dirname(img_path), tempfile.gettempdir()):
            try:
                out = os.path.join(cache_dir, f"{base}_trim.png")
                img.save(out)
                break
            except OSError:
                continue
        return out or img_path
    except Exception:
        return img_path


def image_ratio(img_path):
    """Return height/width of an image (for sizing drawImage calls)."""
    try:
        from PIL import Image
        w, h = Image.open(img_path).size
        return h / w
    except Exception:
        return 0.7


def discover_assets(extra_dirs=None, trim=True):
    """
    Locate ScalePoint brand assets. Default location is this skill's own
    assets/ folder (relative to this module) — no machine-specific paths.
    Pass extra_dirs to prepend additional search locations.
    Logos/icons are auto-trimmed (rule 4) so they render at true size.
    NOTE: logo-white.png has an opaque BLACK background baked in — never
    place it on a colour field; use logo-stacked (bg is exactly DEEP_GREEN).
    """
    import os

    module_assets = os.path.normpath(os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "..", "assets"))
    search_dirs = list(extra_dirs or []) + [module_assets]

    TRIMMABLE = {"logo-primary", "logo-stacked", "icon-fullcolor", "icon-gold"}
    found = {}
    for canonical, filenames in ASSET_MAP.items():
        found[canonical] = None
        for d in search_dirs:
            for fn in filenames:
                path = os.path.join(d, fn)
                if os.path.isfile(path):
                    found[canonical] = trim_image(path) if (trim and canonical in TRIMMABLE) else path
                    break
            if found[canonical]:
                break

    print("=== ScalePoint Asset Discovery ===")
    for name, path in found.items():
        if path:
            note = "  [do NOT place on colour fields — opaque black bg]" if name == "logo-white" else ""
            print(f"  FOUND  {name}: {path}{note}")
        else:
            print(f"  MISSING {name}: searched for {ASSET_MAP[name]}")
    print("==================================")
    return found


# =============================================================================
# LETTER-SPACED CAPS (kickers, descriptors) — shared so style can't drift
# =============================================================================
def spaced(c, x, y, text, font=None, size=None, color=None, tracking=1.2,
           center=False, right=False):
    """Letter-spaced text. Default = THE standard descriptor (rule 22):
    ALL CAPS, LABEL_GOLD, 8pt."""
    font = font or FONT_BODY_BOLD
    size = size or LABEL_SIZE
    color = color or LABEL_GOLD
    c.setFont(font, size)
    c.setFillColor(color)
    total = sum(c.stringWidth(ch, font, size) + tracking for ch in text) - tracking
    sx = x - total / 2 if center else (x - total if right else x)
    for ch in text:
        c.drawString(sx, y, ch)
        sx += c.stringWidth(ch, font, size) + tracking


def draw_descriptor(c, cx, y, label, center=True):
    """RULE 22: the ONE standard hero/stat descriptor — ALL CAPS, LABEL_GOLD,
    8pt, letter-spaced. Identical under every hero number, stat box and value
    card, regardless of the element's accent colour."""
    spaced(c, cx, y, label.upper(), FONT_BODY_BOLD, LABEL_SIZE, LABEL_GOLD,
           tracking=1.2, center=center)


# =============================================================================
# CHARACTER CLEANUP
# =============================================================================
def clean_text(text):
    """Fix encoding failures AND enforce the dash rule. Run on ALL text
    (extracted or generated) before rendering.

    RULE 19: NO EM DASHES, ever. Em dashes become ', '. En dashes survive
    ONLY between digits (numeric ranges: $1.19M\u20131.36M, Net 30\u2013120);
    anywhere else they become ', ' too. Prefer rewriting with commas/colons
    upstream; this is the mechanical safety net."""
    if not text:
        return text
    import re
    text = text.replace('\ufffd', '')
    text = text.replace('\u2018', "'").replace('\u2019', "'")
    text = text.replace('\u201c', '"').replace('\u201d', '"')
    # em dash (and double-hyphen used as one) -> comma
    text = re.sub(r'\s*(?:\u2014|--)\s*', ', ', text)
    # en dash: keep between digits, else -> comma
    text = re.sub(r'(?<=[\d%KMB\)])\s*\u2013\s*(?=[\d$])', '\u2013', text)
    text = re.sub(r'\s*\u2013\s*(?![\d$])', ', ', text)
    # ScalePoint-specific: normalize common M&A shorthand typos
    text = re.sub(r'\bM\s*&\s*A\b', 'M&A', text)
    text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', '', text)
    return text


def assert_no_em_dash(*texts):
    """Hard check for generated copy (rule 19). Raises on any em dash."""
    for t in texts:
        if t and '\u2014' in t:
            raise ValueError(f"Em dash in content (rule 19), rewrite with comma/colon: {t[:70]}")
