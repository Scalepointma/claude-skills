"""
ScalePoint M&A PDF Layouts — Brochure pillars, bento, two-column,
duotone photo treatment, gold topographic motif.

The duotone + gold-wave treatment is the ScalePoint "social media kit"
look: photos get a dark-green duotone + gold flowing lines.
"""

import math
import os
from scalepoint_base import *
from scalepoint_cards import draw_card, draw_card_grid, calculate_card_height


# =============================================================================
# DUOTONE PHOTO + GOLD MOTIF
# =============================================================================
def _make_duotone(img_path, dark_hex="#0A2D2A", light_hex="#E8E4D7"):
    """
    Convert a photo to a dark-green duotone. Returns path to cached file.
    Falls back to original on any error.
    """
    try:
        from PIL import Image, ImageOps
        img = Image.open(img_path).convert("L")   # grayscale
        # Build gradient map from dark to light
        def hx(h):
            h = h.lstrip("#")
            return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
        dark, light = hx(dark_hex), hx(light_hex)
        lut = []
        for i in range(256):
            t = i / 255.0
            r = int(dark[0] + (light[0] - dark[0]) * t)
            g = int(dark[1] + (light[1] - dark[1]) * t)
            b = int(dark[2] + (light[2] - dark[2]) * t)
            lut.extend([r, g, b])
        duo = ImageOps.colorize(img, black=dark_hex, white=light_hex)
        out = img_path.rsplit(".", 1)[0] + "_duotone.jpg"
        duo.save(out, quality=88)
        return out
    except Exception:
        return img_path


def draw_duotone_hero(c, x, y_top, w, h, image_path=None,
                      overlay_opacity=0.55, gold_waves=True,
                      wave_density=9):
    """
    Hero panel with duotone photo + optional gold topographic waves — the
    ScalePoint "social media kit" treatment. Returns y of the bottom edge.

    - overlay_opacity: 0 (photo untouched) to 0.9 (nearly solid green)
    - gold_waves: overlay gold flowing lines across the panel
    - wave_density: number of wave lines
    """
    y_bottom = y_top - h

    # Fill: dark green as base (in case photo fails)
    c.setFillColor(DEEP_GREEN)
    c.saveState()
    clip = c.beginPath()
    clip.roundRect(x, y_bottom, w, h, CORNER_R)
    c.clipPath(clip, stroke=0)

    # Duotone photo (draw into the clipped path)
    if image_path and os.path.isfile(image_path):
        duo_path = _make_duotone(image_path)
        try:
            c.drawImage(duo_path, x, y_bottom, w, h,
                        preserveAspectRatio=True, anchor='c')
        except Exception:
            c.rect(x, y_bottom, w, h, fill=1, stroke=0)
    else:
        c.rect(x, y_bottom, w, h, fill=1, stroke=0)

    # Dark green overlay on top of photo to push tonal range down
    c.setFillColor(Color(10/255, 45/255, 42/255, overlay_opacity))
    c.rect(x, y_bottom, w, h, fill=1, stroke=0)

    # Gold topographic waves (sinusoidal lines radiating from upper-left)
    if gold_waves:
        c.setStrokeColor(GOLD)
        c.setLineWidth(0.7)
        amp_base = h * 0.05
        spacing = h / (wave_density + 2)
        for i in range(wave_density):
            offset = i * spacing
            amp = amp_base * (1 - i / (wave_density * 2))
            path = c.beginPath()
            started = False
            steps = 60
            for s in range(steps + 1):
                t = s / steps
                px = x + t * w
                py = y_top - offset - amp * math.sin(t * math.pi * 2.8 + i * 0.4)
                if not started:
                    path.moveTo(px, py)
                    started = True
                else:
                    path.lineTo(px, py)
            c.drawPath(path, fill=0, stroke=1)

    c.restoreState()

    # Gold frame outline for polish
    c.setStrokeColor(GOLD)
    c.setLineWidth(1.2)
    c.roundRect(x, y_bottom, w, h, CORNER_R, fill=0, stroke=1)

    return y_bottom


