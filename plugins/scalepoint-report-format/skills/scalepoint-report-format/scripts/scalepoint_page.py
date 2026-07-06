"""
ScalePoint M&A PDF Page Setup — Header, Footer, Section Titles, Dividers

The signature ScalePoint page frame:
 - minimal header (just a fine gold hairline)
 - branded footer: icon at bottom-left, deep-green bar across, gold segment
   at right end showing the page title + page number — mirrors the brand
   guide's own page template.
"""

from scalepoint_base import *


def draw_page_bg(c):
    """Paint full page with warm cream. Call FIRST on every interior page."""
    c.setFillColor(PAGE_BG)
    c.rect(0, 0, W, H, fill=1, stroke=0)


def draw_page_setup(c, doc_title="", page_num=1, icon_path=None,
                    section_label=""):
    """
    Draw background + header hairline + branded footer.
    - doc_title: the full document name (appears in footer micro-copy)
    - section_label: short label for the current section (appears in footer bar).
      If omitted, falls back to doc_title.
    - icon_path: path to icon-fullcolor or icon-gold PNG (small mark at
      bottom-left). Falls back to a drawn triangle mark if missing.
    """
    draw_page_bg(c)
    draw_header(c)
    draw_footer(c, doc_title, page_num, icon_path, section_label)


def draw_header(c):
    """Minimal header: a fine gold hairline beneath an empty band. The brand
    guide puts branding in the footer, so the header stays quiet."""
    # Fine gold accent line across the top gutter
    c.setFillColor(GOLD)
    c.rect(MARGIN, H - HEADER_H - HEADER_ACCENT_H,
           CONTENT_W, HEADER_ACCENT_H, fill=1, stroke=0)


def _draw_fallback_icon(c, x, y, size):
    """Draw a simple triangle+peaks mark if icon PNG isn't found.
    Echoes the ScalePoint mark: gold peak + green M&M base."""
    import math
    # Outer triangle (deep green)
    c.setFillColor(DEEP_GREEN)
    p = c.beginPath()
    p.moveTo(x + size / 2, y + size)
    p.lineTo(x, y)
    p.lineTo(x + size, y)
    p.close()
    c.drawPath(p, fill=1, stroke=0)
    # Top gold notch (peak)
    c.setFillColor(GOLD)
    top_h = size * 0.4
    p2 = c.beginPath()
    p2.moveTo(x + size / 2, y + size)
    p2.lineTo(x + size / 2 - top_h * 0.6, y + size - top_h)
    p2.lineTo(x + size / 2 + top_h * 0.6, y + size - top_h)
    p2.close()
    c.drawPath(p2, fill=1, stroke=0)


def draw_footer(c, doc_title="", page_num=1, icon_path=None,
                section_label=""):
    """
    Branded footer — the 'ScalePoint signature' strip:

      [icon]  [---- deep-green bar with section label ----]  [ gold segment : page# ]

    Layout (bottom of page):
      y = 0 .. FOOTER_H      : footer body
      y = FOOTER_H .. FOOTER_H + FOOTER_ACCENT_H : thin gold under-accent
    """
    footer_y = 0

    # Small icon at far left (slightly above footer baseline)
    icon_size = 26
    icon_x = MARGIN - 4
    icon_y = footer_y + (FOOTER_H - icon_size) / 2
    if icon_path:
        try:
            c.drawImage(icon_path, icon_x, icon_y, icon_size, icon_size,
                        preserveAspectRatio=True, mask='auto')
        except Exception:
            _draw_fallback_icon(c, icon_x, icon_y, icon_size)
    else:
        _draw_fallback_icon(c, icon_x, icon_y, icon_size)

    # Deep-green bar (the footer strip) — starts after icon, stops where gold
    # segment begins
    bar_left  = icon_x + icon_size + 8
    # Gold segment takes the final ~15% of the bar
    gold_w    = 90
    bar_right = W - MARGIN
    bar_green_right = bar_right - gold_w

    c.setFillColor(DEEP_GREEN)
    c.rect(bar_left, footer_y + 4, bar_green_right - bar_left,
           FOOTER_H - 8, fill=1, stroke=0)

    # Gold segment (contains page number)
    c.setFillColor(GOLD)
    c.rect(bar_green_right, footer_y + 4, gold_w, FOOTER_H - 8,
           fill=1, stroke=0)

    # Section label in white serif inside the green bar
    label = section_label or doc_title
    if label:
        c.setFont(FONT_DISPLAY, 10)
        c.setFillColor(WHITE)
        c.drawString(bar_left + 14, footer_y + FOOTER_H / 2 - 3, label)

    # Page number in deep-green serif inside gold segment (right-aligned)
    c.setFont(FONT_DISPLAY, 11)
    c.setFillColor(DEEP_GREEN)
    c.drawRightString(bar_right - 12, footer_y + FOOTER_H / 2 - 3,
                      f"{page_num:02d}")

    # (No micro-copy below the footer bar — the bar itself carries the label.
    # Earlier versions had an under-bar "Confidential | ScalePoint M&A" line
    # that clipped at the page bottom edge. Removed for clarity.)


