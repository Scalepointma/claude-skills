#!/usr/bin/env python3
"""Reference build exercising the v2.1 design rules — regenerate and eyeball
whenever the helpers change. Uses ONLY skill helpers + relative paths.

Covers: teaser cover (three-zone, sepia hero badges), stat rows (gold +
deep-green with standard descriptors), per-row card grid, tables with named
headers + total row, gold callout, subhead hierarchy, numbered rows (green
badge, centered), per-column value cards, persona row, info badge, back cover.
"""
import sys, os

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "scripts"))
from scalepoint_pdf import *
from reportlab.pdfgen import canvas

assets = discover_assets()
X = MARGIN
DOC = "Reference Build"


def page(c, pg, label):
    draw_page_setup(c, DOC, pg, assets.get("icon-fullcolor"), label)


def build(out):
    c = canvas.Canvas(out, pagesize=letter)

    # ---- P1: teaser cover (rules 1, 2, 4, 10, 11, 12)
    draw_teaser_cover(
        c,
        kicker="Confidential Buyer Teaser   ·   Project Sample",
        title_lines=["Western Canada's Premier", "Specialty Retailer"],
        descriptor="Western Canada   ·   Specialty Retail & E-Commerce",
        attributes_line="RETAIL & E-COMMERCE   ·   EXCLUSIVE BRANDS   ·   DEBT-FREE   ·   SHARE SALE",
        metrics=[("$3.19M", "FY2025 Revenue"), ("$255K", "Normalized EBITDA"), ("66%", "Online Growth YoY")],
        footer_line="July 2026   ·   scalepointma.com",
        logo_stacked_path=assets.get("logo-stacked"),
    )
    c.showPage()

    # ---- P2: overview (stat rows: gold row + deep-green row, rule 13/22)
    page(c, 2, "Business Overview")
    y = CONTENT_TOP
    y = draw_title_group(c, X, y, section_title="Business Overview")
    y = draw_body_text(c, X, y, clean_text(
        "A reference page exercising the corrected helpers: single-gold accent "
        "discipline, standard descriptors, gold callouts, and the type hierarchy. "
        "Body copy is 10pt Helvetica in deep green."))
    y -= 24
    y = draw_stat_row(c, X, y, [
        {"number": "$3.19M", "label": "FY2025 Revenue"},
        {"number": "$255K", "label": "Normalized EBITDA"},
        {"number": "66%", "label": "Online Growth YoY"},
    ])
    y -= 26
    y = draw_stat_row(c, X, y, [
        {"number": "19%", "label": "3-Yr Revenue Growth"},
        {"number": "$1.7M", "label": "Inventory (Cost)"},
    ], accent_color=DEEP_GREEN)
    y -= 30
    draw_light_callout(c, X, y - 64, CONTENT_W, 64, clean_text(
        "Gold-on-gold callout: the DEFAULT emphasis element, deep-green text on pale gold."))
    c.showPage()

    # ---- P3: per-row card grid (rules 13, 20)
    page(c, 3, "Investment Highlights")
    y = CONTENT_TOP
    y = draw_title_group(c, X, y, section_title="Investment Highlights",
                         intro_text="One accent colour per row: gold, deep green, olive.")
    cards = [
        {"title": "Category leader", "body": "Largest specialty retailer by volume, with decades of brand equity and a loyal customer base."},
        {"title": "Exclusive brands", "body": "Two leading brands not available through the primary competitor; 1 of 5 national dealerships."},
        {"title": "Organic online growth", "body": "E-commerce growing 66% YoY, entirely organic, with no paid advertising and no SEO investment."},
        {"title": "Peak execution", "body": "About 700 orders in 4 days each year, demonstrating loyalty and inventory execution."},
        {"title": "Operating team", "body": "Tenured staff embedded in operations and e-commerce are committed to remaining post-close."},
        {"title": "Debt-free", "body": "No bank debt; long-standing bank relationship. Supplier terms of Net 30–120."},
    ]
    card_grid_rows(c, X, y, cards, 2)
    c.showPage()

    # ---- P4: tables (rule 23) + subhead (rule 8) + callout
    page(c, 4, "Financial Summary")
    y = CONTENT_TOP
    y = draw_title_group(c, X, y, section_title="Financial Summary (CAD)")
    y = draw_table(c, X, y,
                   [CONTENT_W * 0.34, CONTENT_W * 0.22, CONTENT_W * 0.22, CONTENT_W * 0.22],
                   ["Year Ended Nov 30", "FY2025", "FY2024", "FY2023"],
                   [["Revenue", "$3,190,957", "$2,784,597", "$2,690,468"],
                    ["Gross Profit", "$956,055", "$832,411", "$873,700"],
                    ["Reported EBITDA", "$249,447", "$127,420", "$166,466"]])
    y = draw_subheading(c, X, y, "EBITDA Normalization", gap_above=30)
    y = draw_table(c, X, y, [CONTENT_W * 0.68, CONTENT_W * 0.32],
                   ["Adjustment", "Amount"],
                   [["3-Year Average Reported EBITDA", "$181,111"],
                    ["+ Vehicle expense (owner personal)", "$28,095"],
                    ["+ Owner compensation, net of replacement", "$42,500"]],
                   total_row=["Normalized EBITDA", "$255,206"])
    y -= 12
    y = draw_footnote(c, X, y, "Every table column has a named header (rule 23). Footnotes are plain italic, never boxed.")
    c.showPage()

    # ---- P5: numbered rows (rules 7, 13) + per-column value cards (rule 20)
    page(c, 5, "Growth & Transaction")
    y = CONTENT_TOP
    y = draw_title_group(c, X, y, section_title="Growth Opportunities",
                         intro_text="Numbered rows: gold card accent, deep-green badge, vertically centered.")
    for i, op in enumerate([
        "Paid digital marketing, currently zero spend",
        "Email marketing and customer loyalty program",
        "Lessons, coaching and corporate programming",
    ]):
        draw_numbered_card(c, X, y - 50, CONTENT_W, 50, number=i + 1, title=op)
        y -= 50 + 14
    y = draw_subheading(c, X, y, "Transaction Overview", gap_above=24)
    y -= 6
    tx = [{"title": "Western Canada", "body": "Region"}, {"title": "November 30", "body": "Year End"},
          {"title": "Share Sale", "body": "Structure"}, {"title": "Up to 6 months", "body": "Transition"},
          {"title": "On NDA", "body": "Pricing"}, {"title": "2026", "body": "Target Close"}]
    y = cards_by_column(c, X, y, tx, 3)
    c.showPage()

    # ---- P6: persona row + info badge (rules 16, 21, 24)
    page(c, 6, "Next Steps")
    y = CONTENT_TOP
    y = draw_title_group(c, X, y, section_title="Ideal Buyer Profile")
    y = cards_colored(c, X, y - 6, [
        {"title": "Owner-Operator", "body": "An operator ready to run and grow the business day-to-day."},
        {"title": "Strategic Acquirer", "body": "A strategic buyer seeking a dominant Canadian platform."},
        {"title": "Growth Buyer", "body": "A growth-minded buyer ready to use the untapped digital lever."},
    ])
    y -= 46
    y = draw_subheading(c, X, y, "Next Steps")
    draw_light_callout(c, X, y - 64, CONTENT_W, 64,
                       "Qualified buyers execute an NDA to receive the CIM and full financial package.")
    y -= 64 + 30
    # Interior page -> DEEP_GREEN accent on the white info badge (rule 21)
    info_badge(c, W / 2, y - 132, 380, 132,
               name="Alina Martin", role="CEO & Co-Founder",
               phone="403-701-0020", email="alina.martin@scalepointma.com",
               website="scalepointma.com", accent_color=DEEP_GREEN)
    c.showPage()

    # ---- P7: back cover (rules 1, 2, 5, 15, 24)
    draw_back_cover(c, logo_path=assets.get("logo-stacked"),
                    contact_name="Alina Martin", contact_role="CEO & Co-Founder",
                    contact_phone="403-701-0020",
                    email="alina.martin@scalepointma.com")
    c.showPage()

    c.save()
    print("saved", out)


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "reference_report.pdf")
    build(out)