def draw_logo_pill(c, x, y, w, h, logo_icon_path=None, logo_text="SCALEPOINT M&A"):
    """
    Draw the signature gold-outlined logo pill: [icon] | SCALEPOINT M&A.
    Mimics the social media kit lockup. Place over a hero or solid panel.
    Background behind pill is assumed to be dark (for gold to contrast).
    """
    # Gold outline
    c.setStrokeColor(GOLD)
    c.setLineWidth(1.5)
    c.setFillColor(Color(0, 0, 0, 0))
    c.roundRect(x, y, w, h, 8, fill=0, stroke=1)

    # Divider at icon-box end
    icon_box_w = h  # square icon box on the left
    c.line(x + icon_box_w, y, x + icon_box_w, y + h)

    # Icon (if path provided; else fallback triangle)
    if logo_icon_path and os.path.isfile(logo_icon_path):
        try:
            pad = 6
            c.drawImage(logo_icon_path, x + pad, y + pad,
                        icon_box_w - 2 * pad, h - 2 * pad,
                        preserveAspectRatio=True, mask='auto')
        except Exception:
            pass

    # Wordmark — serif, gold
    c.setFont(FONT_DISPLAY_BOLD, h * 0.45)
    c.setFillColor(GOLD)
    c.drawCentredString(x + icon_box_w + (w - icon_box_w) / 2,
                        y + h * 0.32, logo_text)


# =============================================================================
# BROCHURE PILLAR ROW  — Build / Buy / Sell equivalent
# =============================================================================
def draw_pillar_row(c, x, y_top, pillars, image_h=80, card_h=140, gap=12,
                    images_as_duotone=True):
    """
    3-column pillar overview, mirrors the Canva template's Planning/Launching/
    Elevate row. Each pillar: [small photo band] / [solid color band with
    title + body].

    pillars = [{"title": "BUILD", "body": "...", "image": path}, ...]

    Total height = image_h + card_h. Returns y below the whole row.
    """
    n = len(pillars)
    if n == 0:
        return y_top
    col_w = (CONTENT_W - gap * (n - 1)) / n
    y_image_top = y_top
    y_image_bot = y_image_top - image_h
    y_card_top = y_image_bot
    y_card_bot = y_card_top - card_h

    for i, p in enumerate(pillars):
        cx = x + i * (col_w + gap)

        # Top image band
        img_path = p.get("image")
        c.saveState()
        clip = c.beginPath()
        clip.roundRect(cx, y_image_bot, col_w, image_h, CORNER_R)
        c.clipPath(clip, stroke=0)
        if img_path and os.path.isfile(img_path):
            path_use = _make_duotone(img_path) if images_as_duotone else img_path
            try:
                c.drawImage(path_use, cx, y_image_bot, col_w, image_h,
                            preserveAspectRatio=True, anchor='c')
                if images_as_duotone:
                    c.setFillColor(Color(10/255, 45/255, 42/255, 0.35))
                    c.rect(cx, y_image_bot, col_w, image_h, fill=1, stroke=0)
            except Exception:
                c.setFillColor(DEEP_GREEN)
                c.rect(cx, y_image_bot, col_w, image_h, fill=1, stroke=0)
        else:
            c.setFillColor(DEEP_GREEN)
            c.rect(cx, y_image_bot, col_w, image_h, fill=1, stroke=0)
        c.restoreState()

        # Bottom text card — deep green block with gold title & white body
        c.setFillColor(DEEP_GREEN)
        c.rect(cx, y_card_bot, col_w, card_h, fill=0, stroke=0)
        # Solid green block (we want a flat rectangle that butts to the image)
        c.setFillColor(DEEP_GREEN)
        c.rect(cx, y_card_bot, col_w, card_h, fill=1, stroke=0)
        # Thin gold accent at top of card (just inside image seam)
        c.setFillColor(GOLD)
        c.rect(cx, y_card_top - 3, col_w, 3, fill=1, stroke=0)

        # Title — gold serif centered
        title = p.get("title", "")
        if title:
            c.setFont(FONT_DISPLAY_BOLD, 16)
            c.setFillColor(GOLD)
            c.drawCentredString(cx + col_w / 2, y_card_top - 24, title.upper())

        # Body text — off-white, centered block
        body = p.get("body", "")
        if body:
            c.setFont(FONT_BODY, 9.5)
            c.setFillColor(HexColor("#E8E4D7"))
            lines = _wrap_text(c, body, col_w - 24, FONT_BODY, 9.5)
            text_y = y_card_top - 46
            for line in lines[:7]:
                c.drawCentredString(cx + col_w / 2, text_y, line)
                text_y -= 12

    return y_card_bot


