---
name: scalepoint-teaser
description: >
  Produces the ScalePoint M&A one-page blind buyer teaser as a branded,
  print-ready PDF (ReportLab). TRIGGER: use this skill any time the user says
  "/teaser", "format a teaser", "write a teaser", "produce a blind teaser",
  "draft a teaser for [business]", or pastes business facts and asks for a
  teaser, blind profile, or pre-NDA marketing one-pager. Do NOT trigger for a
  CIM, information memorandum, or full deal package. Replaces the old
  markdown+HTML teaser output entirely.
---

# ScalePoint One-Page Teaser (v2)

A teaser is a **filter, not a format**. It is ONE page, blind, pre-NDA. Its
job is to make a qualified buyer sign an NDA, not to answer their questions.
Every prior failure of this skill came from formatting whatever content
existed instead of excluding what doesn't belong.

All support files live in this skill's folder (the directory containing this
SKILL.md): `scripts/teaser_layout.py` (layout engine), `assets/` (logo),
`examples/reference_teaser_eros.pdf` (the locked visual reference — open it
before your first build).

## The content firewall (non-negotiable)

**ON the teaser — nothing else:**
| Element | Budget |
|---|---|
| Header band: serif title + region/industry descriptor | title ≤ 60 chars |
| Opening paragraph (what it is, scale, why selling) | ≤ 3 sentences |
| Proof bullets (single line each) | ≤ 7 |
| Hero metric strip | exactly 3 |
| Revenue + EBITDA bar charts with YoY growth % | 3 fiscal years |
| Industry overview line (optional) | ≤ 2 sentences |
| Momentum callout (optional, e.g. "tracking ahead") | 1 line pattern |
| Numbered growth opportunities | ≤ 7 |
| Transaction column: Structure / FYE / Transition / Pricing | 4 rows; Pricing = "Available on NDA" |
| Footnotes + confidentiality line | every derived figure footnoted |
| Footer strip: deal lead contact + "Execute an NDA" CTA | fixed |

**NEVER on a teaser (CIM material — refuse even if the source draft has it):**
financial summary tables · gross margin · EBITDA normalization tables or
add-back detail · indicative pricing, multiples, or valuation math ·
ownership split · ideal buyer profile · project codes ("Project X" appears
nowhere on the document) · CSRS / compilation-standard references · legal
business name.

If the user insists on including CIM material, push back once with the
reason (it leaks negotiating position pre-NDA), then follow their decision
and note the override in your summary.

## Step 1 — Intake

Ask whether you are FORMATTING existing approved content or AUTHORING new
content, then collect (grouped in ONE question if anything is missing):
business description; industry + region; transaction structure and owner
situation; 3 fiscal years of revenue and EBITDA (+ what the EBITDA is: per
compiled/reviewed/audited statements, or management-prepared); any
normalization basis already agreed with the deal lead; proof points
(differentiators, customer base, debt position, team); growth levers;
momentum data (YTD vs prior year); deal lead name/role/phone/email.

When formatting existing content: preserve the deal lead's phrasing wherever
it fits the budgets; cut, don't rewrite.

## Step 2 — Math gate (before any layout)

1. Recompute every percentage from the raw figures.
2. **CAGR vs total growth**: `CAGR = (end/start)^(1/years) - 1` over the
   stated period. If a supplied "CAGR" is actually total growth, do NOT
   silently change the number — relabel it ("Revenue +X% FYaaaa–FYbbbb"),
   compute the true CAGR separately, and FLAG the discrepancy to the user
   for the deal lead's sign-off.
3. Normalized figures: state the basis in a footnote (e.g. "EBITDA per
   compiled financial statements plus a $50,000 annual owner-compensation
   add-back"). If per-year normalized EBITDA is chartable, chart normalized
   per-year values, never a 3-yr-average as if it were a year.
4. If figures are inconsistent (EBITDA > gross profit, revenue mismatch),
   stop and ask.

## Step 3 — Blind gate

Scan every string that will appear on the page and remove/generalize:
- legal/trade name, city (region only: "Western Canada", not "Calgary"),
  street or landmark references
- supplier/brand/bank names ("two leading archery brands", not "Hoyt and
  Mathews"; "long-standing bank relationship", not "TD Bank")
- identifying dollar peaks (convert to units: "~700 orders in 4 days", not
  "$700K–$800K Black Friday")
- project codenames, SP-codes, file metadata

Codename is used ONLY in the output filename and email subject lines, never
in the document body.

## Step 4 — Build

```bash
python3 -c "import reportlab, pypdfium2" 2>/dev/null || python3 -m pip install reportlab pypdfium2 --quiet --break-system-packages
```

```python
import sys, os
skill_dir = os.path.dirname(<path to this SKILL.md>)   # you know this path — you just read the file
sys.path.insert(0, os.path.join(skill_dir, "scripts"))
from teaser_layout import build_teaser, EXAMPLE_DATA   # EXAMPLE_DATA shows the exact dict shape
build_teaser(data, out_path)
```

`build_teaser` enforces the page: it raises on >7 bullets, >7 growth items,
≠3 metrics, multi-line bullets, em dashes, or vertical overflow. When it
raises, CUT CONTENT — never shrink fonts, never spill to page 2.

Style rules already encoded in the engine (don't fight them): white page
with deep-green bookend bands; gold hairline sections; serif display /
sans body; standard ALL-CAPS gold 8pt descriptors; latest fiscal year bar
in gold, priors in deep green; olive EBITDA bars; growth % in olive. NO
rounded cards, NO badges, NO em dashes (en dash for numeric ranges only).

## Step 5 — Visual QA (mandatory)

Render and LOOK at the page before delivering:

```python
import pypdfium2 as pdfium
page = pdfium.PdfDocument(out_path)[0]
page.render(scale=2).to_pil().save("teaser_qa.png")
```

Check: single page; no text collisions or margin overhangs; bullets one
line each; chart value labels don't overlap growth callouts; footnotes
present for every derived figure; blind-gate scan once more on the rendered
text.

## Step 6 — Deliver and sign off

Save as `ScalePoint_[Codename]_Teaser_1pg_[Mon]YYYY.pdf`. Show the PNG and
a short list of: figures used and their sources, anything relabeled or
flagged at the math gate, anything blinded at the blind gate. Then ask for
the deal lead's sign-off. Do not email, upload, or file the teaser anywhere
until the user explicitly approves.

## House rules

- Never invent facts, figures, or highlights; omit what you don't have.
- Real company names in HubSpot/internal records; codename external.
- All dollars CAD unless stated.
- Improvements to this skill are made in the `Scalepointma/claude-skills`
  repo and pushed — never patched into a session-local copy.
