#!/usr/bin/env python3
"""ScalePoint M&A one-page teaser layout engine.

Standalone (only needs reportlab). Encodes the format locked on Project Eros
(July 2026): white editorial page, deep-green header band + footer strip,
gold hairline sections, single-line proof bullets, hairline-divided metric
strip, revenue/EBITDA bar charts with growth callouts, numbered growth list,
transaction key-value column, footnotes.

Usage:
    from teaser_layout import build_teaser
    build_teaser(DATA, "out.pdf")   # DATA: see EXAMPLE_DATA at bottom

Hard format rules encoded here (do not override from SKILL.md):
- ONE page. build_teaser raises if content overflows the page budget.
- Charts, not tables, for financials.
- No em dashes anywhere (en dash only in numeric ranges).
- Every derived figure needs a footnote line passed in data["footnotes"].
"""
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import HexColor, white

# ---- brand constants (ScalePoint M&A) ----
DEEP_GREEN = HexColor("#0A2D2A")
GOLD       = HexColor("#CB9D43")
OLIVE      = HexColor("#869846")
LABEL_GOLD = HexColor("#A9803A")   # standard descriptor gold
MUTED      = HexColor("#C4B890")   # muted text on dark bands
GREY       = HexColor("#44544F")
HAIR       = HexColor("#D9D4C8")   # hairline rules
WHITE      = white

FONT_DISPLAY      = "Times-Roman"      # serif display (Libre Baskerville stand-in)
FONT_DISPLAY_BOLD = "Times-Bold"
FONT_BODY         = "Helvetica"
FONT_BODY_BOLD    = "Helvetica-Bold"

W, H = letter
MARGIN = 50
CONTENT_W = W - 2 * MARGIN
X = MARGIN

_ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")
LOGO_ON_DARK = os.path.join(_ASSETS, "logo-horizontal-on-dark.png")
LOGO_RATIO = 0.141  # trimmed height/width


# ---- primitives ----
def spaced(c, x, y, text, font, size, color, tr=2.0, center=False, right=False):
    """Letter-spaced caps text (kickers, descriptors)."""
    c.setFont(font, size); c.setFillColor(color)
    total = sum(c.stringWidth(ch, font, size) + tr for ch in text) - tr
    sx = x - total / 2 if center else (x - total if right else x)
    for ch in text:
        c.drawString(sx, y, ch)
        sx += c.stringWidth(ch, font, size) + tr


def wrap(c, x, y, text, font, size, color, maxw, lh):
    """Word-wrapped paragraph; returns y after the last line."""
    c.setFont(font, size); c.setFillColor(color)
    line = ""
    for wd in text.split():
        t = (line + " " + wd).strip()
        if c.stringWidth(t, font, size) > maxw:
            c.drawString(x, y, line); y -= lh; line = wd
            c.setFont(font, size); c.setFillColor(color)
        else:
            line = t
    if line:
        c.drawString(x, y, line); y -= lh
    return y


def rule(c, x, y, w, color=GOLD, lw=1.2):
    c.setStrokeColor(color); c.setLineWidth(lw); c.line(x, y, x + w, y)


def sect(c, x, y, text, size=13):
    """Serif section title with short gold underline."""
    c.setFont(FONT_DISPLAY_BOLD, size); c.setFillColor(DEEP_GREEN)
    c.drawString(x, y, text)
    rule(c, x, y - 5, 26)


