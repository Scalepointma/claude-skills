"""
ScalePoint M&A PDF Covers — Front Cover, Back Cover, Brochure Hero.

Three cover/hero styles:
- draw_front_cover(): full-bleed dark green + stacked gold/white logo,
  serif title, gold accent rule. Used for boardroom reports / CIMs.
- draw_brochure_hero(): hero IMAGE with title pill overlaid — matches the
  Canva-style brochure vibe for Build/Buy/Sell leave-behinds.
- draw_back_cover(): deep-green back cover with contact info + tagline.
"""

from scalepoint_base import *
import os


def _prepare_image_for_page(img_path, target_w, target_h):
    """Return path to the image, preferring a crop that fills target dims.
    ReportLab handles stretching via preserveAspectRatio='auto', but we
    pre-orient landscape source images toward landscape panels and vice versa.
    """
    try:
        from PIL import Image
        img = Image.open(img_path)
        iw, ih = img.size
        want_landscape = target_w >= target_h
        is_landscape = iw >= ih
        if want_landscape != is_landscape:
            # Rotate 90 degrees to match the panel orientation
            rotated = img.rotate(-90, expand=True)
            rotated_path = img_path.rsplit(".", 1)[0] + "_rot.jpg"
            rotated.save(rotated_path, quality=92)
            return rotated_path
        return img_path
    except Exception:
        return img_path


# =============================================================================
# FRONT COVER — boardroom report style
# =============================================================================
def draw_front_cover(c, title="", subtitle="", date="", logo_stacked_path=None,
                     cover_bg_path=None):
    """
    Formal front cover — for CIMs, valuation reports, proposals.
    Dark green full-bleed + gold accent rule + stacked logo + serif title.
    If cover_bg_path is provided, it overrides the solid green with a photo
    (still tinted dark for text legibility).
    """
    # Full-bleed deep green
    c.setFillColor(DEEP_GREEN)
    c.rect(0, 0, W, H, fill=1, stroke=0)

    # Optional photo backdrop (with dark overlay)
    if cover_bg_path and os.path.isfile(cover_bg_path):
        try:
            prepared = _prepare_image_for_page(cover_bg_path, W, H)
            c.drawImage(prepared, 0, 0, W, H,
                        preserveAspectRatio=True, anchor='c')
            # Dark overlay for legibility
            c.setFillColor(Color(10/255, 45/255, 42/255, 0.75))
            c.rect(0, 0, W, H, fill=1, stroke=0)
        except Exception:
            pass

    # Gold vertical accent rule on the left edge (echoes brand-guide cover)
    c.setFillColor(GOLD)
    c.rect(MARGIN - 20, MARGIN, 6, H - MARGIN * 2, fill=1, stroke=0)

    # Stacked logo in the upper center
    if logo_stacked_path and os.path.isfile(logo_stacked_path):
        try:
            logo_w, logo_h = 200, 140
            c.drawImage(logo_stacked_path,
                        W / 2 - logo_w / 2, H * 0.68,
                        logo_w, logo_h,
                        preserveAspectRatio=True, mask='auto')
        except Exception:
            pass
    else:
        # Fallback: text-only cover title
        c.setFont(FONT_DISPLAY_BOLD, 28)
        c.setFillColor(GOLD)
        c.drawCentredString(W / 2, H * 0.72, "SCALEPOINT M&A")

    # Thin gold horizontal accent rule
    rule_w = 140
    c.setFillColor(GOLD)
    c.rect(W / 2 - rule_w / 2, H * 0.58, rule_w, 2, fill=1, stroke=0)

    # Title (serif, off-white)
    if title:
        c.setFont(FONT_DISPLAY_BOLD, 30)
        c.setFillColor(WHITE)
        # Wrap long titles to two lines
        if c.stringWidth(title, FONT_DISPLAY_BOLD, 30) > W - 100:
            words = title.split()
            mid = len(words) // 2
            line1 = " ".join(words[:mid])
            line2 = " ".join(words[mid:])
            c.drawCentredString(W / 2, H * 0.50, line1)
            c.drawCentredString(W / 2, H * 0.50 - 36, line2)
        else:
            c.drawCentredString(W / 2, H * 0.50, title)

    # Subtitle (italic serif, gold)
    if subtitle:
        c.setFont("Times-Italic", 14)
        c.setFillColor(GOLD_LIGHT)
        c.drawCentredString(W / 2, H * 0.40, subtitle)

    # Date (sans, muted)
    if date:
        c.setFont(FONT_BODY, 10)
        c.setFillColor(HexColor("#C4B890"))
        c.drawCentredString(W / 2, H * 0.08, date.upper())

    # Gold baseline rule
    c.setFillColor(GOLD)
    c.rect(MARGIN, 70, W - 2 * MARGIN, 1.5, fill=1, stroke=0)


