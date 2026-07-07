"""ScalePoint M&A Conference Handout Brochure v2 — 2-page letter."""
import os, sys
SKILL_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(SKILL_DIR, "scripts"))

from scalepoint_pdf import *
from scalepoint_base import _wrap_text, _wrap_and_draw, _draw_shadow
from reportlab.pdfgen import canvas

ASSETS = os.path.join(SKILL_DIR, "assets")
LOGO_STACKED = os.path.join(ASSETS, "logo-stacked-on-dark.png")
LOGO_PRIMARY = os.path.join(ASSETS, "logo-primary-horizontal.png")
LOGO_WHITE   = os.path.join(ASSETS, "logo-white.png")
ICON_FULL    = os.path.join(ASSETS, "icon-fullcolor.png")

ALINA = "/sessions/eloquent-dazzling-allen/mnt/07. Marketing/Head Shots/Alina Martin - Head Shot 2.jpg"
SAM   = "/sessions/eloquent-dazzling-allen/mnt/07. Marketing/Head Shots/sam-patel-headshot-1.webp"


def make_portrait_oval(src_path, out_suffix="_oval.png", out_px=700,
                       face_zoom=1.8, top_frac=0.03, left_frac=None):
    """
    Crop a portrait photo to oval, fade edges to white.
    face_zoom: smaller values include MORE body (less face). Default 1.8 tight.
    top_frac: where to start the crop vertically (fraction of source height).
              Use higher values for photos where the subject is lower in frame.
    left_frac: horizontal center fraction; None = auto-center.
    """
    from PIL import Image, ImageDraw, ImageFilter
    img = Image.open(src_path).convert("RGB")
    w, h = img.size
    target_w = int(min(w, h) / face_zoom)
    target_h = int(target_w * 1.25)
    if target_h > h:
        target_h = h
        target_w = int(target_h / 1.25)
    if left_frac is not None:
        left = max(0, int(w * left_frac) - target_w // 2)
    else:
        left = (w - target_w) // 2
    if left + target_w > w:
        left = w - target_w
    top = max(0, int(h * top_frac))
    if top + target_h > h:
        top = h - target_h
    crop = img.crop((left, top, left + target_w, top + target_h))
    new_h = int(out_px * 1.25)
    crop = crop.resize((out_px, new_h), Image.LANCZOS)

    mask = Image.new("L", (out_px, new_h), 0)
    draw = ImageDraw.Draw(mask)
    pad_x = out_px * 0.10
    pad_y = new_h * 0.08
    draw.ellipse((pad_x, pad_y, out_px - pad_x, new_h - pad_y), fill=255)
    mask_feathered = mask.filter(ImageFilter.GaussianBlur(radius=out_px * 0.12))
    white_bg = Image.new("RGB", (out_px, new_h), (255, 255, 255))
    composited = Image.composite(crop, white_bg, mask_feathered)
    alpha = Image.new("L", (out_px, new_h), 0)
    ImageDraw.Draw(alpha).ellipse((0, 0, out_px - 1, new_h - 1), fill=255)
    out = Image.new("RGBA", (out_px, new_h), (255, 255, 255, 0))
    out.paste(composited, (0, 0), alpha)
    out_path = src_path.rsplit(".", 1)[0] + out_suffix
    out.save(out_path, "PNG")
    return out_path


def build_page_1(c):
    # Cream background
    c.setFillColor(CREAM)
    c.rect(0, 0, W, H, fill=1, stroke=0)

    # --- Hero block (top) ---
    hero_top = H
    hero_bot = H - 420
    c.setFillColor(DEEP_GREEN)
    c.rect(0, hero_bot, W, hero_top - hero_bot, fill=1, stroke=0)

    # Gold vertical rule, left gutter, full hero height
    c.setFillColor(GOLD)
    c.rect(MARGIN - 26, hero_bot, 6, hero_top - hero_bot, fill=1, stroke=0)

    # Stacked logo centered near top of hero (150% bigger than v1)
    try:
        logo_w, logo_h = 300, 213
        c.drawImage(LOGO_STACKED, W / 2 - logo_w / 2,
                    hero_top - logo_h - 24,
                    logo_w, logo_h, preserveAspectRatio=True, mask='auto')
    except Exception:
        pass

    # Gold kicker, letter-spaced, centered
    kicker = "OPERATOR-LED M&A ADVISORY"
    c.setFont(FONT_BODY_BOLD, 10)
    c.setFillColor(GOLD)
    total_w = sum(c.stringWidth(ch, FONT_BODY_BOLD, 10) + 2.2 for ch in kicker) - 2.2
    cx = W / 2 - total_w / 2
    for ch in kicker:
        c.drawString(cx, hero_top - 266, ch)
        cx += c.stringWidth(ch, FONT_BODY_BOLD, 10) + 2.2

    # Huge serif headline, centered, two lines
    c.setFont(FONT_DISPLAY_BOLD, 34)
    c.setFillColor(WHITE)
    c.drawCentredString(W / 2, hero_top - 302, "We help founders")
    c.drawCentredString(W / 2, hero_top - 342, "exit on their terms.")

    # Short gold hairline under headline
    c.setFillColor(GOLD)
    c.rect(W / 2 - 40, hero_top - 372, 80, 1.5, fill=1, stroke=0)

    # --- Middle statement band ---
    y = hero_bot - 40
    c.setFont("Times-Italic", 14)
    c.setFillColor(DEEP_GREEN)
    c.drawCentredString(W / 2, y,
                        "For owner-operated businesses doing $1M to $25M in revenue.")

    y -= 26
    # Manual line breaks to avoid orphans — deliberate 3-beat then punchline rhythm
    c.setFont(FONT_BODY, 10.5)
    c.setFillColor(BODY_COLOR)
    c.drawCentredString(W / 2, y,
        "We've built companies. We've bought companies. We've sold companies.")
    y -= 16
    c.drawCentredString(W / 2, y, "Now we help others do the same.")
    y -= 22

    # Short gold hairline
    c.setFillColor(GOLD)
    c.rect(W / 2 - 40, y, 80, 1.2, fill=1, stroke=0)
    y -= 32

    # --- Three pillars ---
    pillars = [
        {"num": "01", "title": "BUILD",
         "body": ("Strengthen the business you've built. We specialize in AI "
                  "implementations that lift enterprise value ahead of an exit.")},
        {"num": "02", "title": "BUY",
         "body": ("Strategic acquisitions that strengthen your position \u2014 "
                  "not ones that delay your exit by five years.")},
        {"num": "03", "title": "SELL",
         "body": ("Sell-side advisory and brokerage for founders who want "
                  "to work with advisors who have been there before.")},
    ]

    num_x = MARGIN + 10
    title_x = MARGIN + 96
    body_x = MARGIN + 210
    body_max_w = W - MARGIN - body_x

    for i, p in enumerate(pillars):
        c.setFont(FONT_DISPLAY_BOLD, 44)
        c.setFillColor(GOLD)
        c.drawString(num_x, y - 34, p["num"])

        c.setFont(FONT_DISPLAY_BOLD, 22)
        c.setFillColor(DEEP_GREEN)
        c.drawString(title_x, y - 26, p["title"])

        c.setFont(FONT_BODY, 10)
        c.setFillColor(BODY_COLOR)
        by = y - 20
        for line in _wrap_text(c, p["body"], body_max_w, FONT_BODY, 10):
            c.drawString(body_x, by, line)
            by -= 13.5

        # Light gold hairline between pillars
        if i < len(pillars) - 1:
            c.setFillColor(HexColor("#E6D9B0"))
            c.rect(MARGIN + 10, y - 62, CONTENT_W - 20, 0.5, fill=1, stroke=0)

        y -= 64

    # Footer
    draw_footer(c, doc_title="", page_num=1, icon_path=ICON_FULL,
                section_label="SCALEPOINT M&A")


def build_page_2(c):
    c.setFillColor(CREAM)
    c.rect(0, 0, W, H, fill=1, stroke=0)

    # Gold vertical rule on RIGHT edge (mirror of p1)
    c.setFillColor(GOLD)
    c.rect(W - MARGIN + 20, 60, 6, H - 120, fill=1, stroke=0)

    y = H - 70

    # Kicker
    kicker = "WHY SCALEPOINT"
    c.setFont(FONT_BODY_BOLD, 10)
    c.setFillColor(GOLD)
    char_x = MARGIN
    for ch in kicker:
        c.drawString(char_x, y, ch)
        char_x += c.stringWidth(ch, FONT_BODY_BOLD, 10) + 2.0

    y -= 28
    c.setFont(FONT_DISPLAY_BOLD, 28)
    c.setFillColor(DEEP_GREEN)
    c.drawString(MARGIN, y, "Advisors who've been operators.")
    y -= 38

    c.setFont(FONT_BODY, 10.5)
    c.setFillColor(BODY_COLOR)
    para = ("Every senior advisor at ScalePoint has built a business. We've "
            "made payroll. We've negotiated deals. We've sat across from "
            "buyers and sellers. When you work with us, you're working with "
            "people who've done this \u2014 not people who've studied it.")
    for line in _wrap_text(c, para, CONTENT_W - 30, FONT_BODY, 10.5):
        c.drawString(MARGIN, y, line)
        y -= 15
    y -= 22

    # Stat row
    stats = [("150+", "Companies advised"),
             ("40+", "Years operating"),
             ("$1-25M", "Revenue band")]
    stat_col_w = (CONTENT_W - 24) / 3

    c.setFillColor(GOLD)
    c.rect(MARGIN, y + 8, CONTENT_W, 1, fill=1, stroke=0)
    y -= 4
    for i, (num, label) in enumerate(stats):
        sx = MARGIN + i * (stat_col_w + 12)
        c.setFont(FONT_DISPLAY_BOLD, 30)
        c.setFillColor(DEEP_GREEN)
        c.drawString(sx, y - 30, num)
        c.setFont(FONT_BODY, 9.5)
        c.setFillColor(SECONDARY_COLOR)
        c.drawString(sx, y - 46, label)
    c.setFillColor(GOLD)
    c.rect(MARGIN, y - 58, CONTENT_W, 1, fill=1, stroke=0)
    y -= 90

    # Team section
    c.setFont(FONT_BODY_BOLD, 10)
    c.setFillColor(GOLD)
    kicker2 = "MEET THE ADVISORS"
    char_x = MARGIN
    for ch in kicker2:
        c.drawString(char_x, y, ch)
        char_x += c.stringWidth(ch, FONT_BODY_BOLD, 10) + 2.0
    y -= 26
    c.setFont(FONT_DISPLAY_BOLD, 22)
    c.setFillColor(DEEP_GREEN)
    c.drawString(MARGIN, y, "Two operators. One conversation.")
    y -= 14

    alina_path = make_portrait_oval(ALINA, face_zoom=1.25, top_frac=0.22)
    sam_path = make_portrait_oval(SAM, face_zoom=1.8, top_frac=0.03)

    col_w = (CONTENT_W - 30) / 2
    photo_w = 140
    photo_h = 175
    photo_top = y - 6
    photo_bot = photo_top - photo_h

    team = [
        {"photo": alina_path, "name": "Alina Martin",
         "title": "Co-Founder \u00b7 M&A Advisor",
         "bio": ("Serial founder and operator. Leads growth and exit "
                 "conversations across services, software, and hospitality.")},
        {"photo": sam_path, "name": "Sam Patel",
         "title": "Partner \u00b7 M&A Advisory",
         "bio": ("Investor and operator with deep experience in "
                 "owner-operated acquisition and integration.")},
    ]

    for i, person in enumerate(team):
        cx = MARGIN + i * (col_w + 30)
        px = cx + (col_w - photo_w) / 2
        try:
            c.drawImage(person["photo"], px, photo_bot, photo_w, photo_h,
                        preserveAspectRatio=True, mask='auto')
        except Exception:
            c.setFillColor(NEAR_WHITE)
            c.rect(px, photo_bot, photo_w, photo_h, fill=1, stroke=0)

        c.setFont(FONT_DISPLAY_BOLD, 15)
        c.setFillColor(DEEP_GREEN)
        c.drawCentredString(cx + col_w / 2, photo_bot - 20, person["name"])

        c.setFont("Times-Italic", 10)
        c.setFillColor(GOLD)
        c.drawCentredString(cx + col_w / 2, photo_bot - 36, person["title"])

        c.setFont(FONT_BODY, 9)
        c.setFillColor(SECONDARY_COLOR)
        bio_lines = _wrap_text(c, person["bio"], col_w - 20, FONT_BODY, 9)
        by = photo_bot - 54
        for line in bio_lines[:3]:
            c.drawCentredString(cx + col_w / 2, by, line)
            by -= 12

    y = photo_bot - 110

    # Contact block
    c.setFillColor(GOLD)
    c.rect(MARGIN, y + 20, CONTENT_W, 1, fill=1, stroke=0)
    y -= 8

    c.setFont("Times-Italic", 11)
    c.setFillColor(SECONDARY_COLOR)
    c.drawString(MARGIN, y, "Thoughtful about what comes next?")
    c.setFont(FONT_DISPLAY_BOLD, 22)
    c.setFillColor(DEEP_GREEN)
    c.drawString(MARGIN, y - 26, "Let's talk.")

    right_x = W - MARGIN
    c.setFont(FONT_BODY_BOLD, 9)
    c.setFillColor(GOLD)
    c.drawRightString(right_x, y, "CONTACT")

    c.setFont(FONT_DISPLAY, 13)
    c.setFillColor(DEEP_GREEN)
    c.drawRightString(right_x, y - 18, "www.scalepointma.com")
    c.drawRightString(right_x, y - 36, "info@scalepointma.com")

    draw_footer(c, doc_title="", page_num=2, icon_path=ICON_FULL,
                section_label="SCALEPOINT M&A")


if __name__ == "__main__":
    OUT = "/sessions/eloquent-dazzling-allen/mnt/outputs/ScalePoint_Brochure_v2.pdf"
    c = canvas.Canvas(OUT, pagesize=letter)
    build_page_1(c)
    c.showPage()
    build_page_2(c)
    c.save()
    print(f"Wrote: {OUT}")
