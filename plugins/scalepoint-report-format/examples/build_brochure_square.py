"""ScalePoint M&A — Square brochure (7.5" x 7.5") with rounded-corner card.
Matches the business-card format/feel — distinctive, hand-friendly at a
conference. 2-page double-sided (front + back)."""
import os, sys
SKILL_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(SKILL_DIR, "scripts"))
from scalepoint_pdf import *
from scalepoint_base import _wrap_text, _wrap_and_draw, _draw_shadow
from reportlab.pdfgen import canvas
from reportlab.lib.colors import Color

ASSETS = os.path.join(SKILL_DIR, "assets")
LOGO_STACKED = os.path.join(ASSETS, "logo-stacked-on-dark-trimmed.png")
ICON_FULL    = os.path.join(ASSETS, "icon-fullcolor.png")
ALINA = "/sessions/eloquent-dazzling-allen/mnt/07. Marketing/Head Shots/Alina Martin - Head Shot 2.jpg"
SAM   = "/sessions/eloquent-dazzling-allen/mnt/07. Marketing/Head Shots/sam-patel-headshot-1.webp"
HERO_PHOTO = "/sessions/eloquent-dazzling-allen/mnt/Website Images/iStock-2184269063.jpg"

# Square page size: 7.5" x 7.5" = 540 x 540 pt
SQ = 540
INSET = 8          # how far the card is inset from the page edge (shows shadow outside)
CARD_R = 22        # rounded corner radius of the card
CARD_MARGIN = 36   # inner content margin from card edge
CARD_LEFT = INSET + CARD_MARGIN
CARD_RIGHT = SQ - INSET - CARD_MARGIN
CARD_W = CARD_RIGHT - CARD_LEFT  # ≈ 448


def make_duotone(src_path, suffix="_duo_sq.jpg", dark="#0A2D2A", light="#E8E4D7"):
    from PIL import Image, ImageOps
    img = Image.open(src_path).convert("L")
    out = ImageOps.colorize(img, black=dark, white=light)
    op = src_path.rsplit(".", 1)[0] + suffix
    out.save(op, quality=90)
    return op


def make_portrait_oval(src, suffix="_ovalS.png", out_px=500, face_zoom=1.25,
                       top_frac=0.22):
    from PIL import Image, ImageDraw, ImageFilter
    img = Image.open(src).convert("RGB")
    w, h = img.size
    target_w = int(min(w, h) / face_zoom)
    target_h = int(target_w * 1.25)
    if target_h > h:
        target_h = h
        target_w = int(target_h / 1.25)
    left = (w - target_w) // 2
    top = max(0, int(h * top_frac))
    if top + target_h > h:
        top = h - target_h
    crop = img.crop((left, top, left + target_w, top + target_h))
    new_h = int(out_px * 1.25)
    crop = crop.resize((out_px, new_h), Image.LANCZOS)
    mask = Image.new("L", (out_px, new_h), 0)
    ImageDraw.Draw(mask).ellipse((out_px*0.10, new_h*0.08,
                                  out_px*0.90, new_h*0.92), fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(radius=out_px*0.10))
    white = Image.new("RGB", (out_px, new_h), (255, 255, 255))
    comp = Image.composite(crop, white, mask)
    alpha = Image.new("L", (out_px, new_h), 0)
    ImageDraw.Draw(alpha).ellipse((0, 0, out_px-1, new_h-1), fill=255)
    out_img = Image.new("RGBA", (out_px, new_h), (255, 255, 255, 0))
    out_img.paste(comp, (0, 0), alpha)
    op = src.rsplit(".", 1)[0] + suffix
    out_img.save(op, "PNG")
    return op


def draw_card_frame(c):
    """Rounded-corner cream card on a neutral page bg, with subtle shadow."""
    # Page bg: slightly darker than cream so the card shows
    c.setFillColor(HexColor("#EFEBDC"))
    c.rect(0, 0, SQ, SQ, fill=1, stroke=0)
    # Subtle shadow
    _draw_shadow(c, INSET, INSET, SQ - 2*INSET, SQ - 2*INSET,
                 radius=CARD_R, offset=2, opacity=0.08)
    # Card itself
    c.setFillColor(CREAM)
    c.roundRect(INSET, INSET, SQ - 2*INSET, SQ - 2*INSET, CARD_R,
                fill=1, stroke=0)
    # Gold hairline around the card (1pt)
    c.setStrokeColor(HexColor("#E6D9B0"))
    c.setLineWidth(0.7)
    c.roundRect(INSET, INSET, SQ - 2*INSET, SQ - 2*INSET, CARD_R,
                fill=0, stroke=1)


