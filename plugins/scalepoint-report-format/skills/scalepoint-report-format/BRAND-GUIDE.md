# ScalePoint M&A — Visual Brand Guide

This is the production brand guide for PDF outputs. It captures the colors,
typography, page frame, element heights, and composition rules the Python
modules enforce. Source: official ScalePoint Brand Guidelines PDF + Social
Media Kit + scalepointma.com.

---

## 1. Color Palette

| Role | Name | Hex | Python const |
|---|---|---|---|
| Primary background / dark text | Deep Green | `#0A2D2A` | `DEEP_GREEN` |
| Deeper variant (back cover) | Deep Green Dk | `#061C1A` | `DEEP_GREEN_DK` |
| Primary accent | Gold | `#CB9D43` | `GOLD` |
| Gold gradient mid | Gold Deep | `#D7A848` | `GOLD_DEEP` |
| Gold gradient light | Gold Light | `#F6E279` | `GOLD_LIGHT` |
| Secondary (supporting) | Olive | `#869846` | `OLIVE` |
| Secondary (supporting) | Teal | `#18766A` | `TEAL` |
| Page background | Cream | `#FAF8F2` | `CREAM` / `PAGE_BG` |
| Warm off-white (callouts, table rows) | Near White | `#F7F5EF` | `NEAR_WHITE` |
| Body copy | Deep Green | `#0A2D2A` | `BODY_COLOR` |
| Muted / footnotes | Muted Green-Grey | `#4A5B58` | `SECONDARY_COLOR` |
| Micro-copy | Light Sage | `#8A9995` | `LIGHT_TEXT` |

**Accent discipline (2026-07 revision):** the default accent is a SINGLE
consistent **GOLD** — the old random gold/teal/olive rotation is retired (it
read as random and cheap). Break up gold **deliberately and evenly** only via
the palette helpers: per-ROW in card grids (`card_grid_rows`: gold / deep
green / olive), per-COLUMN in value grids (`cards_by_column`: 2 gold / 2
green / 2 olive), a second stat row in deep green
(`draw_stat_row(accent_color=DEEP_GREEN)`), and deep-green number badges on
gold numbered rows. Never a per-card random mix.

**Standard descriptor:** the small label under any hero number, stat box or
value card is ALWAYS: ALL CAPS, `LABEL_GOLD` `#A9803A`, 8pt, letter-spaced
(`draw_descriptor`) — identical everywhere, whatever the accent bar colour.

**GOLD_LIGHT `#F6E279` is never a text colour** — it exists only inside the
gold gradient bar.

---

## 2. Typography

Brand fount is **Libre Baskerville** — the TTFs are BUNDLED in
`assets/fonts/` (OFL licensed) and registered automatically when
`scalepoint_base` is imported. `FONT_DISPLAY` / `FONT_DISPLAY_BOLD` /
`FONT_DISPLAY_ITALIC` resolve to Libre Baskerville; if the TTFs are missing
the module warns and falls back to Times.

| Role | Font const | Face |
|---|---|---|
| Section titles, subheadings, stat numbers, card titles, table headers, deal tombstones, TOC | `FONT_DISPLAY_BOLD` | Libre Baskerville Bold |
| Italic pull-quotes, taglines, subtitles | `FONT_DISPLAY_ITALIC` | Libre Baskerville Italic |
| Body copy, bullet lists, table cells, footnotes, card body | `FONT_BODY` (Helvetica) | sans body for readability |
| Kickers (small uppercase), labels | `FONT_BODY_BOLD` | crisp sans for small caps |

**Type hierarchy is an ALWAYS rule — check every page:**
heading (28pt) > **subhead (20pt serif)** > hero/caption fonts > body (10pt).
A subhead must be visibly larger than the page's callout/caption text and
smaller than the heading, with enforced space above and below.

**No em dashes in any content, ever** — rewrite with commas, colons, or
shorter sentences. En dash is allowed ONLY inside numeric ranges
($1.19M–$1.36M, Net 30–120, FY2023–FY2025). `clean_text()` enforces this
mechanically; write it correctly in the first place.

---

## 3. Page Frame

```
y=792 ┌────────────────────────────────────────────────┐
      │  · · · (quiet header gutter) · · ·              │   ← HEADER_H=36
y=754 ├────────  ── gold hairline accent ──  ──────────┤   ← HEADER_ACCENT_H=2
      │                                                 │
      │            CONTENT AREA (CONTENT_W=512)         │   ← CONTENT_TOP≈736
      │                                                 │
      │              ... your content ...               │
      │                                                 │
y= 52 │  [icon] [─── DEEP GREEN BAR ───][ GOLD | 01 ]   │   ← FOOTER_ZONE_TOP
y=  0 └────────────────────────────────────────────────┘   ← FOOTER_H=30
```

Margins: 50pt on all sides. Content width: 512pt. Content height: ~684pt.

**Footer is the ScalePoint signature** — echoing the brand guide PDF's own
page template:
- Small icon (fullcolor or gold) at bottom-left
- Deep-green bar spanning most of the footer, holding section label in
  white serif
- Gold segment at the right ~90pt wide, holding page number in deep-green serif
- Thin "Confidential | ScalePoint M&A" micro-line below the bar

---

## 4. Element Heights Reference

Use these when planning pages (sum heights + inter-element gaps to verify fit).

