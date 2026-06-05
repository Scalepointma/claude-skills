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

**Accent rotation:** `[GOLD, TEAL, GOLD, OLIVE, GOLD, TEAL]` — gold is dominant,
olive and teal provide contrast. Never repeat a color in adjacent positions.

---

## 2. Typography

Brand fount is **Libre Baskerville** (Bold + Regular). ReportLab's PostScript
fonts do not include Libre Baskerville, so we pair:

| Role | Font (ReportLab) | Brand equivalent |
|---|---|---|
| Section titles, subheadings, stat numbers, card titles, table headers, deal tombstones, TOC | **Times-Bold** | Libre Baskerville Bold |
| Italic pull-quotes, taglines, subtitles | **Times-Italic** | Libre Baskerville Italic |
| Body copy, bullet lists, table cells, footnotes, card body | **Helvetica** | sans body for readability |
| Kickers (small uppercase), labels | **Helvetica-Bold** | crisp sans for small caps |

To upgrade to true Libre Baskerville later, register TTFs via
`pdfmetrics.registerFont()` before calling the skill.

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
| Stacked on dark (icon + gold wordmark box, green bg) | Full covers, hero blocks on deep-green | `logo-stacked-on-dark.png` |
| White reverse (all white on dark) | Back covers, dark footers | `logo-white.png` |
| Icon only — full color | Footer icon, small brand marks | `icon-fullcolor.png` |
| Icon only — gold | Monochrome gold applications | `icon-gold.png` |
| Pattern — light bg | Subtle watermark textures | `pattern-light.png` |

**Forbidden** (per brand guide): stretching/skewing, re-typing wordmark,
white logo on pale background, graphic effects, placement on high-contrast
photo backgrounds (always duotone the photo first), changing relative size of
icon vs wordmark.

---

## 9. Asset Discovery

`discover_assets()` searches these paths for canonical filenames:

- `/sessions/*/mnt/*/scalepoint-report-format*/assets`
- `/sessions/*/mnt/**/scalepoint-report-format*/assets`
- `/sessions/*/mnt/.claude/skills/scalepoint*/assets`
- `/sessions/*/mnt/outputs/scalepoint-report-format/assets`
- `/sessions/*/mnt/uploads`

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
