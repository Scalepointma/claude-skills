"""
ScalePoint M&A PDF Cards — Card, Card Grid, Stat Box, Numbered Card.
White cards with gold/teal/olive accent bars.
"""

from scalepoint_base import *


def calculate_card_height(c, title="", body="", width=None, padding=16):
    """Calculate minimum card height for given content."""
    if width is None:
        width = (CONTENT_W - 12) / 2
    inner_w = width - padding * 2 - ACCENT_W
    h = padding
    if title:
        h += 20  # serif title sits a bit taller
    if body:
        h += measure_text_height(c, body, inner_w, FONT_BODY, 10, 13)
        h += 8
    return max(92, h + padding)


def draw_card(c, x, y, w, h, title="", body="", accent_color=None,
              accent_position="left", shadow=True, accent_index=0):
    """
    White card with accent bar (two-box technique):
    1. Rounded rect in accent color (full size)
    2. Smaller white rounded rect on top, offset to reveal accent edge
    """
    if accent_color is None:
        accent_color = ACCENT_ROTATION[accent_index % len(ACCENT_ROTATION)]

    if shadow:
        _draw_shadow(c, x, y, w, h)

    c.setFillColor(accent_color)
    c.roundRect(x, y, w, h, CORNER_R, fill=1, stroke=0)

    if accent_position == "left":
        c.setFillColor(WHITE)
        c.roundRect(x + ACCENT_W, y, w - ACCENT_W, h, CORNER_R,
                    fill=1, stroke=0)
    elif accent_position == "top":
        c.setFillColor(WHITE)
        c.roundRect(x, y, w, h - ACCENT_W, CORNER_R, fill=1, stroke=0)

    if title:
        tx = x + 16 + (ACCENT_W if accent_position == "left" else 0)
        ty = y + h - 22 - (ACCENT_W if accent_position == "top" else 0)
        c.setFont(FONT_DISPLAY_BOLD, 13)
        c.setFillColor(DEEP_GREEN)
        c.drawString(tx, ty, title)

    if body:
        tx = x + 16 + (ACCENT_W if accent_position == "left" else 0)
        ty_start = y + h - 40 - (ACCENT_W if accent_position == "top" else 0)
        max_w = w - 32 - (ACCENT_W if accent_position == "left" else 0)
        _wrap_and_draw(c, body, tx, ty_start, max_w,
                       FONT_BODY, 10, 13, BODY_COLOR)

    return y


def _grid_accent_index(i, cols):
    """Color rotation that avoids neighboring duplicates (horizontal + vertical)."""
    candidate = i % len(ACCENT_ROTATION)
    left_idx  = (i - 1) % len(ACCENT_ROTATION) if i % cols != 0 else -1
    above_idx = (i - cols) % len(ACCENT_ROTATION) if i >= cols else -1

    left_color  = ACCENT_ROTATION[left_idx]  if left_idx  >= 0 else None
    above_color = ACCENT_ROTATION[above_idx] if above_idx >= 0 else None

    attempts = 0
    while attempts < len(ACCENT_ROTATION):
        color = ACCENT_ROTATION[candidate % len(ACCENT_ROTATION)]
        if not ((left_color and color == left_color) or
                (above_color and color == above_color)):
            break
        candidate += 1
        attempts += 1

    return candidate % len(ACCENT_ROTATION)


def draw_card_grid(c, x, y, cards, cols=2, card_w=None, card_h=120,
                   gap=12, accent_position="left", auto_height=False):
    """Grid of cards with color-adjacency checks. Returns y below the grid."""
    if card_w is None:
        card_w = (CONTENT_W - gap * (cols - 1)) / cols

    row_heights = {}
    if auto_height:
        for i, card in enumerate(cards):
            row = i // cols
            h = calculate_card_height(c, card.get("title", ""),
                                      card.get("body", ""), card_w)
            row_heights[row] = max(row_heights.get(row, 92), h)

    cur_y = y
    for i, card in enumerate(cards):
        col = i % cols
        row = i // cols
        h = row_heights.get(row, card_h) if auto_height else card_h

        cx = x + col * (card_w + gap)
        row_y = y
        for r in range(row):
            row_y -= (row_heights.get(r, card_h) if auto_height else card_h) + gap
        cy = row_y - h

        ai = _grid_accent_index(i, cols)
        draw_card(c, cx, cy, card_w, h,
                  title=card.get("title", ""),
                  body=card.get("body", ""),
                  accent_position=accent_position,
                  accent_index=ai)

        if col == cols - 1 or i == len(cards) - 1:
            cur_y = cy

    return cur_y


