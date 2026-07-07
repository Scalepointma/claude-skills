---
name: scalepoint-report-format
description: >
  Produces boardroom-quality, print-ready PDFs in ScalePoint M&A's brand
  visual style using ReportLab. MANDATORY TRIGGER: use this skill ANY time
  the user asks to create a PDF, report, CIM, confidential information
  memorandum, teaser, blind profile, valuation report, opinion of value,
  engagement proposal, deal proposal, pitch document, one-pager, brochure,
  leave-behind, deal tombstone, closing binder cover, or any printable
  document for ScalePoint M&A or for ScalePoint's clients / sellers /
  buyers. Also trigger when the user mentions "boardroom PDF," "ScalePoint
  brand," "Build/Buy/Sell brochure," "annual report style," "polished PDF,"
  or references the ScalePoint brand guide as a visual template. This skill
  overrides the generic print-pdf-from-html skill for all ScalePoint work.
  If the user says "make it look like the brand guide" or "use the
  ScalePoint format," this is the skill.
---

# ScalePoint M&A Report Format Skill

## Step 0: Read the Full Reference Files (MANDATORY)

This skill is intentionally lean. Full design specs and helper modules live
**in this skill's folder** — the directory containing this SKILL.md. You know
that path because you just read this file; call it `ref_dir`. Never search
absolute or machine-specific paths for it.

```python
import sys, os
ref_dir = "<directory containing this SKILL.md>"
scripts_dir = os.path.join(ref_dir, "scripts")
assets_dir  = os.path.join(ref_dir, "assets")
sys.path.insert(0, scripts_dir)
```

**Read these BEFORE writing ANY code:**

Read from `ref_dir`:
1. **BRAND-GUIDE.md** — colors, fonts, page frame, element heights, visual
   weight hierarchy, photography treatment, logo usage, voice & tone.
2. **DESIGN-RULES.md** — content→layout decision tree, document-type presets
   (brochure / teaser / CIM / valuation / proposal), anti-pattern checklist
   (28 items), layout verification checklist (10 items), widow/orphan rules.

## Step 1: Content Handling — ASK FIRST

> "Are you providing existing content for me to format, or would you like me
> to help author new content? Or a mix?"

- **Existing content**: Preserve EVERY word. DO NOT edit / rewrite / summarize.
  Flag suspected errors but do not fix them without approval.
- **Authoring**: Draft normally; user reviews before finalizing. Use the
  ScalePoint voice from BRAND-GUIDE.md §10 (founder-led, operator-to-operator,
  plain-spoken, no buzzwords).
- After building: confirm "I preserved all original content without edits."

## Step 1.5: Content Inventory (MANDATORY)

Before choosing ANY layouts, inventory the source content:

1. List every section with heading, approximate word count, content type.
2. Flag missing / suspect content — ask the user.
3. Map each section to an element type using the decision tree in
   DESIGN-RULES.md §2.
4. Estimate page count from element heights in BRAND-GUIDE.md §4.
5. Run `clean_text()` on ALL extracted text.

## Step 2: Asset Discovery & Module Import

```bash
python3 -c "import reportlab, PIL, pypdfium2" 2>/dev/null || \
  python3 -m pip install reportlab Pillow pypdfium2 --quiet --break-system-packages
```

```python
import sys, os
sys.path.insert(0, scripts_dir)   # scripts_dir / assets_dir from Step 0

from scalepoint_pdf import *
from reportlab.pdfgen import canvas

assets = discover_assets(extra_dirs=[assets_dir])
```

Available assets (canonical names): `logo-primary`, `logo-stacked`,
`logo-white`, `icon-fullcolor`, `icon-gold`, `pattern-light`, `cover-bg`.

**Do NOT rewrite the helper functions.** Import and use as-is.

## Step 3: Pick a Document Preset

See DESIGN-RULES.md §3 for full patterns. Quick picks:

- **Boardroom document** (CIM, valuation, proposal, closing binder):
  `draw_front_cover()` → content pages with `draw_page_setup()` frame →
  `draw_back_cover()`.
- **Brochure / leave-behind**: `draw_brochure_hero()` OR
  `draw_duotone_hero()` + `draw_logo_pill()` → `draw_pillar_row()`
  (Build / Buy / Sell) → narrative → `draw_contact_strip()`.
- **Teaser / blind profile**: use the dedicated `scalepoint-teaser` skill
  (locked one-page format). For a teaser-style cover inside another doc:
  `draw_teaser_cover()` (three-zone, sepia hero badges) — NEVER the heavy
  boardroom `draw_front_cover()` on a teaser.

