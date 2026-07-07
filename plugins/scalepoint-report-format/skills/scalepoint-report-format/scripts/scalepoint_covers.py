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

    # (Rule 6: NO stray gold vertical rule at the left edge.)

    # Stacked logo, upper center — LARGE (rule 4). Trim padding so the logo
    # renders at its true size; size from real aspect ratio, not a fixed box.
    if logo_stacked_path and os.path.isfile(logo_stacked_path):
        try:
            trimmed = trim_image(logo_stacked_path)
            logo_w = 250
            logo_h = logo_w * image_ratio(trimmed)
            c.drawImage(trimmed, W / 2 - logo_w / 2, H * 0.70,
                        logo_w, logo_h,
                        preserveAspectRatio=True, mask='auto')
        except Exception:
            pass
    else:
        # Fallback: text-only cover title
        c.setFont(FONT_DISPLAY_BOLD, 28)
        c.setFillColor(GOLD)
        c.drawCentredString(W / 2, H * 0.72, "SCALEPOINT M&A")

    # (Rule 1: NO decorative rule under the logo — the lockup has its own pill.)

    # Title (serif, off-white) — wraps, never overhangs margins (rule 6)
    if title:
        size = 30
        c.setFillColor(WHITE)
        lines = _wrap_text(c, title, W - 2 * MARGIN - 20, FONT_DISPLAY_BOLD, size)
        c.setFont(FONT_DISPLAY_BOLD, size)
        ty = H * 0.50
        for ln in lines:
            c.drawCentredString(W / 2, ty, ln)
            ty -= size + 6

    # Subtitle (italic serif, GOLD — rule 2: never GOLD_LIGHT as text), wrapped
    if subtitle:
        c.setFillColor(GOLD)
        sub_lines = _wrap_text(c, subtitle, W - 2 * MARGIN - 40, FONT_DISPLAY_ITALIC, 14)
        c.setFont(FONT_DISPLAY_ITALIC, 14)
        sy = H * 0.40
        for ln in sub_lines:
            c.drawCentredString(W / 2, sy, ln)
            sy -= 19

    # Date (sans, muted)
    if date:
        c.setFont(FONT_BODY, 10)
        c.setFillColor(HexColor("#C4B890"))
        c.drawCentredString(W / 2, H * 0.08, date.upper())

    # Gold baseline rule
    c.setFillColor(GOLD)
    c.rect(MARGIN, 70, W - 2 * MARGIN, 1.5, fill=1, stroke=0)


# =============================================================================
# HERO & INFO BADGES (rules 11, 21, 24)
# =============================================================================
def hero_badge(c, x, y, w, h, num, label):
    """Cover hero badge: SEPIA face + gold top accent sliver (rule 11);
    deep-green number, standard gold descriptor (rule 22)."""
    c.setFillColor(GOLD)
    c.roundRect(x, y, w, h, CORNER_R, fill=1, stroke=0)
    c.setFillColor(SEPIA)
    c.roundRect(x, y, w, h - 5, CORNER_R, fill=1, stroke=0)
    c.setFont(FONT_DISPLAY_BOLD, 24)
    c.setFillColor(DEEP_GREEN)
    c.drawCentredString(x + w / 2, y + h / 2 - 4, str(num))
    draw_descriptor(c, x + w / 2, y + 15, label)


def info_badge(c, cx, y, w, h, lines=None, name="", role="", phone="",
               email="", website="", accent_color=None, face=None):
    """Contact/info badge (rules 16, 21, 24): WHITE face + top accent.
    Accent = GOLD on dark pages (back cover), DEEP_GREEN on light interior
    pages. Name serif, role gold, then phone / email / website EACH ON THEIR
    OWN LINE — never combined.
    Either pass `lines` = [(text, font, size, color), ...] or the named fields."""
    if face is None:
        face = WHITE
    if accent_color is None:
        accent_color = GOLD
    if lines is None:
        lines = [(name, FONT_DISPLAY_BOLD, 18, DEEP_GREEN)] if name else []
        if role:
            lines.append((role, FONT_BODY, 11, LABEL_GOLD))
        for item in (phone, email, website):
            if item:
                lines.append((item, FONT_BODY, 11, DEEP_GREEN))
    x = cx - w / 2
    c.setFillColor(accent_color)
    c.roundRect(x, y, w, h, CORNER_R, fill=1, stroke=0)
    c.setFillColor(face)
    c.roundRect(x, y, w, h - 5, CORNER_R, fill=1, stroke=0)
    leads = [sz + 7 for (_, _, sz, _) in lines]
    total = sum(leads)
    ty = y + (h - 5) / 2 + total / 2 - leads[0] + 2
    for (txt, fn, sz, col), ld in zip(lines, leads):
        c.setFont(fn, sz)
        c.setFillColor(col)
        c.drawCentredString(cx, ty, txt)
        ty -= ld