def draw_footer_square(c, page_num=1):
    """Tiny footer at bottom of card: icon left, mini green bar, gold page chip."""
    fy = INSET + 14
    icon_size = 18
    icon_x = CARD_LEFT - 4
    try:
        c.drawImage(ICON_FULL, icon_x, fy - 3, icon_size, icon_size,
                    preserveAspectRatio=True, mask='auto')
    except Exception:
        pass
    bar_left = icon_x + icon_size + 8
    gold_w = 58
    bar_right = CARD_RIGHT
    c.setFillColor(DEEP_GREEN)
    c.rect(bar_left, fy + 1, bar_right - bar_left - gold_w, 16,
           fill=1, stroke=0)
    c.setFillColor(GOLD)
    c.rect(bar_right - gold_w, fy + 1, gold_w, 16, fill=1, stroke=0)
    c.setFont(FONT_DISPLAY, 7.5)
    c.setFillColor(WHITE)
    c.drawString(bar_left + 10, fy + 5, "SCALEPOINT M&A")
    c.setFont(FONT_DISPLAY, 8.5)
    c.setFillColor(DEEP_GREEN)
    c.drawRightString(bar_right - 8, fy + 5, f"{page_num:02d}")


def build_page_1(c):
    draw_card_frame(c)

    # --- Hero: clean deep green within the rounded card, rounded top corners ---
    hero_top = SQ - INSET - 4
    hero_bot = hero_top - 230
    c.saveState()
    clip = c.beginPath()
    clip.roundRect(INSET + 2, hero_bot, SQ - 2*(INSET+2), hero_top - hero_bot,
                   CARD_R - 2)
    c.clipPath(clip, stroke=0)
    c.setFillColor(DEEP_GREEN)
    c.rect(INSET, hero_bot, SQ - 2*INSET, hero_top - hero_bot, fill=1, stroke=0)
    c.restoreState()

    # Gold vertical rule on left of hero
    c.setFillColor(GOLD)
    c.rect(CARD_LEFT - 16, hero_bot + 8, 4, hero_top - hero_bot - 16,
           fill=1, stroke=0)

    # Logo centered in hero (big)
    logo_w, logo_h = 220, 156
    try:
        c.drawImage(LOGO_STACKED, SQ/2 - logo_w/2, hero_top - logo_h - 10,
                    logo_w, logo_h, preserveAspectRatio=True, mask='auto')
    except Exception:
        pass

    # Kicker
    kicker = "OPERATOR-LED M&A ADVISORY"
    c.setFont(FONT_BODY_BOLD, 8)
    c.setFillColor(GOLD)
    total_w = sum(c.stringWidth(ch, FONT_BODY_BOLD, 8) + 1.8 for ch in kicker) - 1.8
    cx = SQ/2 - total_w/2
    for ch in kicker:
        c.drawString(cx, hero_top - 178, ch)
        cx += c.stringWidth(ch, FONT_BODY_BOLD, 8) + 1.8

    # Huge serif headline
    c.setFont(FONT_DISPLAY_BOLD, 24)
    c.setFillColor(WHITE)
    c.drawCentredString(SQ/2, hero_top - 202, "We help founders exit")
    c.drawCentredString(SQ/2, hero_top - 224, "on their terms.")

    # --- Middle positioning + body ---
    y = hero_bot - 26
    c.setFont("Times-Italic", 11)
    c.setFillColor(DEEP_GREEN)
    c.drawCentredString(SQ/2, y,
                        "For owner-operated businesses $1M \u2013 $25M in revenue.")
    y -= 18
    c.setFont(FONT_BODY, 9.5)
    c.setFillColor(BODY_COLOR)
    c.drawCentredString(SQ/2, y,
        "We've built companies. We've bought companies. We've sold companies.")
    y -= 14
    c.drawCentredString(SQ/2, y, "Now we help others do the same.")
    y -= 18

    # Gold hairline
    c.setFillColor(GOLD)
    c.rect(SQ/2 - 28, y, 56, 1, fill=1, stroke=0)
    y -= 22

    # --- Three pillars (compact) ---
    pillars = [
        ("01", "BUILD", "AI implementations that lift enterprise value ahead of exit."),
        ("02", "BUY", "Strategic acquisitions that strengthen your position."),
        ("03", "SELL", "Sell-side advisory for founders who want advisors who've been there."),
    ]
    num_x = CARD_LEFT + 4
    title_x = CARD_LEFT + 54
    body_x = CARD_LEFT + 128
    body_w = CARD_RIGHT - body_x
    for i, (num, title, body) in enumerate(pillars):
        c.setFont(FONT_DISPLAY_BOLD, 28)
        c.setFillColor(GOLD)
        c.drawString(num_x, y - 22, num)
        c.setFont(FONT_DISPLAY_BOLD, 15)
        c.setFillColor(DEEP_GREEN)
        c.drawString(title_x, y - 18, title)
        c.setFont(FONT_BODY, 8.8)
        c.setFillColor(BODY_COLOR)
        by = y - 14
        for line in _wrap_text(c, body, body_w, FONT_BODY, 8.8):
            c.drawString(body_x, by, line)
            by -= 11
        if i < len(pillars) - 1:
            c.setFillColor(HexColor("#E6D9B0"))
            c.rect(CARD_LEFT + 4, y - 36, CARD_W - 8, 0.4, fill=1, stroke=0)
        y -= 38

    draw_footer_square(c, page_num=1)