## Step 4: Plan ALL Pages, Then Build

Plan every page with y-coordinates BEFORE coding. Use the Page Plan
Template from DESIGN-RULES.md §1.

**The #1 visual rule:** white cards with accent bars — accent is a SINGLE
consistent GOLD by default; break it up only with the deliberate palette
helpers (`card_grid_rows` per-row, `cards_by_column` per-column,
`draw_stat_row(accent_color=DEEP_GREEN)` for a second row). NO dark-filled
cards (max 1 reverse-tint per page). 10pt corners everywhere.
NO em dashes in any copy (commas/colons; en dash for numeric ranges only).
Descriptors under numbers are always the standard ALL-CAPS gold 8pt
(`draw_descriptor`). GOLD_LIGHT is never a text colour.

**The #1 layout rule:** use `ensure_space()` before drawing any element
near the bottom. Use `draw_title_group()` for all kicker+subheading
combinations. Use `draw_footnote()` for disclaimers (NOT callout boxes).

**The #1 photography rule:** all photos pass through
`draw_duotone_hero()` or `draw_pillar_row(images_as_duotone=True)`.
Never drop a full-color photo into a ScalePoint document.

## Step 5: Key Functions Reference

All drawing functions return the y-position after drawing, for stacking.

### Page Setup
| Function | Purpose |
|---|---|
| `draw_page_setup(c, doc_title, page_num, icon_path, section_label)` | Background + header hairline + branded footer |
| `draw_page_bg(c)` | Paint cream page bg only |
| `ensure_space(c, y, needed_h, doc_title, page_num, icon_path, section_label)` | Auto page-break |

### Titles & Text
| Function | Purpose |
|---|---|
| `draw_title_group(c, x, y, kicker, subheading, intro_text, section_title, new_section)` | Complete title group with internal spacing |
| `draw_section_title(c, x, y, text, size=28)` | Large serif section title |
| `draw_kicker(c, x, y, text)` | Letter-spaced uppercase, gold |
| `draw_subheading(c, x, y, text, size=20)` | Serif sub-section heading — 20pt STANDARD (hierarchy: 28 heading > 20 subhead > hero/caption > 10 body) |
| `draw_body_text(c, x, y, text)` | 10pt Helvetica body |
| `draw_divider(c, x, y, ...)` | Thin gold accent line |

### Cards
| Function | Purpose |
|---|---|
| `draw_card(c, x, y, w, h, title, body, accent_color, accent_position)` | Single card with accent bar (default GOLD) |
| `card_grid_rows(c, x, y, cards, cols, row_colors)` | Grid, one colour PER ROW (gold/green/olive) — the approved highlight grid |
| `cards_colored(c, x, y, cards, colors, cols)` | One row, each card its own colour (persona cards) |
| `draw_card_grid(c, x, y, cards, cols, card_h, gap, auto_height)` | Plain grid (single gold accent) |
| `draw_numbered_card(c, x, y, w, h, number, kicker, title, body)` | Gold card + DEEP-GREEN number badge; single-line rows vertically centered |
| `kv_card(c, x, y, w, h, value, label, accent_color)` | Value card: serif value + standard gold descriptor |
| `cards_by_column(c, x, y, cards, cols, col_colors, card_h)` | Value grid, one colour PER COLUMN (2 gold / 2 green / 2 olive) |
| `calculate_card_height(c, title, body, width)` | Measure minimum card height |

### Stats
| Function | Purpose |
|---|---|
| `draw_stat_box(c, x, y, w, h, number, label, accent_color)` | Single stat; descriptor is ALWAYS the standard gold |
| `draw_stat_row(c, x, y, stats, gap, accent_color)` | Row of stat boxes, ONE colour per row (default GOLD; 2nd row: DEEP_GREEN) |
| `draw_descriptor(c, cx, y, label)` | THE standard descriptor: ALL CAPS, #A9803A, 8pt, letter-spaced |
| `spaced(c, x, y, text, font, size, color, tracking, center, right)` | Letter-spaced caps text |

### Callouts
| Function | Purpose |
|---|---|
| `draw_light_callout(c, x, y, w, h, text)` | Gold-tinted + left accent — for emphasis |
| `draw_callout_bar(c, x, y, w, h, text)` | Deep-green bar with gold text — takeaways |
| `draw_reverse_tint(c, x, y, w, h, title, body)` | Dark hero card — MAX 1 PER PAGE |