# ---- composite blocks ----
def header_band(c, title, descriptor, band_bottom=676):
    """Deep-green bookend: logo left, kicker right, serif title, muted descriptor."""
    c.setFillColor(DEEP_GREEN); c.rect(0, band_bottom, W, H - band_bottom, fill=1, stroke=0)
    lw_ = 170; lh_ = lw_ * LOGO_RATIO
    if os.path.isfile(LOGO_ON_DARK):
        c.drawImage(LOGO_ON_DARK, X, H - 32 - lh_, lw_, lh_, mask='auto', preserveAspectRatio=True)
    spaced(c, X + CONTENT_W, H - 30 - lh_ / 2, "CONFIDENTIAL BUYER TEASER",
           FONT_BODY_BOLD, 8, GOLD, 1.8, right=True)
    c.setFont(FONT_DISPLAY_BOLD, 21); c.setFillColor(WHITE)
    c.drawString(X, band_bottom + 30, title)
    c.setFont(FONT_BODY, 9); c.setFillColor(MUTED)
    c.drawString(X, band_bottom + 12, descriptor)


def bullet_rows(c, y, items):
    """Single-line gold-dot proof bullets. Each item MUST fit one line."""
    for b in items:
        if c.stringWidth(b, FONT_BODY, 9) > CONTENT_W - 10:
            raise ValueError(f"Bullet too long for one line (shorten it): {b[:60]}...")
        c.setFillColor(GOLD); c.circle(X + 2.4, y + 2.8, 2.3, fill=1, stroke=0)
        c.setFont(FONT_BODY, 9); c.setFillColor(DEEP_GREEN)
        c.drawString(X + 10, y, b)
        y -= 12.5
    return y


def metric_strip(c, y, metrics):
    """3 hero metrics with hairline dividers. metrics: [(value, LABEL), ...]"""
    n = len(metrics)
    my = y - 20
    cols = [X + CONTENT_W * ((2 * i + 1) / (2 * n)) for i in range(n)]
    for (val, lab), mx in zip(metrics, cols):
        c.setFont(FONT_DISPLAY_BOLD, 20); c.setFillColor(DEEP_GREEN)
        c.drawCentredString(mx, my, val)
        spaced(c, mx, my - 13, lab.upper(), FONT_BODY_BOLD, 6.2, LABEL_GOLD, 0.9, center=True)
    c.setStrokeColor(HAIR); c.setLineWidth(1)
    for i in range(1, n):
        c.line(X + CONTENT_W * i / n, my - 11, X + CONTENT_W * i / n, my + 14)
    return my - 13 - 16


def _fmt_money(v):
    """Auto-scale a CAD figure: $8.43M / $2.69M / $216K."""
    if v >= 10e6:
        return f"${v/1e6:.1f}M"
    if v >= 1e6:
        return f"${v/1e6:.2f}M"
    return f"${v/1e3:.0f}K"