# =============================================================================
# BROCHURE HERO — Canva-style leave-behind cover
# =============================================================================
def draw_brochure_hero(c, y_top, height, hero_image_path, title_text="",
                       subtitle_text="", title_pill_bg=None,
                       subtitle_pill_bg=None):
    """
    Photo-driven hero band with title pill + subtitle pill overlaid.
    Use for brochures, one-pagers, leave-behinds.

    - y_top: top y of the hero band (usually CONTENT_TOP or H - MARGIN)
    - height: hero band height (typical: 220–280pt)
    - hero_image_path: path to photo to fill the band (full-bleed to margins)
    - title_text: bold serif (short, e.g., "BUILD. BUY. SELL.")
    - subtitle_text: shorter sans uppercase strapline
    """
    if title_pill_bg is None:
        title_pill_bg = WHITE
    if subtitle_pill_bg is None:
        subtitle_pill_bg = DEEP_GREEN

    x = MARGIN
    w = CONTENT_W
    y_bottom = y_top - height

    # Photo panel (full content width)
    if hero_image_path and os.path.isfile(hero_image_path):
        try:
            prepared = _prepare_image_for_page(hero_image_path, w, height)
            c.saveState()
            # Clip to rounded rect so the photo has soft corners
            clip = c.beginPath()
            clip.roundRect(x, y_bottom, w, height, CORNER_R)
            c.clipPath(clip, stroke=0)
            c.drawImage(prepared, x, y_bottom, w, height,
                        preserveAspectRatio=True, anchor='c',
                        preserveAspectRatio_kwarg=True) \
                if False else c.drawImage(prepared, x, y_bottom, w, height,
                                          preserveAspectRatio=True, anchor='c')
            c.restoreState()
        except Exception:
            # Fallback: solid deep-green panel
            c.setFillColor(DEEP_GREEN)
            c.roundRect(x, y_bottom, w, height, CORNER_R, fill=1, stroke=0)
    else:
        c.setFillColor(DEEP_GREEN)
        c.roundRect(x, y_bottom, w, height, CORNER_R, fill=1, stroke=0)

    # Subtle gold frame for polish
    c.setStrokeColor(GOLD)
    c.setLineWidth(1.2)
    c.roundRect(x, y_bottom, w, height, CORNER_R, fill=0, stroke=1)

    # Title pill — center-low on the hero (like the Canva template)
    if title_text:
        pill_font = FONT_DISPLAY_BOLD
        pill_size = 22
        pad_x, pad_y = 24, 14
        text_w = c.stringWidth(title_text, pill_font, pill_size)
        pill_w = text_w + pad_x * 2
        pill_h = pill_size + pad_y
        pill_x = x + (w - pill_w) / 2
        pill_y = y_bottom + height * 0.35

        # Shadow for depth
        _draw_shadow(c, pill_x, pill_y, pill_w, pill_h, opacity=0.18)
        c.setFillColor(title_pill_bg)
        c.roundRect(pill_x, pill_y, pill_w, pill_h, CORNER_R, fill=1, stroke=0)
        c.setFont(pill_font, pill_size)
        c.setFillColor(DEEP_GREEN)
        c.drawCentredString(pill_x + pill_w / 2,
                            pill_y + pad_y * 0.8, title_text)

    # Subtitle pill — sits just below the title pill
    if subtitle_text:
        sub_font = FONT_BODY_BOLD
        sub_size = 11
        pad_x, pad_y = 20, 10
        text_w = c.stringWidth(subtitle_text.upper(), sub_font, sub_size)
        pill_w = text_w + pad_x * 2
        pill_h = sub_size + pad_y
        pill_x = x + (w - pill_w) / 2
        pill_y = y_bottom + height * 0.18

        c.setFillColor(subtitle_pill_bg)
        c.roundRect(pill_x, pill_y, pill_w, pill_h, CORNER_R, fill=1, stroke=0)
        c.setFont(sub_font, sub_size)
        c.setFillColor(GOLD)
        c.drawCentredString(pill_x + pill_w / 2,
                            pill_y + pad_y * 0.75, subtitle_text.upper())

    return y_bottom