# =============================================================================
# TEASER COVER — three-zone spec (rules 10, 12) — NOT the boardroom cover
# =============================================================================
def draw_teaser_cover(c, kicker="", title_lines=None, descriptor="",
                      attributes_line="", metrics=None, footer_line="",
                      logo_stacked_path=None):
    """
    Teaser front cover per the locked Project Eros spec. The heavy boardroom
    cover is the WRONG default for a teaser (rule 6) — use this instead.

    Even vertical rhythm between four groups (rule 12):
      LOGO (large, trimmed) /
      TITLE GROUP (kicker · serif title · muted descriptor — kicker sits
        clearly ABOVE the title; codename goes IN the kicker line, never as
        standalone bright text) /
      HERO UNIT (attributes line ABOVE three sepia hero badges, centered
        as one unit) /
      PAGE FOOTER (pinned to page bottom, excluded from zone centering).
    """
    c.setFillColor(DEEP_GREEN)
    c.rect(0, 0, W, H, fill=1, stroke=0)

    # ---- LOGO (large, trimmed)
    if logo_stacked_path and os.path.isfile(logo_stacked_path):
        trimmed = trim_image(logo_stacked_path)
        lw = 250
        lh = lw * image_ratio(trimmed)
        c.drawImage(trimmed, W / 2 - lw / 2, 578, lw, lh,
                    mask='auto', preserveAspectRatio=True)

    # ---- TITLE GROUP
    if kicker:
        spaced(c, W / 2, 483, kicker.upper(), FONT_BODY_BOLD, 10, GOLD, 2.5, center=True)
    c.setFont(FONT_DISPLAY_BOLD, 32)
    c.setFillColor(WHITE)
    ty = 437
    for ln in (title_lines or []):
        c.drawCentredString(W / 2, ty, ln)
        ty -= 38
    if descriptor:
        c.setFont(FONT_BODY, 11)
        c.setFillColor(HexColor("#C4B890"))
        c.drawCentredString(W / 2, 367, descriptor)

    # ---- HERO UNIT (attributes line on top of the badges)
    if attributes_line:
        spaced(c, W / 2, 262, attributes_line.upper(), FONT_BODY_BOLD, 7.5, GOLD, 0.8, center=True)
    if metrics:
        bw, bh, gap = 152, 78, 18
        x0 = (W - (len(metrics) * bw + (len(metrics) - 1) * gap)) / 2
        for i, (num, label) in enumerate(metrics):
            hero_badge(c, x0 + i * (bw + gap), 160, bw, bh, num, label)

    # ---- PAGE FOOTER (pinned)
    if footer_line:
        spaced(c, W / 2, 55, footer_line.upper(), FONT_BODY_BOLD, 8,
               HexColor("#C4B890"), 1.5, center=True)


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


def draw_back_cover(c, logo_path=None, year="2026",
                    tagline="We've built. We've bought. We've sold.",
                    website="scalepointma.com",
                    email="info@scalepointma.com",
                    contact_name="", contact_role="", contact_phone="",
                    logo_white_path=None):
    """Deep-green back cover: large trimmed logo, 21pt gold italic tagline
    (rule 15), contact in a WHITE info badge with GOLD accent (rules 21/24).

    Rule 5: pass the STACKED logo (its background is exactly DEEP_GREEN and
    blends). logo-white.png has an opaque BLACK background baked in and will
    show as a black box: never place it on a colour field.
    (`logo_white_path` kept as a deprecated alias.)"""
    if logo_path is None:
        logo_path = logo_white_path   # deprecated alias

    c.setFillColor(DEEP_GREEN)
    c.rect(0, 0, W, H, fill=1, stroke=0)

    # Large trimmed logo, upper center (rules 1 & 4: big, and NO rule under it)
    if logo_path and os.path.isfile(logo_path):
        try:
            trimmed = trim_image(logo_path)
            lw = 250
            lh = lw * image_ratio(trimmed)
            c.drawImage(trimmed, W / 2 - lw / 2, H * 0.60, lw, lh,
                        preserveAspectRatio=True, mask='auto')
        except Exception:
            pass

    # Tagline: italic serif, GOLD (rule 2), LARGER (rule 15: ~21pt)
    c.setFont(FONT_DISPLAY_ITALIC, 21)
    c.setFillColor(GOLD)
    c.drawCentredString(W / 2, H * 0.50, tagline)

    # Contact block: white info badge, gold accent, each line its own row
    if contact_name:
        info_badge(c, W / 2, H * 0.24, 380, 132,
                   name=contact_name, role=contact_role,
                   phone=contact_phone, email=email, website=website,
                   accent_color=GOLD, face=WHITE)
    else:
        info_badge(c, W / 2, H * 0.28, 380, 84, lines=[
            (website, FONT_BODY, 11, DEEP_GREEN),
            (email, FONT_BODY, 11, DEEP_GREEN),
        ], accent_color=GOLD, face=WHITE)

    # Copyright micro-copy
    c.setFont(FONT_BODY, 8)
    c.setFillColor(HexColor("#8A9995"))
    c.drawCentredString(W / 2, H * 0.11,
                        f"\u00a9 {year} ScalePoint M&A.  Confidential.")