def dual_bar_charts(c, x, y_top, w, h, left_title, left_series, right_title, right_series,
                    left_fmt=_fmt_money, right_fmt=_fmt_money,
                    growth_on_left=True):
    """Two side-by-side bar charts (e.g. Revenue | Normalized EBITDA).
    series: [(label, value), ...]. Growth % callouts drawn between left bars."""
    base = y_top - h + 16; top = y_top - 20
    lw = w * 0.56; rw = w * 0.36; gap_mid = w - lw - rw
    spaced(c, x + lw / 2, y_top - 8, left_title.upper(), FONT_BODY_BOLD, 6.5, LABEL_GOLD, 1.0, center=True)
    spaced(c, x + lw + gap_mid + rw / 2, y_top - 8, right_title.upper(), FONT_BODY_BOLD, 6.5, LABEL_GOLD, 1.0, center=True)
    c.setStrokeColor(HAIR); c.setLineWidth(0.8)
    c.line(x, base, x + lw, base); c.line(x + lw + gap_mid, base, x + w, base)

    n = len(left_series); bw = 46; slot = lw / n
    scale = (top - base - 18) / max(v for _, v in left_series)
    tops = []
    for i, (lab, v) in enumerate(left_series):
        bx = x + slot * i + (slot - bw) / 2; bh = v * scale
        c.setFillColor(GOLD if i == n - 1 else DEEP_GREEN)
        c.rect(bx, base, bw, bh, fill=1, stroke=0)
        tops.append((bx + bw / 2, base + bh))
        c.setFont(FONT_DISPLAY_BOLD, 9); c.setFillColor(DEEP_GREEN)
        c.drawCentredString(bx + bw / 2, base + bh + 5, left_fmt(v))
        c.setFont(FONT_BODY_BOLD, 6.5); c.setFillColor(GREY)
        c.drawCentredString(bx + bw / 2, base - 10, lab)
    if growth_on_left:
        for i in range(1, n):
            g = (left_series[i][1] / left_series[i - 1][1] - 1) * 100
            mx = (tops[i - 1][0] + tops[i][0]) / 2
            my = max(tops[i - 1][1], tops[i][1]) + 16
            c.setFont(FONT_BODY_BOLD, 6.8); c.setFillColor(OLIVE)
            c.drawCentredString(mx, my, f"+{g:.1f}%")

    rx0 = x + lw + gap_mid; n2 = len(right_series); slot2 = rw / n2; bw2 = 32
    scale2 = (top - base - 18) / max(v for _, v in right_series)
    for i, (lab, v) in enumerate(right_series):
        bx = rx0 + slot2 * i + (slot2 - bw2) / 2; bh = v * scale2
        c.setFillColor(OLIVE)
        c.rect(bx, base, bw2, bh, fill=1, stroke=0)
        c.setFont(FONT_DISPLAY_BOLD, 8); c.setFillColor(DEEP_GREEN)
        c.drawCentredString(bx + bw2 / 2, base + bh + 5, right_fmt(v))
        c.setFont(FONT_BODY_BOLD, 6.5); c.setFillColor(GREY)
        c.drawCentredString(bx + bw2 / 2, base - 10, lab)


def gold_callout(c, y, text):
    """Gold accent bar + bold-italic line (the 'materially tracking ahead' pattern)."""
    c.setFillColor(GOLD); c.rect(X, y - 20, 2.5, 24, fill=1, stroke=0)
    wrap(c, X + 12, y - 4, text, "Times-BoldItalic", 9, DEEP_GREEN, CONTENT_W - 12, 12)
    return y - 36


def numbered_and_kv(c, y, left_title, numbered_items, right_title, kv_pairs, left_w=310):
    """Two-column block: numbered gold list left, key-value column right."""
    rx = X + left_w + 24
    sect(c, X, y, left_title, size=12)
    sect(c, rx, y, right_title, size=12)
    c.setStrokeColor(HAIR); c.setLineWidth(0.8)
    c.line(rx - 14, y - 96, rx - 14, y + 8)
    yy = y - 18
    for i, item in enumerate(numbered_items):
        c.setFont(FONT_BODY_BOLD, 8.2); c.setFillColor(LABEL_GOLD)
        c.drawString(X, yy, f"{i+1}.")
        c.setFont(FONT_BODY, 8.4); c.setFillColor(DEEP_GREEN)
        c.drawString(X + 12, yy, item)
        yy -= 12.5
    ty = y - 20
    for lab, val in kv_pairs:
        spaced(c, rx, ty, lab.upper(), FONT_BODY_BOLD, 6.2, LABEL_GOLD, 0.8)
        c.setFont(FONT_DISPLAY_BOLD, 9.5); c.setFillColor(DEEP_GREEN)
        c.drawString(rx, ty - 10.5, val)
        ty -= 21
    return min(yy, ty)


def footnotes(c, lines, y0=87, lh=9):
    c.setFont("Helvetica-Oblique", 6.6); c.setFillColor(GREY)
    y = y0
    for ln in lines:
        c.drawString(X, y, ln)
        y -= lh


