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
        c.setFont(FONT_BODY_BOLD, 8)
        c.setFillColor(accent_color)
        label_upper = label.upper()
        # Letter-spaced label for editorial feel
        char_x = x
        total_w = 0
        for ch in label_upper:
            total_w += c.stringWidth(ch, FONT_BODY_BOLD, 8) + 1.2
        char_x = x + (w - total_w) / 2
        for ch in label_upper:
            c.drawString(char_x, y + 12, ch)
            char_x += c.stringWidth(ch, FONT_BODY_BOLD, 8) + 1.2

    return y


def draw_stat_row(c, x, y, stats, gap=12):
    """Row of stat boxes with enforced color adjacency. Returns y below."""
    n = len(stats)
    if n == 0:
        return y
    box_w = (CONTENT_W - gap * (n - 1)) / n
    box_h = 82

    prev_color = None
    for i, stat in enumerate(stats):
        sx = x + i * (box_w + gap)
        color = get_accent_color(i, prev_color)
        draw_stat_box(c, sx, y - box_h, box_w, box_h,
                      number=stat.get("number", ""),
                      label=stat.get("label", ""),
                      accent_color=color)
        prev_color = color

    return y - box_h


def draw_numbered_card(c, x, y, w, h, number=1, kicker="", title="", body="",
                       accent_color=None, accent_index=0, shadow=True):
    """Card with numbered circle badge. USE FOR MODULES / STEPS / PHASES."""
    if accent_color is None:
        accent_color = ACCENT_ROTATION[accent_index % len(ACCENT_ROTATION)]

    draw_card(c, x, y, w, h, accent_color=accent_color,
              accent_position="left", shadow=shadow)

    circle_r = 14
    circle_x = x + ACCENT_W + 16 + circle_r
    circle_y = y + h - 18 - circle_r

    c.setFillColor(accent_color)
    c.circle(circle_x, circle_y, circle_r, fill=1, stroke=0)
    c.setFont(FONT_DISPLAY_BOLD, 13)
    c.setFillColor(WHITE)
    num_str = str(number)
    num_w = c.stringWidth(num_str, FONT_DISPLAY_BOLD, 13)
    c.drawString(circle_x - num_w / 2, circle_y - 4.5, num_str)

    text_left = circle_x + circle_r + 10
    text_max_w = x + w - text_left - 16

    if kicker:
        c.setFont(FONT_BODY_BOLD, 8)
        c.setFillColor(accent_color)
        c.drawString(text_left, circle_y + 6, kicker.upper())

    if title:
        title_y = circle_y - 10 if kicker else circle_y + 2
        c.setFont(FONT_DISPLAY_BOLD, 13)
        c.setFillColor(DEEP_GREEN)
        c.drawString(text_left, title_y, title)

    if body:
        body_x = x + ACCENT_W + 16
        body_y = circle_y - circle_r - 14
        max_w = w - ACCENT_W - 32
        _wrap_and_draw(c, body, body_x, body_y, max_w,
                       FONT_BODY, 10, 13, BODY_COLOR)

    return y
