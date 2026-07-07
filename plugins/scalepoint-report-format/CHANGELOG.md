# scalepoint-report-format changelog

## 2.1.0 (2026-07-06) — design rules 1–24 baked in
Implements the full Project Eros design-rule memo (rules 1–24) in code + docs:

- **Accent discipline (r3, r13, r20)**: single-GOLD default (rotation retired);
  deliberate palettes via new `card_grid_rows` (per-row), `cards_by_column`
  (per-column), `cards_colored`, `draw_stat_row(accent_color=)`.
- **Standard descriptor (r22)**: `draw_descriptor` — ALL CAPS #A9803A 8pt
  letter-spaced, used by stat boxes / kv cards / hero badges everywhere.
- **Logo handling (r1, r4, r5)**: `trim_image` + `image_ratio` auto-trim dead
  padding (stacked logo was rendering ~3x too small); no rules under logos;
  logo-white flagged unusable on colour fields; back cover uses stacked logo.
- **Covers (r6, r10, r11, r12)**: front cover stray gold bar removed, big logo,
  wrapped titles, subtitle GOLD not GOLD_LIGHT; NEW `draw_teaser_cover`
  (three-zone, sepia `hero_badge`s, codename in kicker, pinned footer).
- **Contact blocks (r14, r16, r21, r24)**: NEW `info_badge` — white face,
  gold accent on dark / deep-green on light, each contact line its own row;
  back cover tagline 21pt gold italic (r15).
- **Numbered cards (r7, r13)**: deep-green number badge on gold card, numeral
  centered, single-line rows vertically centered.
- **Type (r2, r8)**: Libre Baskerville TTFs bundled (assets/fonts, OFL) and
  registered at import with Times fallback; subhead standard 20pt; GOLD_LIGHT
  removed as a text colour everywhere.
- **Dashes (r19)**: `clean_text` rewrites em dashes to commas, keeps en dash
  only inside numeric ranges; `assert_no_em_dash` hard gate.
- **Tables (r23)**: `draw_table` raises on blank column headers.
- **Callouts (r9)**: gold-on-gold `draw_light_callout` documented as default;
  dark bar marked rare.
- **Portability**: `discover_assets` reads the skill's own assets/ folder
  (relative), auto-trims; all /sessions/ and machine paths removed.
- Docs: BRAND-GUIDE + DESIGN-RULES updated (anti-pattern items 6, 8b, 15b–e,
  27–33); `examples/build_reference_report.py` + `reference_report.pdf` are
  the regenerate-and-compare visual target.

## 2.0.0 (2026-07-06)
- Converted from agents/ to skills/ format; portable relative paths; pypdfium2
  replaces pdf2image/poppler.
