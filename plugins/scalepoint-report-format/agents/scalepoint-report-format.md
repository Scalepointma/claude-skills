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
in the skill folder. **Read these BEFORE writing ANY code:**

```python
import glob, os

SKILL_LOCAL = "/Users/delta/delta/templates/scalepoint-report-format"

ref_dir = None
# Local Delta machine path — always check first
if os.path.isdir(SKILL_LOCAL):
    ref_dir = SKILL_LOCAL
else:
    # Cowork / remote session fallback
    for pattern in [
        "/sessions/*/mnt/*/scalepoint-report-format*/BRAND-GUIDE.md",
        "/sessions/*/mnt/**/scalepoint-report-format*/BRAND-GUIDE.md",
        "/sessions/*/mnt/.claude/skills/scalepoint-report-format*/BRAND-GUIDE.md",
        "/sessions/*/mnt/outputs/scalepoint-report-format/BRAND-GUIDE.md",
    ]:
        found = glob.glob(pattern, recursive=True)
        if found:
            ref_dir = found[0].rsplit("/", 1)[0]
            break
```

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
pip install reportlab Pillow pdf2image --break-system-packages
```

```python
import sys, glob, os

SKILL_LOCAL = "/Users/delta/delta/templates/scalepoint-report-format"

scripts_dir = None
if os.path.isdir(os.path.join(SKILL_LOCAL, "scripts")):
    scripts_dir = os.path.join(SKILL_LOCAL, "scripts")
else:
    for pattern in [
        "/sessions/*/mnt/*/scalepoint-report-format*/scripts",
        "/sessions/*/mnt/**/scalepoint-report-format*/scripts",
        "/sessions/*/mnt/.claude/skills/scalepoint*/scripts",
        "/sessions/*/mnt/outputs/scalepoint-report-format/scripts",
    ]:
        found = glob.glob(pattern, recursive=True)
        if found:
            scripts_dir = found[0]
            break

if scripts_dir:
    sys.path.insert(0, scripts_dir)

from scalepoint_pdf import *
from reportlab.pdfgen import canvas

assets = discover_assets()
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
- **Teaser / blind profile**: `draw_page_setup()` from page 1 (no cover) →
  serif section title → body + stat row + pull-quote → footnote
  confidentiality line.

## Step 4: Plan ALL Pages, Then Build

Plan every page with y-coordinates BEFORE coding. Use the Page Plan
Template from DESIGN-RULES.md §1.

**The #1 visual rule:** white cards with gold/teal/olive accent bars.
NO dark-filled cards (max 1 reverse-tint per page for hero elements).
10pt corners everywhere.

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
| `draw_subheading(c, x, y, text, size=22)` | Serif sub-section heading |
| `draw_body_text(c, x, y, text)` | 10pt Helvetica body |
| `draw_divider(c, x, y, ...)` | Thin gold accent line |

### Cards
| Function | Purpose |
|---|---|
| `draw_card(c, x, y, w, h, title, body, accent_color, accent_position, accent_index)` | Single card with accent bar |
| `draw_card_grid(c, x, y, cards, cols, card_h, gap, auto_height)` | Grid with color adjacency |
| `draw_numbered_card(c, x, y, w, h, number, kicker, title, body)` | Numbered badge card — for steps / phases |
| `calculate_card_height(c, title, body, width)` | Measure minimum card height |

### Stats
| Function | Purpose |
|---|---|
| `draw_stat_box(c, x, y, w, h, number, label, accent_color)` | Single stat with big serif number |
| `draw_stat_row(c, x, y, stats, gap)` | Row of stat boxes, auto color rotation |

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
| `draw_front_cover(c, title, subtitle, date, logo_stacked_path, cover_bg_path)` | Boardroom dark-green cover |
| `draw_brochure_hero(c, y_top, height, hero_image_path, title_text, subtitle_text)` | Canva-style photo hero with title pill |
| `draw_duotone_hero(c, x, y_top, w, h, image_path, overlay_opacity, gold_waves)` | Duotone photo + gold topographic lines |
| `draw_logo_pill(c, x, y, w, h, logo_icon_path, logo_text)` | Gold-outlined [icon] [wordmark] pill |
| `draw_back_cover(c, logo_white_path, year, tagline, website, email)` | Deep-green back with contacts |

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
| `clean_text(text)` | Normalize quotes, strip control chars |
| `discover_assets(extra_dirs)` | Find all ScalePoint brand assets |

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
from pdf2image import convert_from_path
images = convert_from_path('output.pdf', dpi=150)
for i, img in enumerate(images):
    img.save(f'page_{i+1}.png')
```

View EVERY page as PNG. Check against the 29-item anti-pattern checklist
AND the 10-item layout verification checklist in DESIGN-RULES.md.

## Step 7: Deliver

Write to workspace folder. Use a descriptive filename (e.g.,
`ScalePoint_Crown_Holdings_Teaser_2026.pdf`). Present with `computer://` link.
Confirm content integrity: "I preserved all original content without edits."