def draw_section_title(c, x, y, text, size=28):
    """
    Draw large section title in serif. LARGEST text element on a page.
    Enforces PAD_SECTION_TITLE_TOP when at top of page.
    Returns y after title with GAP_SECTION_TO_KICKER below.
    """
    if y >= CONTENT_TOP - 2:
        y -= PAD_SECTION_TITLE_TOP

    c.setFont(FONT_DISPLAY_BOLD, size)
    c.setFillColor(DEEP_GREEN)

    title_w = c.stringWidth(text, FONT_DISPLAY_BOLD, size)
    if title_w > CONTENT_W:
        words = text.split()
        mid = len(words) // 2
        line1 = " ".join(words[:mid])
        line2 = " ".join(words[mid:])
        c.drawString(x, y, line1)
        y -= size + 4
        c.drawString(x, y, line2)
        return y - GAP_SECTION_TO_KICKER
    else:
        c.drawString(x, y, text)
        return y - size - GAP_SECTION_TO_KICKER


def draw_kicker(c, x, y, text, color=None):
    """Small uppercase kicker with letter-spacing. Returns y below."""
    if color is None:
        color = GOLD  # ScalePoint kickers are gold, not teal
    c.setFont(FONT_BODY_BOLD, 9)
    c.setFillColor(color)

    char_x = x
    for ch in text.upper():
        c.drawString(char_x, y, ch)
        char_x += c.stringWidth(ch, FONT_BODY_BOLD, 9) + 1.5

    return y - GAP_KICKER_TO_SUBHEAD


def draw_subheading(c, x, y, text, size=22):
    """Serif sub-heading in deep green. Returns y with GAP_SUBHEAD_TO_BODY."""
    c.setFont(FONT_DISPLAY_BOLD, size)
    c.setFillColor(DEEP_GREEN)
    c.drawString(x, y, text)
    return y - size - GAP_SUBHEAD_TO_BODY


def draw_title_group(c, x, y, kicker="", subheading="", intro_text=None,
                     section_title=None, new_section=False):
    """
    Complete title group: optional section title -> kicker -> subheading ->
    optional intro paragraph. Handles all internal spacing.

    new_section=True adds GAP_NEW_SECTION_ABOVE for mid-page section breaks.
    """
    if new_section and y < CONTENT_TOP - 2:
        y -= GAP_NEW_SECTION_ABOVE

    # Enforce top padding when the group starts at CONTENT_TOP so kickers
    # and subheadings aren't clipped by the header gutter.
    if y >= CONTENT_TOP - 2 and not section_title:
        y -= PAD_SECTION_TITLE_TOP

    if section_title:
        y = draw_section_title(c, x, y, section_title)

    if kicker:
        y = draw_kicker(c, x, y, kicker)

    if subheading:
        y = draw_subheading(c, x, y, subheading)

    if intro_text:
        y = draw_body_text(c, x, y, intro_text)
        y -= GAP_BODY_TO_ELEMENT

    return y


def draw_divider(c, x, y, width=None, color=None, thickness=1.0,
                 gap_above=12, gap_below=12):
    """Thin accent line between sections. Returns y below the divider."""
    if width is None:
        width = CONTENT_W
    if color is None:
        color = GOLD

    y -= gap_above
    c.setStrokeColor(color)
    c.setLineWidth(thickness)
    c.line(x, y, x + width, y)
    return y - gap_below


def ensure_space(c, y_current, needed_height, doc_title="", page_num=1,
                 icon_path=None, section_label=""):
    """
    If needed_height won't fit above the footer zone, start a new page.
    Returns (new_y, new_page_num). Call BEFORE drawing any near-bottom element.
    """
    if not will_fit(y_current, needed_height):
        c.showPage()
        page_num += 1
        draw_page_setup(c, doc_title, page_num, icon_path, section_label)
        return CONTENT_TOP, page_num
    return y_current, page_num