def build_page_2(c):
    draw_card_frame(c)

    # Gold vertical rule on RIGHT (mirror p1)
    c.setFillColor(GOLD)
    c.rect(CARD_RIGHT + 6, INSET + 48, 4, SQ - 2*INSET - 96, fill=1, stroke=0)

    # --- Why ScalePoint ---
    y = SQ - INSET - 40

    kicker = "WHY SCALEPOINT"
    c.setFont(FONT_BODY_BOLD, 8)
    c.setFillColor(GOLD)
    char_x = CARD_LEFT
    for ch in kicker:
        c.drawString(char_x, y, ch)
        char_x += c.stringWidth(ch, FONT_BODY_BOLD, 8) + 1.6

    y -= 22
    c.setFont(FONT_DISPLAY_BOLD, 22)
    c.setFillColor(DEEP_GREEN)
    c.drawString(CARD_LEFT, y, "Advisors who've been operators.")
    y -= 26

    c.setFont(FONT_BODY, 9.5)
    c.setFillColor(BODY_COLOR)
    para = ("Every senior advisor at ScalePoint has built a business. "
            "We've made payroll. We've negotiated deals. When you work with us, "
            "you're working with people who've done this \u2014 not studied it.")
    for line in _wrap_text(c, para, CARD_W, FONT_BODY, 9.5):
        c.drawString(CARD_LEFT, y, line)
        y -= 13
    y -= 12

    # Stats
    stats = [("150+", "Companies advised"),
             ("40+", "Years operating"),
             ("$1-25M", "Revenue band")]
    col_w = CARD_W / 3
    c.setFillColor(GOLD)
    c.rect(CARD_LEFT, y + 6, CARD_W, 0.6, fill=1, stroke=0)
    y -= 4
    for i, (num, label) in enumerate(stats):
        sx = CARD_LEFT + i * col_w
        c.setFont(FONT_DISPLAY_BOLD, 22)
        c.setFillColor(DEEP_GREEN)
        c.drawString(sx, y - 22, num)
        c.setFont(FONT_BODY, 8.5)
        c.setFillColor(SECONDARY_COLOR)
        c.drawString(sx, y - 34, label)
    c.setFillColor(GOLD)
    c.rect(CARD_LEFT, y - 44, CARD_W, 0.6, fill=1, stroke=0)
    y -= 64

    # --- Team ---
    c.setFont(FONT_BODY_BOLD, 8)
    c.setFillColor(GOLD)
    kicker2 = "MEET THE ADVISORS"
    char_x = CARD_LEFT
    for ch in kicker2:
        c.drawString(char_x, y, ch)
        char_x += c.stringWidth(ch, FONT_BODY_BOLD, 8) + 1.6
    y -= 22
    c.setFont(FONT_DISPLAY_BOLD, 18)
    c.setFillColor(DEEP_GREEN)
    c.drawString(CARD_LEFT, y, "Two operators. One conversation.")
    y -= 14

    alina_p = make_portrait_oval(ALINA, face_zoom=1.25, top_frac=0.22)
    sam_p = make_portrait_oval(SAM, face_zoom=1.22, top_frac=0.07)
    col_w = (CARD_W - 20) / 2
    photo_w, photo_h = 100, 125
    photo_top = y - 6
    photo_bot = photo_top - photo_h

    team = [
        (alina_p, "Alina Martin", "CEO"),
        (sam_p, "Sam Patel", "Senior Associate"),
    ]
    for i, (photo, name, title) in enumerate(team):
        cx = CARD_LEFT + i * (col_w + 20)
        px = cx + (col_w - photo_w) / 2
        try:
            c.drawImage(photo, px, photo_bot, photo_w, photo_h,
                        preserveAspectRatio=True, mask='auto')
        except Exception:
            c.setFillColor(NEAR_WHITE)
            c.rect(px, photo_bot, photo_w, photo_h, fill=1, stroke=0)
        c.setFont(FONT_DISPLAY_BOLD, 12)
        c.setFillColor(DEEP_GREEN)
        c.drawCentredString(cx + col_w/2, photo_bot - 16, name)
        c.setFont("Times-Italic", 9)
        c.setFillColor(GOLD)
        c.drawCentredString(cx + col_w/2, photo_bot - 30, title)

    # --- Contact strip (consolidated, at bottom) ---
    strip_h = 96
    strip_y = INSET + 40
    c.setFillColor(DEEP_GREEN)
    c.roundRect(CARD_LEFT - 8, strip_y, CARD_W + 16, strip_h, 14,
                fill=1, stroke=0)
    c.setStrokeColor(GOLD)
    c.setLineWidth(0.9)
    c.roundRect(CARD_LEFT - 4, strip_y + 4, CARD_W + 8, strip_h - 8, 12,
                fill=0, stroke=1)

    c.setFont(FONT_DISPLAY_BOLD, 16)
    c.setFillColor(GOLD)
    c.drawCentredString(SQ/2, strip_y + strip_h - 22, "Let\u2019s talk.")

    col_w_strip = (CARD_W - 16) / 3
    col_top = strip_y + strip_h - 42
    contacts = [
        ("ALINA MARTIN", "CEO",
         "403.701.0020", "alina.martin@scalepointma.com"),
        ("SAM PATEL", "Senior Associate",
         "587.582.6032", "sam.patel@scalepointma.com"),
        ("GENERAL", "Toll-free",
         "888.278.4991", "info@scalepointma.com"),
    ]
    for i, (name, role, phone, email) in enumerate(contacts):
        cx = CARD_LEFT - 4 + i * col_w_strip
        c.setFont(FONT_BODY_BOLD, 7.5)
        c.setFillColor(GOLD)
        char_x = cx + 6
        for ch in name:
            c.drawString(char_x, col_top, ch)
            char_x += c.stringWidth(ch, FONT_BODY_BOLD, 7.5) + 1.2
        c.setFont("Times-Italic", 7.5)
        c.setFillColor(HexColor("#E6D9B0"))
        c.drawString(cx + 6, col_top - 11, role)
        c.setFont(FONT_BODY, 8.5)
        c.setFillColor(WHITE)
        c.drawString(cx + 6, col_top - 25, phone)
        c.setFont(FONT_BODY, 7.2)
        c.setFillColor(HexColor("#E6D9B0"))
        c.drawString(cx + 6, col_top - 37, email)

    # Vertical separators
    c.setStrokeColor(GOLD)
    c.setLineWidth(0.4)
    for i in [1, 2]:
        sep_x = CARD_LEFT - 4 + i * col_w_strip
        c.line(sep_x, strip_y + 8, sep_x, strip_y + strip_h - 46)

    draw_footer_square(c, page_num=2)


if __name__ == "__main__":
    OUT = "/sessions/eloquent-dazzling-allen/mnt/outputs/ScalePoint_Brochure_Square.pdf"
    c = canvas.Canvas(OUT, pagesize=(SQ, SQ))
    build_page_1(c)
    c.showPage()
    c.setPageSize((SQ, SQ))
    build_page_2(c)
    c.save()
    print(f"Wrote: {OUT} (7.5\" x 7.5\")")
