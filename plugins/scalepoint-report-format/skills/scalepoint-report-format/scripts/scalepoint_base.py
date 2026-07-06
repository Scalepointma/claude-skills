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
    'ACCENT_ROTATION', 'get_accent_color',
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
    'FONT_DISPLAY', 'FONT_DISPLAY_BOLD', 'FONT_BODY', 'FONT_BODY_BOLD',
    'FONT_BODY_ITALIC',
    # Helpers
    '_draw_shadow', '_wrap_text', '_wrap_and_draw',
    'measure_text_height', 'draw_body_text', 'clean_text',
    'will_fit', 'remaining_height',
    'ASSET_MAP', 'discover_assets',
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

# Accent rotation — gold is dominant; teal + olive provide contrast.
# Never the same color twice in a row.
ACCENT_ROTATION = [GOLD, TEAL, GOLD, OLIVE, GOLD, TEAL]


def get_accent_color(index, prev_color=None):
    """Get accent color at `index`, guaranteeing no repeat with prev_color."""
    color = ACCENT_ROTATION[index % len(ACCENT_ROTATION)]
    if prev_color and color == prev_color:
        color = ACCENT_ROTATION[(index + 1) % len(ACCENT_ROTATION)]
    return color


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
# Display / headings / card titles / stat numbers — serif (echoes Libre Baskerville)
FONT_DISPLAY      = "Times-Roman"
FONT_DISPLAY_BOLD = "Times-Bold"

# Body copy / tables / bullets / footnotes — sans for readability at small sizes
FONT_BODY         = "Helvetica"
FONT_BODY_BOLD    = "Helvetica-Bold"
FONT_BODY_ITALIC  = "Helvetica-Oblique"


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


def discover_assets(extra_dirs=None):
    """
    Search for ScalePoint assets across common skill locations.
    Returns {canonical_name: path_or_None} and prints a report.
    """
    import glob, os

    search_dirs = []
    for pattern in [
        "/sessions/*/mnt/*/scalepoint-report-format*/assets",
        "/sessions/*/mnt/**/scalepoint-report-format*/assets",
        "/sessions/*/mnt/.claude/skills/scalepoint*/assets",
        "/sessions/*/mnt/outputs/scalepoint-report-format/assets",
        "/sessions/*/mnt/*/assets",
        "/sessions/*/mnt/uploads",
    ]:
        search_dirs.extend(glob.glob(pattern, recursive=True))
    if extra_dirs:
        search_dirs.extend(extra_dirs)

    found = {}
    for canonical, filenames in ASSET_MAP.items():
        found[canonical] = None
        for d in search_dirs:
            for fn in filenames:
                path = os.path.join(d, fn)
                if os.path.isfile(path):
                    found[canonical] = path
                    break
            if found[canonical]:
                break

    print("=== ScalePoint Asset Discovery ===")
    for name, path in found.items():
        if path:
            print(f"  FOUND  {name}: {path}")
        else:
            print(f"  MISSING {name}: searched for {ASSET_MAP[name]}")
    print("==================================")
    return found


# =============================================================================
# CHARACTER CLEANUP
# =============================================================================
def clean_text(text):
    """Fix encoding failures in extracted content (smart quotes, control chars).
    Run on ALL text pulled from docx/pptx/pdf before rendering."""
    if not text:
        return text
    import re
    text = text.replace('\ufffd', '')
    text = text.replace('\u2018', "'").replace('\u2019', "'")
    text = text.replace('\u201c', '"').replace('\u201d', '"')
    text = text.replace('\u2013', '-').replace('\u2014', '--')
    # ScalePoint-specific: normalize common M&A shorthand typos
    text = re.sub(r'\bM\s*&\s*A\b', 'M&A', text)
    text = re.sub(r'\bLOI\b', 'LOI', text)  # preserved (not stripped)
    text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', '', text)
    return text
