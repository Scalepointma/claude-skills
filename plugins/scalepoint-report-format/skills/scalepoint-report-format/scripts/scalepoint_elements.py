"""
ScalePoint M&A PDF Elements — Callouts, Tables, Bullets, Footnotes, TOC.
M&A additions: deal tombstone and KPI strip (see bottom).
"""

from scalepoint_base import *


# =============================================================================
# BULLET LIST
# =============================================================================
def draw_bullet_list(c, x, y, items, max_width=None, indent=12,
                     bullet_char="\u2022", font=None, size=10,
                     leading=13, color=None, bold_prefix=False):
    """
    Draw a bulleted list with per-item wrapping.
    Items can be strings or dicts {"prefix": "Bold part", "text": "rest"}.
    """
    if max_width is None:
        max_width = CONTENT_W
    if color is None:
        color = BODY_COLOR
    if font is None:
        font = FONT_BODY

    bullet_w = c.stringWidth(bullet_char + " ", font, size)
    text_x = x + indent + bullet_w
    text_w = max_width - indent - bullet_w

    cur_y = y
    for item in items:
        if cur_y < FOOTER_ZONE_TOP:
            print(f"WARNING: bullet list truncated at y={cur_y:.0f}")
            break

        c.setFont(font, size)
        c.setFillColor(GOLD)       # bullets themselves are gold for a subtle brand cue
        c.drawString(x + indent, cur_y, bullet_char)

        if isinstance(item, dict):
            prefix = item.get("prefix", "")
            text = item.get("text", "")
            if prefix:
                c.setFont(FONT_BODY_BOLD, size)
                c.setFillColor(DEEP_GREEN)
                c.drawString(text_x, cur_y, prefix)
                prefix_w = c.stringWidth(prefix + " ", FONT_BODY_BOLD, size)
                remaining_w = text_w - prefix_w
                if text and remaining_w > 50:
                    lines = _wrap_text(c, text, remaining_w, font, size)
                    if lines:
                        c.setFont(font, size)
                        c.setFillColor(color)
                        c.drawString(text_x + prefix_w, cur_y, lines[0])
                        cur_y -= leading
                        for line in lines[1:]:
                            if cur_y < FOOTER_ZONE_TOP:
                                break
                            c.drawString(text_x, cur_y, line)
                            cur_y -= leading
                    else:
                        cur_y -= leading
                else:
                    cur_y -= leading
                    if text:
                        cur_y = _wrap_and_draw(c, text, text_x, cur_y,
                                               text_w, font, size, leading, color)
            else:
                cur_y = _wrap_and_draw(c, text, text_x, cur_y, text_w,
                                       font, size, leading, color)
        else:
            lines = _wrap_text(c, str(item), text_w, font, size)
            c.setFont(font, size)
            c.setFillColor(color)
            for j, line in enumerate(lines):
                if cur_y < FOOTER_ZONE_TOP:
                    break
                c.drawString(text_x, cur_y, line)
                cur_y -= leading

        cur_y -= 3

    return cur_y


# =============================================================================
# CALLOUTS
# =============================================================================
def draw_reverse_tint(c, x, y, w, h, title="", body="",
                      bg_color=None, title_color=None,
                      body_color=None, shadow=True):
    """Dark reverse-tint card for HERO elements only. Max 1 per page."""
    if bg_color is None:
        bg_color = DEEP_GREEN
    if title_color is None:
        title_color = GOLD
    if body_color is None:
        body_color = HexColor("#E8E4D7")   # warm off-white on green

    if shadow:
        _draw_shadow(c, x, y, w, h, opacity=0.12)

    c.setFillColor(bg_color)
    c.roundRect(x, y, w, h, CORNER_R, fill=1, stroke=0)

    if title:
        c.setFont(FONT_DISPLAY_BOLD, 14)
        c.setFillColor(title_color)
        c.drawString(x + 20, y + h - 28, title)

    if body:
        _wrap_and_draw(c, body, x + 20, y + h - 48,
                       w - 40, FONT_BODY, 10, 13, body_color)

    return y


def draw_callout_bar(c, x, y, w, h, text="", bg_color=None,
                     text_color=None):
    """Full-width dark bar. RARE (rule 9): the DEFAULT callout is the
    gold-on-gold `draw_light_callout` (pale gold bg + gold accent +
    deep-green text). Reserve this dark bar for exceptional cases."""
    if bg_color is None:
        bg_color = DEEP_GREEN
    if text_color is None:
        text_color = GOLD

    c.setFillColor(bg_color)
    c.roundRect(x, y, w, h, CORNER_R, fill=1, stroke=0)

    if text:
        font_name = FONT_DISPLAY_BOLD
        font_size = 11
        leading = 14
        max_w = w - 40
        c.setFont(font_name, font_size)

        lines = _wrap_text(c, text, max_w, font_name, font_size)
        text_block_h = len(lines) * leading
        start_y = y + (h + text_block_h) / 2 - leading + 2

        c.setFillColor(text_color)
        for line in lines:
            c.drawString(x + 20, start_y, line)
            start_y -= leading

    return y