### Tables & Lists
| Function | Purpose |
|---|---|
| `draw_table(c, x, y, col_widths, headers, rows, total_row, highlight_rows)` | Deep-green header + gold total row |
| `draw_bullet_list(c, x, y, items, max_width, bold_prefix)` | Gold bullets, wrapping |
| `draw_toc(c, x, y, entries)` | Dark pills with gold page-number chips |
| `draw_footnote(c, x, y, text)` | 8pt italic muted — NO box |

### Covers & Brochure
| Function | Purpose |
|---|---|
| `draw_front_cover(c, title, subtitle, date, logo_stacked_path, cover_bg_path)` | Boardroom dark-green cover (large trimmed logo, no stray rules) |
| `draw_teaser_cover(c, kicker, title_lines, descriptor, attributes_line, metrics, footer_line, logo_stacked_path)` | Three-zone teaser cover: logo / title group / sepia hero badges; codename in the kicker |
| `hero_badge(c, x, y, w, h, num, label)` | Sepia face + gold top accent hero metric badge |
| `info_badge(c, cx, y, w, h, name=, role=, phone=, email=, website=, accent_color=)` | Contact badge: white face; gold accent on dark pages, deep-green on light; each line its own row |
| `draw_brochure_hero(c, y_top, height, hero_image_path, title_text, subtitle_text)` | Canva-style photo hero with title pill |
| `draw_duotone_hero(c, x, y_top, w, h, image_path, overlay_opacity, gold_waves)` | Duotone photo + gold topographic lines |
| `draw_logo_pill(c, x, y, w, h, logo_icon_path, logo_text)` | Gold-outlined [icon] [wordmark] pill |
| `draw_back_cover(c, logo_path, year, tagline, website, email, contact_name, contact_role, contact_phone)` | Deep-green back: 21pt gold tagline + white contact info badge; pass the STACKED logo |

### M&A-Specific
| Function | Purpose |
|---|---|
| `draw_deal_tombstone(c, x, y, w, h, deal_name, sector, transaction_value, role, close_date)` | Closed-deal block |
| `draw_deal_tombstone_grid(c, x, y, deals, cols, h, gap)` | Grid of deal tombstones |
| `draw_pillar_row(c, x, y_top, pillars, image_h, card_h, images_as_duotone)` | Build / Buy / Sell 3-column block |
| `draw_contact_strip(c, x, y, phone, email, website, cta_text)` | Gold CTA button + green contact bar |

### Layouts
| Function | Purpose |
|---|---|
| `draw_bento_layout(c, x, y, items, style)` | Asymmetric card grid (A/B/C) |
| `get_two_column_x(col)` | Returns `(x, width)` for 2-col layouts |

### Measurement & Safety
| Function | Purpose |
|---|---|
| `measure_text_height(c, text, max_width, font, size, leading)` | Calculate text height without drawing |
| `will_fit(y, height)` | Check element fits above footer zone |
| `remaining_height(y)` | Points of space remaining |
| `clean_text(text)` | Normalize quotes, strip control chars, ENFORCE the dash rule (em dash → comma; en dash only in numeric ranges) |
| `assert_no_em_dash(*texts)` | Hard check for generated copy — raises on any em dash |
| `discover_assets(extra_dirs)` | Find brand assets in the skill's own assets/ folder (auto-trims logos) |
| `trim_image(path)` / `image_ratio(path)` | Trim logo padding; true aspect ratio for sizing |

### Constants
| Name | Value | Purpose |
|---|---|---|
| `MARGIN` | 50 | Page margins |
| `CONTENT_W` | 512 | Available content width |
| `CONTENT_TOP` | ~736 | Y where content starts |
| `FOOTER_ZONE_TOP` | ~52 | Y below which nothing may be drawn |
| `CONTENT_HEIGHT` | ~684 | Total available vertical space |

## Step 6: Visual Verification (MANDATORY)

```python
import pypdfium2 as pdfium
doc = pdfium.PdfDocument('output.pdf')
for i, page in enumerate(doc):
    page.render(scale=2).to_pil().save(f'page_{i+1}.png')
```

View EVERY page as PNG. Check against the 29-item anti-pattern checklist
AND the 10-item layout verification checklist in DESIGN-RULES.md.

## Step 7: Deliver

Write to workspace folder. Use a descriptive filename (e.g.,
`ScalePoint_Crown_Holdings_Teaser_2026.pdf`). Present with `computer://` link.
Confirm content integrity: "I preserved all original content without edits."