| Element | Height | Notes |
|---|---|---|
| Section title | size + 4 (default 32pt) | `draw_section_title()` |
| Kicker + subhead group | ~55 | `draw_title_group()` handles spacing |
| Body paragraph (1 line) | 13 | 10pt at 13pt leading |
| Body paragraph (3 lines) | ~39 | per `measure_text_height()` |
| Card (2-col, standard) | 110-130 | `card_h=120` default |
| Numbered card (single) | 130-160 | slightly taller for badge |
| Stat row (3 boxes) | 82 | box height constant |
| Table (per row) | 24 | +30 for header, +24 for total row |
| TOC entry | 36 + 8 gap | |
| Callout bar | 40-56 | |
| Light callout | 60-90 | |
| Reverse-tint hero | 100-160 | **max 1 per page** |
| Duotone hero (brochure) | 200-280 | full-width, with gold waves |
| Pillar row (image + card) | 80 + 140 = 220 | 3-column Build/Buy/Sell block |
| Contact strip CTA | ~72 | button floats above bar |
| Deal tombstone | 80 | 2-col grid typical |
| Footnote (per line) | 10.5 | |

---

## 5. Visual Weight Hierarchy

Top → bottom:

1. **Front cover / hero** — largest type, deep green bg, gold accents
2. **Section title** (28pt Times-Bold) — one per page
3. **Subheading** (22pt Times-Bold)
4. **Card title** (13pt Times-Bold) / **Stat number** (34pt Times-Bold)
5. **Kicker** (9pt Helvetica-Bold, uppercase, letter-spaced) — gold
6. **Body** (10pt Helvetica) — deep green
7. **Footnote / micro-copy** (8pt Helvetica-Oblique) — muted

Never invert: a footnote should never look heavier than body text.

---

## 6. Card Discipline

**The #1 visual rule:** white cards with accent bars. Accent bar = 5pt sliver
revealed by drawing a full-color rounded rect, then a slightly smaller white
rounded rect on top. Left accent is default; top accent for horizontal hero
cards.

- Corner radius: **10pt** everywhere. NEVER square corners. NEVER 8pt.
- Drop shadow: opacity 0.06, offset 2pt — subtle only.
- Accent rotation enforced horizontally AND vertically in grids.
- **Max 1 dark/reverse-tint card per page** (for hero elements). Everything
  else is white-card-with-accent.

---

## 7. Photography Treatment — "Social Media Kit" Style

Photos in ScalePoint materials are **duotone** (not full color):

- Convert to grayscale, then colorize across `DEEP_GREEN` → warm near-white
  (`#E8E4D7`).
- Overlay a 40-55% deep-green tint on top for additional tonal compression.
- **Overlay gold topographic wave lines** across the hero panel — the
  sinusoidal-lines motif visible in the social media banners. Use
  `draw_duotone_hero(..., gold_waves=True)`.
- Photo always enclosed in a gold-outlined rounded rectangle for polish.

This treatment is applied by `draw_duotone_hero()` and
`draw_pillar_row(images_as_duotone=True)`.

---

## 8. Logo Usage

| Lockup | When to use | Asset file |
|---|---|---|
| Primary horizontal (icon + gold wordmark in outlined box) | Standard headers, letterheads, small hero panels | `logo-primary-horizontal.png` |
| Stacked on dark (icon + gold wordmark box, green bg) | Full covers, hero blocks on deep-green, **back covers** | `logo-stacked-on-dark.png` |
| White reverse | ⚠️ has an opaque BLACK background baked in — never place on a colour field; effectively unused until re-exported with transparency | `logo-white.png` |
| Icon only — full color | Footer icon, small brand marks | `icon-fullcolor.png` |
| Icon only — gold | Monochrome gold applications | `icon-gold.png` |
| Pattern — light bg | Subtle watermark textures | `pattern-light.png` |

**Logos must be TRIMMED before placing** — the PNGs ship with huge dead
padding (the stacked logo is ~27% content), which makes them render ~3x too
small in fixed boxes. `discover_assets()` auto-trims; if you place a logo
manually, run it through `trim_image()` and size with `image_ratio()`.
**Covers want a LARGE logo** (~250pt wide stacked lockup).

**Never draw a decorative rule/line directly under the logo** — the lockup
already has its wordmark pill.

**Forbidden** (per brand guide): stretching/skewing, re-typing wordmark,
white logo on pale background, graphic effects, placement on high-contrast
photo backgrounds (always duotone the photo first), changing relative size of
icon vs wordmark.

---

## 9. Asset Discovery

`discover_assets()` looks in this skill's own `assets/` folder (relative to
the scripts module — works identically on any machine, plugin install, or
claude.ai skill upload). Pass `extra_dirs=[...]` to prepend other locations
(e.g. a session uploads folder). Logos/icons are auto-trimmed on discovery.

Canonical names: `logo-primary`, `logo-stacked`, `logo-white`, `icon-fullcolor`,
`icon-gold`, `pattern-light`, `cover-bg`.

If an asset is missing, `discover_assets()` prints it. Fallbacks exist for the
icon (a drawn triangle + peaks) but NOT for the logos — always prefer
PNG variants from the Marketing folder.

---

## 10. Voice & Tone (for authored content)

From scalepointma.com and Jodi's positioning:

- **Founder-led, operator-to-operator.** "We've built. We've bought. We've sold."
- **Honest & plain-spoken.** Avoid buzzwords, jargon, hype.
- **Selective.** Focus on $1M–$25M owner-operated businesses. Say no to
  pre-revenue / early-stage.
- **Relationship-first, no-pressure.** "If you're ready to be thoughtful about
  what comes next—we should talk."
- **Experienced.** 150+ companies advised. 40+ years operating.
- **Three pillars.** Build. Buy. Sell.

Do not write: "revolutionize," "synergy," "game-changing," "next-generation,"
"world-class."