def draw_light_callout(c, x, y, w, h, text="", bg_color=None,
                       accent_color=None, shadow=True):
    """Tinted callout with left accent bar — for emphasis / pull-quotes."""
    if bg_color is None:
        bg_color = CALLOUT_GOLD_BG
    if accent_color is None:
        accent_color = GOLD

    if shadow:
        _draw_shadow(c, x, y, w, h)

    c.setFillColor(accent_color)
    c.roundRect(x, y, w, h, CORNER_R, fill=1, stroke=0)

    c.setFillColor(bg_color)
    c.roundRect(x + ACCENT_W, y, w - ACCENT_W, h, CORNER_R, fill=1, stroke=0)

    if text:
        font_name = FONT_DISPLAY_BOLD
        font_size = 11
        leading = 14
        max_w = w - ACCENT_W - 32
        c.setFont(font_name, font_size)

        lines = _wrap_text(c, text, max_w, font_name, font_size)
        text_block_h = len(lines) * leading
        start_y = y + (h + text_block_h) / 2 - leading + 2

        c.setFillColor(DEEP_GREEN)
        for line in lines:
            c.drawString(x + ACCENT_W + 16, start_y, line)
            start_y -= leading

    return y


# =============================================================================
# FOOTNOTE
# =============================================================================
def draw_footnote(c, x, y, text, max_width=None):
    """8pt italic muted — for disclaimers, caveats, *Notes. NEVER in a box."""
    if max_width is None:
        max_width = CONTENT_W
    return _wrap_and_draw(c, text, x, y, max_width,
                          FONT_BODY_ITALIC, 8, 10.5, SECONDARY_COLOR)


# =============================================================================
# TABLE
# =============================================================================
def draw_table(c, x, y, col_widths, headers, rows, total_row=None,
               highlight_rows=None):
    """Boardroom table: deep-green header, alternating cream rows, rounded.

    RULE 23: every column needs a real header. Raises on blank headers."""
    if len(headers) != len(col_widths):
        raise ValueError(f"draw_table: {len(headers)} headers for {len(col_widths)} columns.")
    for i, hdr in enumerate(headers):
        if not str(hdr).strip():
            raise ValueError(f"draw_table: blank header in column {i+1} (rule 23): name every column (e.g. 'Adjustment', 'Component').")
    row_h = 24
    header_h = 30
    table_w = sum(col_widths)
    table_total_h = header_h + len(rows) * row_h + (row_h if total_row else 0)

    if highlight_rows is None:
        highlight_rows = {}

    c.saveState()
    clip_path = c.beginPath()
    clip_path.roundRect(x, y - table_total_h, table_w, table_total_h, CORNER_R)
    c.clipPath(clip_path, stroke=0)

    # Header (deep green + gold text)
    c.setFillColor(DEEP_GREEN)
    c.rect(x, y - header_h, table_w, header_h, fill=1, stroke=0)

    c.setFont(FONT_DISPLAY_BOLD, 10)
    c.setFillColor(GOLD)
    cx = x
    for i, hdr in enumerate(headers):
        c.drawString(cx + 8, y - header_h + 9, hdr)
        cx += col_widths[i]

    cur_y = y - header_h

    # Body rows
    for r, row in enumerate(rows):
        hl = highlight_rows.get(r, None)
        if hl:
            bg = hl.get("bg", CALLOUT_GOLD_BG)
            is_bold = hl.get("bold", False)
            text_color = hl.get("text_color", BODY_COLOR)
        else:
            bg = NEAR_WHITE if r % 2 == 0 else WHITE
            is_bold = False
            text_color = BODY_COLOR

        c.setFillColor(bg)
        c.rect(x, cur_y - row_h, table_w, row_h, fill=1, stroke=0)

        font = FONT_BODY_BOLD if is_bold else FONT_BODY
        c.setFont(font, 9.5)
        c.setFillColor(text_color)
        cx = x
        for i, cell in enumerate(row):
            cell_str = str(cell)
            avail_w = col_widths[i] - 16
            if c.stringWidth(cell_str, font, 9.5) > avail_w:
                lines = _wrap_text(c, cell_str, avail_w, font, 9.5)
                cell_y = cur_y - 8
                for line in lines[:2]:
                    c.drawString(cx + 8, cell_y, line)
                    cell_y -= 11
            else:
                c.drawString(cx + 8, cur_y - row_h + 7, cell_str)
            cx += col_widths[i]
        cur_y -= row_h

    # Total row — gold bar with deep-green text
    if total_row:
        c.setFillColor(GOLD)
        c.rect(x, cur_y - row_h, table_w, row_h, fill=1, stroke=0)

        c.setFont(FONT_DISPLAY_BOLD, 10)
        c.setFillColor(DEEP_GREEN)
        cx = x
        for i, cell in enumerate(total_row):
            c.drawString(cx + 8, cur_y - row_h + 7, str(cell))
            cx += col_widths[i]
        cur_y -= row_h

    c.restoreState()
    return cur_y