def footer_strip(c, name, role, contact_line, cta_head="NEXT STEP: EXECUTE AN NDA",
                 cta_sub="CIM, pricing and full financial package available to qualified buyers."):
    """Deep-green footer bookend with gold top hairline and contact."""
    FS = 54
    c.setFillColor(DEEP_GREEN); c.rect(0, 0, W, FS, fill=1, stroke=0)
    c.setFillColor(GOLD); c.rect(0, FS, W, 1.5, fill=1, stroke=0)
    c.setFont(FONT_DISPLAY_BOLD, 11); c.setFillColor(WHITE)
    c.drawString(X, FS - 22, name)
    nw = c.stringWidth(name, FONT_DISPLAY_BOLD, 11)
    c.setFont(FONT_BODY, 8.6); c.setFillColor(GOLD)
    c.drawString(X + nw + 7, FS - 22, role)
    c.setFont(FONT_BODY, 8.4); c.setFillColor(MUTED)
    c.drawString(X, FS - 37, contact_line)
    spaced(c, X + CONTENT_W, FS - 22, cta_head, FONT_BODY_BOLD, 8, GOLD, 1.2, right=True)
    c.setFont(FONT_BODY, 7.8); c.setFillColor(MUTED)
    c.drawRightString(X + CONTENT_W, FS - 37, cta_sub)


# ---- orchestrator ----
def build_teaser(d, out_path):
    """Build the one-page teaser from a data dict. See EXAMPLE_DATA for shape.
    Raises ValueError if content overflows the single page."""
    for key in ("title", "descriptor", "opener", "bullets", "metrics",
                "fin_left_series", "fin_right_series", "growth_items",
                "transaction_kv", "footnotes", "contact"):
        if key not in d:
            raise ValueError(f"Missing required teaser field: {key}")
    if len(d["bullets"]) > 7:
        raise ValueError("Max 7 proof bullets on a one-page teaser.")
    if len(d["metrics"]) != 3:
        raise ValueError("Exactly 3 hero metrics.")
    if len(d["growth_items"]) > 7:
        raise ValueError("Max 7 growth items.")
    for s in ("opener", "industry_line", "callout"):
        if "—" in d.get(s, ""):
            raise ValueError(f"Em dash found in '{s}' - rewrite with commas/colons (en dash only for ranges).")

    c = canvas.Canvas(out_path, pagesize=letter)
    c.setFillColor(WHITE); c.rect(0, 0, W, H, fill=1, stroke=0)
    header_band(c, d["title"], d["descriptor"])

    y = 676 - 24
    y = wrap(c, X, y, d["opener"], FONT_BODY, 9.5, DEEP_GREEN, CONTENT_W, 13)
    y -= 4
    y = bullet_rows(c, y, d["bullets"])
    y -= 12
    y = metric_strip(c, y, d["metrics"])

    rule(c, X, y, CONTENT_W, HAIR, 0.8); y -= 17
    sect(c, X, y, "Financial Performance")
    if d.get("fin_kicker"):
        spaced(c, X + CONTENT_W, y + 1, d["fin_kicker"].upper(), FONT_BODY_BOLD, 6.5, LABEL_GOLD, 1.0, right=True)
    y -= 8
    CHT = 100
    dual_bar_charts(c, X + 4, y, CONTENT_W - 8, CHT,
                    d.get("fin_left_title", "Revenue (CAD)"), d["fin_left_series"],
                    d.get("fin_right_title", "Normalized EBITDA (CAD)"), d["fin_right_series"])
    y -= CHT + 14

    if d.get("industry_line"):
        rule(c, X, y, CONTENT_W, HAIR, 0.8); y -= 17
        sect(c, X, y, "Industry Overview", size=12)
        y -= 14
        y = wrap(c, X, y, d["industry_line"], FONT_BODY, 8.4, GREY, CONTENT_W, 11)
        y -= 6
    if d.get("callout"):
        y = gold_callout(c, y, d["callout"])

    rule(c, X, y, CONTENT_W, HAIR, 0.8); y -= 17
    y = numbered_and_kv(c, y, "Growth Opportunities", d["growth_items"],
                        "Transaction", d["transaction_kv"])
    if y < 100:
        raise ValueError(f"Content overflows the page (bottom y={y:.0f} < 100). Cut content; do NOT shrink fonts.")

    footnotes(c, d["footnotes"])
    ct = d["contact"]
    footer_strip(c, ct["name"], ct["role"], ct["line"],
                 d.get("cta_head", "NEXT STEP: EXECUTE AN NDA"),
                 d.get("cta_sub", "CIM, pricing and full financial package available to qualified buyers."))
    c.showPage(); c.save()
    return out_path


