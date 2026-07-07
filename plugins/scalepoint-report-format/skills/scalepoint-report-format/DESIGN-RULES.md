# ScalePoint M&A — Design Rules & Layout Decision Tree

Read this BEFORE writing any PDF generation code. Run the anti-pattern and
verification checklists BEFORE declaring any PDF done.

---

## 1. Page Plan Template

Before coding, produce a page plan for every page:

```
PAGE N — [section label]
  y=736   [section title, 28pt]      -32pt
  y=704   [kicker]                   -14pt
  y=690   [subheading, 22pt]         -36pt
  y=654   [intro paragraph, 3 lines] -55pt
  y=599   [element: card grid, h=260] -272pt
  y=327   [divider]                   -24pt
  y=303   [element: stat row, h=82]  -102pt
  y=201   [footnote, 1 line]         -12pt
  y=189   [remaining space before footer zone: 137pt — OK]
```

Each element's height is listed in BRAND-GUIDE.md §4. Always call
`ensure_space()` before drawing any element near the bottom.

---

## 2. Content → Layout Decision Tree

Map source content to element types using this tree.

**Overview sections / executive summary**
- 3 KPIs → `draw_stat_row()` — e.g., "150+ Companies Advised | 40+ Years | $1M–$25M"
- 3 pillars with short descriptions → `draw_pillar_row()` (brochure) or
  `draw_card_grid(cols=3)` (boardroom)
- 4-6 modules/steps with numbers → `draw_numbered_card()` in 2-col or 3-col grid

**Transaction / deal content**
- List of 4+ closed deals → `draw_deal_tombstone_grid(cols=2)`
- Single hero deal → single `draw_deal_tombstone()` at 2x height
- Deal narrative → body text + optional pull-quote via `draw_light_callout()`

**Financial content**
- Tabular financials → `draw_table()` with total row
- Key metrics above table → `draw_stat_row()` then `draw_table()`
- Multi-year comparison → `draw_table()` with `highlight_rows` for current year

**Process / methodology / phases**
- 3-7 phases → `draw_numbered_card()` grid
- Before/after comparison → 2-col `draw_card_grid(cols=2)` with
  accent-position="left"
- Timeline → `draw_numbered_card()` row (horizontal, cols=n)

**Credentials / about us**
- Team bios → 2-col `draw_card_grid()` with auto_height=True
- Client logo wall → placeholder card grid (future: image wall helper)
- Track record → `draw_deal_tombstone_grid()`

**Hero / cover / brochure pages**
- Boardroom document → `draw_front_cover()` (dark green + stacked logo)
- Brochure / leave-behind → `draw_brochure_hero()` OR `draw_duotone_hero()`
  + `draw_logo_pill()` overlay
- Any content page with a dominant photo → `draw_duotone_hero()` at
  height 200-280pt with pull-quote below

**CTAs / contact**
- End of brochure → `draw_contact_strip(cta_text="START A CONVERSATION")`
- End of report → `draw_back_cover()`

**Supporting / fine print**
- Disclaimers → `draw_footnote()` (NEVER in a callout box)
- Key takeaway / pull-quote / emphasis → `draw_light_callout()` — the
  DEFAULT callout is gold-on-gold (pale gold bg + gold accent + deep-green
  text). `draw_callout_bar()` (dark bar) is RARE, exceptional cases only.
- Hero stat / headline summary → `draw_reverse_tint()` (max 1 per page)

**Contact blocks**
- Deal-lead contact → `info_badge()` — WHITE face + top accent (GOLD on a
  dark page, DEEP_GREEN on a light interior page); name serif, role gold,
  then phone / email / website EACH ON ITS OWN LINE. Same badge on the back
  cover and any Next Steps page. Never cram contact into plain text lines.