# =============================================================================
# TOC
# =============================================================================
def _toc_accent_index(i):
    """Sequence that avoids adjacent color repeats for TOC pills."""
    return [0, 1, 2, 0, 1, 2, 1, 2, 0][i % 9]


def draw_toc(c, x, y, entries, accent_color=None):
    """
    Table of Contents. entries = [{"title": str, "page": int|str}, ...]
    Rendered as dark-green pills with gold page-number chip at the right end.
    """
    entry_h = 36
    gap = 8

    for i, entry in enumerate(entries):
        ey = y - i * (entry_h + gap) - entry_h

        # Main deep-green pill
        c.setFillColor(DEEP_GREEN)
        c.roundRect(x, ey, CONTENT_W, entry_h, CORNER_R, fill=1, stroke=0)

        # Gold page-number chip on the right ~12% of the pill
        chip_w = 60
        c.setFillColor(GOLD)
        c.roundRect(x + CONTENT_W - chip_w, ey, chip_w, entry_h,
                    CORNER_R, fill=1, stroke=0)
        # Square off the chip's left side to blend with the pill's right half
        c.setFillColor(GOLD)
        c.rect(x + CONTENT_W - chip_w, ey, CORNER_R, entry_h,
               fill=1, stroke=0)

        # Serif title in gold on the dark pill
        c.setFont(FONT_DISPLAY_BOLD, 11)
        c.setFillColor(GOLD)
        c.drawString(x + 18, ey + entry_h / 2 - 4, entry.get("title", ""))

        # Page number in deep green on gold chip
        page_str = str(entry.get("page", ""))
        c.setFont(FONT_DISPLAY_BOLD, 12)
        c.setFillColor(DEEP_GREEN)
        c.drawRightString(x + CONTENT_W - 14, ey + entry_h / 2 - 4, page_str)

    total = len(entries) * (entry_h + gap)
    return y - total


# =============================================================================
# M&A-SPECIFIC ELEMENTS
# =============================================================================
def draw_deal_tombstone(c, x, y, w, h, deal_name="", sector="",
                        transaction_value="", role="",
                        close_date="", accent_color=None):
    """
    Deal tombstone block — for closed-deal lists, credentials pages, case studies.
    Layout:
        [deep-green rounded block with thin gold border]
        DEAL_NAME       (serif, gold)
        sector          (kicker)
        transaction     | role         | close
        value           |              | date
    """
    if accent_color is None:
        accent_color = GOLD

    # Outer dark block with gold border
    c.setFillColor(accent_color)
    c.roundRect(x, y, w, h, CORNER_R, fill=1, stroke=0)
    c.setFillColor(DEEP_GREEN)
    c.roundRect(x + 1.5, y + 1.5, w - 3, h - 3, CORNER_R, fill=1, stroke=0)

    # Deal name — serif, gold, top
    if deal_name:
        c.setFont(FONT_DISPLAY_BOLD, 14)
        c.setFillColor(GOLD)
        c.drawString(x + 18, y + h - 26, deal_name)

    # Sector kicker
    if sector:
        c.setFont(FONT_BODY_BOLD, 8)
        c.setFillColor(HexColor("#C4B890"))
        char_x = x + 18
        for ch in sector.upper():
            c.drawString(char_x, y + h - 42, ch)
            char_x += c.stringWidth(ch, FONT_BODY_BOLD, 8) + 1.4

    # Three-column details row at bottom
    labels = [("VALUE", transaction_value), ("ROLE", role), ("CLOSED", close_date)]
    col_w = (w - 36) / 3
    for i, (label, value) in enumerate(labels):
        cx = x + 18 + i * col_w
        c.setFont(FONT_BODY, 7)
        c.setFillColor(HexColor("#8A9995"))
        c.drawString(cx, y + 24, label)
        c.setFont(FONT_DISPLAY_BOLD, 11)
        c.setFillColor(WHITE)
        c.drawString(cx, y + 10, value or "-")

    return y


def draw_deal_tombstone_grid(c, x, y, deals, cols=2, h=80, gap=12):
    """Grid of deal tombstones — for tombstone walls / credentials pages."""
    card_w = (CONTENT_W - gap * (cols - 1)) / cols
    n = len(deals)
    rows = (n + cols - 1) // cols

    for i, deal in enumerate(deals):
        col = i % cols
        row = i // cols
        cx = x + col * (card_w + gap)
        cy = y - (row + 1) * h - row * gap
        draw_deal_tombstone(c, cx, cy, card_w, h, **deal)

    return y - rows * h - (rows - 1) * gap