# ---- reference example (Project Eros, July 2026 - the locked format) ----
EXAMPLE_DATA = {
    "title": "Western Canada's Premier Specialty Archery Retailer",
    "descriptor": "Western Canada   ·   Specialty Retail & E-Commerce",
    "opener": ("A leading specialty archery retailer and fast-growing e-commerce operator, among the largest "
               "dedicated archery pro shops in Western Canada by volume. A single showroom and warehouse "
               "location plus a Shopify store shipping nationwide. The primary owner is retiring."),
    "bullets": [
        "25+ year customer base, in store, online and across Canada",
        "Two leading archery brands not available through its primary competitor; 1 of 5 national apparel dealerships",
        "Online revenue averaging ~$96K/month, grown organically",
        "Black Friday: ~700 orders in 4 days each year",
        "Pricing power: margins held through the 2024 tariff and FX volatility",
        "Debt-free: ~$1.4M shareholder equity, $1.7M+ current inventory, no long-term debt",
        "Management and sales team in place and staying; expert phone and product advice is a key differentiator",
    ],
    "metrics": [("$3.19M", "FY2025 Revenue"), ("$299K", "FY2025 Norm. EBITDA"), ("8.5%", "3-Yr Revenue CAGR")],
    "fin_kicker": "Total revenue growth FY2023–FY2025: +19%",
    "fin_left_series": [("FY2023", 2690468), ("FY2024", 2784597), ("FY2025", 3190957)],
    "fin_right_series": [("FY2023", 216466), ("FY2024", 168420), ("FY2025", 299447)],
    "industry_line": ("The global archery equipment market is estimated at up to US$4.4B, growing ~5% annually; North "
                      "America represents ~38% of demand with 4M+ active bowhunters. The category is fragmented and "
                      "consolidating, with demand shifting online."),
    "callout": ("FY2026 is materially tracking ahead: $1.7M total revenue (+31% YTD) and $500K online "
                "in the first six months, ahead of the same period in FY2025."),
    "growth_items": [
        "Paid digital and social media marketing, near-zero spend today",
        "FX / treasury: USD buying unhedged, margin upside",
        "Email marketing and customer loyalty program",
        "Lessons, coaching and corporate programming",
        "Range expansion and event programming",
        "Working capital: ~$750K unlock via an inventory-backed line",
        "Proven single-store model ready for multi-location and further online expansion",
    ],
    "transaction_kv": [("Structure", "Share Sale"), ("Fiscal Year End", "November 30"),
                       ("Transition", "Up to 6 months"), ("Pricing", "Available on NDA")],
    "footnotes": [
        "Normalized EBITDA = EBITDA per compiled financial statements plus a $50,000 annual owner-compensation add-back. Revenue CAGR measured FY2022–FY2025.",
        "Prepared by ScalePoint M&A on behalf of the vendor; strictly confidential and not an offer to sell. Information is provided by the vendor and has not been",
        "independently verified. July 2026 | scalepointma.com",
    ],
    "contact": {"name": "Alina Martin", "role": "CEO & Co-Founder",
                "line": "403-701-0020   ·   alina.martin@scalepointma.com   ·   scalepointma.com"},
}

if __name__ == "__main__":
    import sys
    out = sys.argv[1] if len(sys.argv) > 1 else "teaser_example.pdf"
    print("saved", build_teaser(EXAMPLE_DATA, out))