def draw_stat_box(c, x, y, w, h, number="", label="", accent_color=None,
                  accent_index=0, shadow=True):
    """Stat box: big serif number + small uppercase sans label. Top accent bar."""
    if accent_color is None:
        accent_color = ACCENT_ROTATION[accent_index % len(ACCENT_ROTATION)]

    if shadow:
        _draw_shadow(c, x, y, w, h)

    c.setFillColor(accent_color)
    c.roundRect(x, y, w, h, CORNER_R, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.roundRect(x, y, w, h - ACCENT_W, CORNER_R, fill=1, stroke=0)

    if number:
        c.setFont(FONT_DISPLAY_BOLD, 34)
        c.setFillColor(DEEP_GREEN)
        num_w = c.stringWidth(str(number), FONT_DISPLAY_BOLD, 34)
        c.drawString(x + (w - num_w) / 2, y + h / 2 - 2, str(number))

    if label:
        # RULE 22: descriptor is ALWAYS the standard gold, regardless of
        # the accent bar colour.
        draw_descriptor(c, x + w / 2, y + 12, label)

    return y


def draw_stat_row(c, x, y, stats, gap=12, accent_color=None):
    """Row of stat boxes, ONE accent colour for the whole row (rule 3/13).
    Default GOLD. For a second stat row on the same page, pass
    accent_color=DEEP_GREEN to break up the gold. Returns y below."""
    n = len(stats)
    if n == 0:
        return y
    if accent_color is None:
        accent_color = GOLD
    box_w = (CONTENT_W - gap * (n - 1)) / n
    box_h = 82

    for i, stat in enumerate(stats):
        sx = x + i * (box_w + gap)
        draw_stat_box(c, sx, y - box_h, box_w, box_h,
                      number=stat.get("number", ""),
                      label=stat.get("label", ""),
                      accent_color=accent_color)

    return y - box_h


def draw_numbered_card(c, x, y, w, h, number=1, kicker="", title="", body="",
                       accent_color=None, badge_color=None, accent_index=0,
                       shadow=True):
    """Card with numbered circle badge. USE FOR MODULES / STEPS / PHASES.

    RULE 13: default = GOLD card accent + DEEP-GREEN number badge (the green
    badge cuts the gold). RULE 7: for single-line rows (no body), the badge
    and title are vertically CENTERED in the card, and the numeral is
    centered within its circle."""
    if accent_color is None:
        accent_color = GOLD
    if badge_color is None:
        badge_color = DEEP_GREEN

    draw_card(c, x, y, w, h, accent_color=accent_color,
              accent_position="left", shadow=shadow)

    circle_r = 13
    circle_x = x + ACCENT_W + 16 + circle_r
    single_line = bool(title) and not body and not kicker
    # Rule 7: center vertically for single-line rows; top-align otherwise
    circle_y = y + h / 2 if single_line else y + h - 18 - circle_r

    c.setFillColor(badge_color)
    c.circle(circle_x, circle_y, circle_r, fill=1, stroke=0)
    c.setFont(FONT_DISPLAY_BOLD, 13)
    c.setFillColor(WHITE)
    # numeral centered in its circle (optical centre: half cap-height down)
    c.drawCentredString(circle_x, circle_y - 4.5, str(number))

    text_left = circle_x + circle_r + 12

    if kicker:
        spaced(c, text_left, circle_y + 6, kicker.upper(),
               FONT_BODY_BOLD, LABEL_SIZE, LABEL_GOLD, 1.0)

    if title:
        title_y = (circle_y - 4.5) if single_line else \
                  (circle_y - 10 if kicker else circle_y + 2)
        c.setFont(FONT_DISPLAY_BOLD, 12.5)
        c.setFillColor(DEEP_GREEN)
        c.drawString(text_left, title_y, title)

    if body:
        body_x = x + ACCENT_W + 16
        body_y = circle_y - circle_r - 14
        max_w = w - ACCENT_W - 32
        _wrap_and_draw(c, body, body_x, body_y, max_w,
                       FONT_BODY, 10, 13, BODY_COLOR)

    return y


# =============================================================================
# DELIBERATE COLOUR-BALANCED GRIDS (rules 13 & 20) + VALUE CARDS (rule 22)
# =============================================================================
def card_grid_rows(c, x, y, cards, cols, row_colors=None, gap=14):
    """Card grid where each ROW uses one accent colour — the approved way to
    break up gold in a highlight grid (rule 13): row1 GOLD, row2 DEEP_GREEN,
    row3 OLIVE. Returns y below the grid."""
    if row_colors is None:
        row_colors = [GOLD, DEEP_GREEN, OLIVE]
    cw = (CONTENT_W - gap * (cols - 1)) / cols
    rh = {}
    for i, cd in enumerate(cards):
        r = i // cols
        rh[r] = max(rh.get(r, 92),
                    calculate_card_height(c, cd.get("title", ""), cd.get("body", ""), cw))
    for i, cd in enumerate(cards):
        col = i % cols
        r = i // cols
        cx = x + col * (cw + gap)
        row_y = y
        for rr in range(r):
            row_y -= rh[rr] + gap
        draw_card(c, cx, row_y - rh[r], cw, rh[r],
                  title=cd.get("title", ""), body=cd.get("body", ""),
                  accent_color=row_colors[r % len(row_colors)])
    return y - (sum(rh.values()) + gap * (len(rh) - 1))


def cards_colored(c, x, y, cards, colors=None, cols=3, gap=14):
    """One row of cards, each with its own accent colour (e.g. persona cards:
    GOLD / DEEP_GREEN / OLIVE). Returns y below the row."""
    if colors is None:
        colors = [GOLD, DEEP_GREEN, OLIVE]
    cw = (CONTENT_W - gap * (cols - 1)) / cols
    h = max(calculate_card_height(c, cd.get("title", ""), cd.get("body", ""), cw)
            for cd in cards)
    for i, cd in enumerate(cards):
        draw_card(c, x + i * (cw + gap), y - h, cw, h,
                  title=cd.get("title", ""), body=cd.get("body", ""),
                  accent_color=colors[i % len(colors)])
    return y - h


def kv_card(c, x, y, w, h, value, label, accent_color=None):
    """Value card: serif value + THE standard descriptor (rule 22)."""
    if accent_color is None:
        accent_color = GOLD
    draw_card(c, x, y, w, h, accent_color=accent_color, accent_position="left")
    tx = x + ACCENT_W + 16
    c.setFont(FONT_DISPLAY_BOLD, 15)
    c.setFillColor(DEEP_GREEN)
    c.drawString(tx, y + h - 30, str(value))
    spaced(c, tx, y + 16, label.upper(), FONT_BODY_BOLD, LABEL_SIZE, LABEL_GOLD, 1.0)


def cards_by_column(c, x, y, cards, cols, col_colors=None, card_h=72, gap=12):
    """Value-card grid; each COLUMN (stack) uses one accent colour so the
    palette balances EVENLY (rule 20: for a 6-up grid, 2 gold / 2 green /
    2 olive by column). cards = [{"title": value, "body": label}, ...]"""
    import math
    if col_colors is None:
        col_colors = [GOLD, DEEP_GREEN, OLIVE]
    cw = (CONTENT_W - gap * (cols - 1)) / cols
    rows = math.ceil(len(cards) / cols)
    for i, cd in enumerate(cards):
        col = i % cols
        r = i // cols
        kv_card(c, x + col * (cw + gap), y - r * (card_h + gap) - card_h, cw, card_h,
                cd["title"], cd["body"], col_colors[col % len(col_colors)])
    return y - (rows * card_h + (rows - 1) * gap)