# =============================================================================
# CONTACT STRIP  — Canva-template style CTA footer
# =============================================================================
def draw_contact_strip(c, x, y, w=None, phone="", email="", website="",
                       cta_text="START A CONVERSATION", h=36):
    """
    Gold CTA button centered over a deep-green contact bar.
    Returns y below the strip.
    """
    if w is None:
        w = CONTENT_W

    # Gold CTA button (centered, floating above)
    btn_w = 240
    btn_h = h
    btn_x = x + (w - btn_w) / 2
    btn_y = y - btn_h / 2
    c.setFillColor(GOLD)
    c.roundRect(btn_x, btn_y, btn_w, btn_h, CORNER_R, fill=1, stroke=0)
    c.setFont(FONT_DISPLAY_BOLD, 12)
    c.setFillColor(DEEP_GREEN)
    c.drawCentredString(btn_x + btn_w / 2, btn_y + btn_h * 0.35, cta_text)

    # Deep-green contact bar underneath
    bar_h = 32
    bar_y = y - btn_h / 2 - bar_h + 8
    c.setFillColor(DEEP_GREEN)
    c.roundRect(x, bar_y, w, bar_h, CORNER_R, fill=1, stroke=0)

    # Contact text inside
    c.setFont(FONT_BODY, 9)
    c.setFillColor(GOLD_LIGHT)
    items = [s for s in [phone, email, website] if s]
    if items:
        sep = "   \u2022   "
        text = sep.join(items)
        c.drawCentredString(x + w / 2, bar_y + bar_h / 2 - 3, text)

    return bar_y - 6


# =============================================================================
# BENTO (unchanged API, ScalePoint colors)
# =============================================================================
def draw_bento_layout(c, x, y, items, style="A", gap=12):
    """
    Bento-box layout — mixed-size cards in asymmetric grid. Use sparingly.
    Styles: A (1 large + 2 stacked right), B (1 wide top + 3 below),
    C (1 tall left + 3 stacked right).
    """
    if style == "A" and len(items) >= 3:
        left_w = (CONTENT_W * 2 / 3) - gap / 2
        right_w = (CONTENT_W * 1 / 3) - gap / 2
        total_h = 220
        right_h = (total_h - gap) / 2

        c0 = get_accent_color(0)
        draw_card(c, x, y - total_h, left_w, total_h,
                  title=items[0].get("title", ""),
                  body=items[0].get("body", ""),
                  accent_color=c0,
                  accent_position="left")

        rx = x + left_w + gap
        c1 = get_accent_color(1, c0)
        draw_card(c, rx, y - right_h, right_w, right_h,
                  title=items[1].get("title", ""),
                  body=items[1].get("body", ""),
                  accent_color=c1,
                  accent_position="left")

        c2 = get_accent_color(2, c1)
        if c2 == c0:
            c2 = get_accent_color(3, c0)
        draw_card(c, rx, y - total_h, right_w, right_h,
                  title=items[2].get("title", ""),
                  body=items[2].get("body", ""),
                  accent_color=c2,
                  accent_position="left")

        return y - total_h

    elif style == "B" and len(items) >= 4:
        top_h = 80
        bottom_h = 120
        card_w = (CONTENT_W - gap * 2) / 3

        c0 = get_accent_color(0)
        draw_card(c, x, y - top_h, CONTENT_W, top_h,
                  title=items[0].get("title", ""),
                  body=items[0].get("body", ""),
                  accent_color=c0,
                  accent_position="top")

        by = y - top_h - gap
        prev = c0
        for i in range(3):
            cx = x + i * (card_w + gap)
            color = get_accent_color(i + 1, prev)
            draw_card(c, cx, by - bottom_h, card_w, bottom_h,
                      title=items[i + 1].get("title", ""),
                      body=items[i + 1].get("body", ""),
                      accent_color=color,
                      accent_position="left")
            prev = color

        return by - bottom_h

    elif style == "C" and len(items) >= 4:
        left_w = CONTENT_W / 2 - gap / 2
        right_w = CONTENT_W / 2 - gap / 2
        total_h = 240
        right_h = (total_h - gap * 2) / 3

        c0 = get_accent_color(0)
        draw_card(c, x, y - total_h, left_w, total_h,
                  title=items[0].get("title", ""),
                  body=items[0].get("body", ""),
                  accent_color=c0,
                  accent_position="left")

        rx = x + left_w + gap
        prev = c0
        for i in range(3):
            ry = y - (i * (right_h + gap)) - right_h
            color = get_accent_color(i + 1, prev)
            if color == c0:
                color = get_accent_color(i + 2, prev)
            draw_card(c, rx, ry, right_w, right_h,
                      title=items[i + 1].get("title", ""),
                      body=items[i + 1].get("body", ""),
                      accent_color=color,
                      accent_position="left")
            prev = color

        return y - total_h

    else:
        return draw_card_grid(c, x, y, items, cols=2)


def get_two_column_x(col, gap=24):
    """Get (x, width) for a 2-column layout. col: 0 (left) or 1 (right)."""
    col_w = (CONTENT_W - gap) / 2
    if col == 0:
        return MARGIN, col_w
    else:
        return MARGIN + col_w + gap, col_w