**Accent-colour discipline (ALWAYS)**
- Default accent is a single consistent GOLD. Break it up DELIBERATELY and
  EVENLY, never randomly:
  - highlight card grids → `card_grid_rows(row_colors=[GOLD, DEEP_GREEN, OLIVE])`
    (one colour per row)
  - 6-up value grids → `cards_by_column(col_colors=[GOLD, DEEP_GREEN, OLIVE])`
    (one colour per column: 2 gold / 2 green / 2 olive)
  - a second stat row on a page → `draw_stat_row(accent_color=DEEP_GREEN)`
  - numbered rows → gold card accent + deep-green number badge (built into
    `draw_numbered_card`)
- The small descriptor under ANY hero number / stat / value card is always
  THE standard: ALL CAPS, `LABEL_GOLD` #A9803A, 8pt, letter-spaced
  (`draw_descriptor`) — even when the element's accent bar is green or olive.

---

## 3. Document-Type Presets

### Brochure (2-4 pages, leave-behind)
```
Page 1: draw_brochure_hero() OR draw_duotone_hero() + draw_logo_pill()
        draw_pillar_row([Build, Buy, Sell])
        draw_title_group(kicker="ABOUT", subheading="Built for owners who've built something.")
        body paragraph (website "Built for owners" block)
        draw_contact_strip()
Page 2: small hero band + meet-the-team cards (2-col)
        draw_stat_row([150+ ADVISED, 40+ YEARS, $1M–$25M])
        testimonial/pull-quote via draw_light_callout()
        draw_contact_strip()
```

### Teaser (Blind Profile, 1 page)
Teasers have their own dedicated skill (`scalepoint-teaser`) with a locked
one-page layout, content firewall and blind rules — USE THAT SKILL, not this
one, for teasers. If a teaser-style COVER is needed inside another document,
use `draw_teaser_cover()` (three-zone: logo / title group / sepia hero
badges; even vertical rhythm; codename in the kicker line only). The heavy
boardroom `draw_front_cover()` is the wrong cover for anything teaser-like.

### CIM (Confidential Information Memorandum, 20-40 pages)
```
Cover: draw_front_cover() with cover_bg_path=duotone_photo
Page 2: draw_toc()
Sections: Executive summary → Company overview → Market → Operations →
          Financials → Growth → Transaction → Appendices
draw_back_cover()
```

### Valuation Report / Opinion of Value (10-15 pages)
```
Cover: draw_front_cover()
draw_toc()
Multiple sections using stat rows for multiples, tables for comparables,
bullet lists for methodology, reverse_tint for conclusion
draw_back_cover()
```

### Engagement Proposal (3-5 pages)
```
Cover: draw_front_cover()
Sections: Scope → Approach (numbered cards) → Fees (table) →
          Team bios → Next steps + CTA
```

### Deal Tombstone Page / Credentials
```
Section title + intro line + draw_deal_tombstone_grid(deals, cols=2)
```

---

## 4. The Anti-Pattern Checklist

Run before every PDF is considered done. If any item is YES, fix it.

**Layout bugs**
1. Any text overlapping another element
2. Any content below y=52 (footer zone)
3. Section title drawn in the header area
4. Square corners anywhere (must be 10pt radius)
5. More than 1 reverse-tint / dark card on a single page
6. Random multi-colour accent mix (gold/teal/olive scattered per-card).
   Accents are single-GOLD by default; only the deliberate per-row /
   per-column / per-stat-row palettes may break it up.
7. Drop shadow opacity > 0.08 (too heavy)
8. Card without accent bar (flat card = not on-brand)
8b. Large trailing whitespace at the end of a page or document — distribute
    content (break flat prose into cards/personas) so a final page is never
    half empty.

**Typography bugs**
9. Helvetica used for section title / subheading (should be serif bold)
10. Serif used for body at 10pt (readability regression; use Helvetica)
11. Footnote in a box (footnotes must be plain italic text)
12. Body text < 9.5pt outside tables
13. Table body text < 9pt
14. Kicker not uppercase, not letter-spaced
15. Stat number < 30pt
15b. EM DASH anywhere in content (rule 19: rewrite with commas/colons; en
     dash ONLY inside numeric ranges like $1.19M–$1.36M, Net 30–120)