# =============================================================================
# BACK COVER
# =============================================================================
def _draw_globe_icon(c, x, y, size, color=None):
    import math
    if color is None:
        color = GOLD
    c.saveState()
    r = size / 2
    cx, cy = x + r, y + r
    c.setStrokeColor(color)
    c.setLineWidth(0.9)
    c.setFillColor(DEEP_GREEN)
    c.circle(cx, cy, r, fill=0, stroke=1)
    p = c.beginPath()
    for i in range(25):
        angle = (i / 24) * 2 * math.pi
        mx = cx + r * 0.4 * math.cos(angle)
        my = cy + r * math.sin(angle)
        if i == 0:
            p.moveTo(mx, my)
        else:
            p.lineTo(mx, my)
    p.close()
    c.drawPath(p, fill=0, stroke=1)
    c.line(x, cy, x + size, cy)
    c.line(x + r * 0.25, cy + r * 0.5, x + size - r * 0.25, cy + r * 0.5)
    c.line(x + r * 0.25, cy - r * 0.5, x + size - r * 0.25, cy - r * 0.5)
    c.restoreState()


def _draw_envelope_icon(c, x, y, size, color=None):
    if color is None:
        color = GOLD
    c.saveState()
    c.setStrokeColor(color)
    c.setLineWidth(0.9)
    env_h = size * 0.65
    env_y = y + (size - env_h) / 2
    c.rect(x, env_y, size, env_h, fill=0, stroke=1)
    mid_x = x + size / 2
    mid_y = env_y + env_h * 0.3
    p = c.beginPath()
    p.moveTo(x, env_y + env_h)
    p.lineTo(mid_x, mid_y)
    p.lineTo(x + size, env_y + env_h)
    c.drawPath(p, fill=0, stroke=1)
    c.restoreState()


def draw_back_cover(c, logo_white_path=None, year="2026",
                    tagline="We've built. We've bought. We've sold.",
                    website="www.scalepointma.com",
                    email="info@scalepointma.com"):
    """Deep-green back cover with white logo, gold accent, tagline, contact."""
    c.setFillColor(DEEP_GREEN_DK)
    c.rect(0, 0, W, H, fill=1, stroke=0)

    # White logo, upper center
    if logo_white_path and os.path.isfile(logo_white_path):
        try:
            c.drawImage(logo_white_path,
                        W / 2 - 110, H * 0.60, 220, 90,
                        preserveAspectRatio=True, mask='auto')
        except Exception:
            pass

    # Gold accent rule
    line_w = 140
    c.setFillColor(GOLD)
    c.rect(W / 2 - line_w / 2, H * 0.55, line_w, 2, fill=1, stroke=0)

    # Tagline — italic serif, gold
    c.setFont("Times-Italic", 14)
    c.setFillColor(GOLD_LIGHT)
    c.drawCentredString(W / 2, H * 0.48, tagline)

    # Contact block
    contact_y_web = H * 0.36
    contact_y_email = H * 0.36 - 22
    icon_size = 11
    icon_gap = 8

    # Website
    web_tw = c.stringWidth(website, FONT_BODY, 11)
    web_total_w = icon_size + icon_gap + web_tw
    web_start_x = W / 2 - web_total_w / 2
    _draw_globe_icon(c, web_start_x, contact_y_web - 1, icon_size, GOLD)
    c.setFont(FONT_BODY, 11)
    c.setFillColor(WHITE)
    c.drawString(web_start_x + icon_size + icon_gap, contact_y_web, website)

    # Email
    email_tw = c.stringWidth(email, FONT_BODY, 11)
    email_total_w = icon_size + icon_gap + email_tw
    email_start_x = W / 2 - email_total_w / 2
    _draw_envelope_icon(c, email_start_x, contact_y_email - 1, icon_size, GOLD)
    c.setFont(FONT_BODY, 11)
    c.setFillColor(WHITE)
    c.drawString(email_start_x + icon_size + icon_gap,
                 contact_y_email, email)

    # Copyright micro-copy
    c.setFont(FONT_BODY, 8)
    c.setFillColor(HexColor("#8A9995"))
    c.drawCentredString(W / 2, H * 0.15,
                        f"\u00a9 {year} ScalePoint M&A.  Confidential.")