15c. Subhead hierarchy broken: subhead must be 20pt serif — visibly larger
     than hero/caption text, smaller than the 28pt page heading, with real
     space above and below (a 9pt eyebrow is NOT a subhead)
15d. Descriptor under a hero number/stat/value card that is not THE standard
     (ALL CAPS, LABEL_GOLD #A9803A, 8pt, letter-spaced)
15e. Bright yellow GOLD_LIGHT #F6E279 used as a TEXT colour (it exists only
     inside the gold gradient bar)

**Color bugs**
16. Pure black anywhere (body text should be `BODY_COLOR` = DEEP_GREEN)
17. EcoClaim's navy `#002C5E` anywhere (wrong brand)
18. Generic slate/grey anywhere — use `SECONDARY_COLOR` / `LIGHT_TEXT`
19. Green that isn't `DEEP_GREEN` / `OLIVE` in branded contexts

**M&A-specific bugs**
20. Seller / business identifying details on a teaser / blind profile
21. Deal tombstone missing any of: name, sector, value, role, close date
22. "LOI," "CIM," "NDA" expanded unnecessarily (these are recognized terms)
23. Claim of being a "licensed broker" without Alberta license citation
24. Confidentiality footer missing on any CIM / teaser page
25. Revenue / EBITDA figures without corresponding year or period
26. Currency symbols inconsistent (mix of CAD $ and US $)

**Brand bugs**
27. Logo stretched / wrong aspect ratio, or rendered tiny because the PNG's
    dead padding wasn't trimmed (always place logos via `trim_image()` /
    `discover_assets()`, which trims automatically)
28. White logo on cream / pale background (contrast fail) — AND
    `logo-white.png` on ANY colour field (it has an opaque black background
    baked in; use `logo-stacked` on deep green)
29. Photo used full-color instead of duotone (off-brand)
30. Decorative rule/line drawn directly under the ScalePoint logo (the
    lockup already has its wordmark pill)
31. Blank table header cell (every column needs a real header, e.g.
    "Adjustment", "Component" — `draw_table` now raises on this)
32. Contact block with phone + email on one line (each on its OWN line,
    inside the standard `info_badge`)
33. Cover: kicker touching the title, codename as standalone bright text
    (codename lives IN the kicker line), or uneven vertical rhythm between
    logo / title group / hero unit / footer

---

## 5. Layout Verification Checklist

Before declaring done:

1. [ ] Every page has the branded footer (icon + green bar + gold segment)
2. [ ] First page has either front cover OR brochure hero
3. [ ] Last page has back cover OR contact strip CTA
4. [ ] All photos are duotone (not full color)
5. [ ] All card accent bars visible (5pt sliver)
6. [ ] Corner radius is 10pt everywhere (visually check 3 cards)
7. [ ] No content in the footer zone (y < 52)
8. [ ] Gold outline visible on hero panels
9. [ ] Logo used correctly per §8 of BRAND-GUIDE.md
10. [ ] Voice passes: no buzzwords, no jargon, operator register

---

## 6. Widow / Orphan Rules

- No single-line body paragraph at the bottom of a page (orphan) — add
  `ensure_space(c, y, 39)` (three lines) before a paragraph
- No section title alone at the bottom — `ensure_space(c, y, 120)` before
  `draw_title_group()`
- No card with only title at the bottom — `ensure_space(c, y, 120)` before
  any single card
- For grids, `ensure_space(c, y, total_grid_height)` before starting

---

## 7. Content Inventory Step (MANDATORY)

Before choosing ANY layouts:

1. List every source section with heading, approximate word count, content
   type (text / bullet / table / metrics / phases / etc.)
2. Flag missing / suspect content — ask the user, don't invent
3. Map each section to an element type using the decision tree above
4. Estimate page count from heights
5. Run `clean_text()` on all extracted text before rendering

This prevents: content omission, wrong layout, mid-build rework.
