---
name: teaser-formatter
description: >
  Formats a blind buyer teaser in the ScalePoint M&A house style (SP-XX-YY format),
  producing both a plain markdown version and a fully branded self-contained HTML document.
  TRIGGER: use this skill any time the user says "/teaser", "format a teaser", "write a teaser",
  "produce a blind teaser", "draft a teaser for [business]", or pastes a set of business facts
  and asks for a teaser or marketing document.
  Do NOT trigger for CIM, information memorandum, or full deal packages — this is for the
  1-page blind teaser only.
---

# ScalePoint Teaser Formatter Skill (Enhanced — Markdown + Branded HTML)

Produces a 1-page confidential blind teaser in the ScalePoint M&A house style, ready to send
to prospective buyers before NDA. Outputs both a plain markdown version and a fully branded,
self-contained HTML document using the ScalePoint visual system.

> **Pre-flight requirement — normalization must happen BEFORE this skill runs.**
> This skill does NOT normalize financials. It formats what it is given.
> EBITDA adjustments for owner compensation, one-time expenses, related-party rent,
> personal vehicle charges, or any other add-backs must be calculated and agreed upon
> with the seller's accountant BEFORE running this skill. The teaser will state
> "no normalization" in the source footnote unless you explicitly pass normalized figures
> and instruct the skill to label them as adjusted.

---

## Step 1 — Collect required inputs

Check the user's message for the following. If any required field is missing, ask for it
in a single grouped question — do not ask one at a time.

### Required
| Field | Notes |
|---|---|
| Business description | 2–4 sentences: what the business does, how it operates, key differentiators |
| Industry | Plain English (e.g. "automotive aftermarket — quick-lube", "residential HVAC", "commercial cleaning") |
| Location | City, Province |
| Format / facility | Physical description: sq ft, bays, lots, units, whatever is relevant |
| Business structure | Franchise, independent, chain unit, etc. |
| Transaction structure | Share sale, asset sale, or both available; owner situation (retiring, exiting, relocating…) |
| Financials — 3 fiscal years | For each year: fiscal year label, revenue, gross profit, EBITDA. See Step 2 for EBITDA calculation rules. |
| Fiscal year end month | e.g. "December YE", "February YE" |

### Strongly recommended (include if available)
| Field | Notes |
|---|---|
| Trailing period data | Period label, net sales, invoice count, average ticket, new customers |
| Investment highlights | Bullet list — 5–8 points; provide raw points and the skill will polish phrasing |
| Growth opportunities | Bullet list — 3–6 points |
| Brand / franchise name | Use if public knowledge or if the seller permits disclosure at teaser stage; otherwise omit |
| Asking price | Usually withheld at teaser stage — only include if seller explicitly wants it visible pre-NDA |

### Optional / conditional
| Field | Notes |
|---|---|
| Pending financials note | e.g. "FY2025 financials expected Q3 2026" — include only if relevant |
| Special deal terms | Assumable lease, CEBA retirement, vendor financing available, etc. |

---

## Step 2 — Verify and calculate EBITDA

**Formula (no normalization):**

```
EBITDA = Net Income + Interest Expense + Income Tax + Depreciation & Amortization
```

If the user provides the four components, calculate EBITDA and show the build clearly.
If the user provides a pre-calculated EBITDA figure, use it as given and note the source
(e.g. "as per compilation financials").

**Margin calculation:**
```
EBITDA Margin % = EBITDA / Revenue × 100
Gross Margin %  = Gross Profit / Revenue × 100
```

Round all margins to one decimal place.

**EBITDA footnote wording:**
- If figures come from CSRS 4200 compilation statements: `EBITDA = net income + interest + taxes + D&A, no normalization.`
- If figures come from review engagement: `EBITDA = net income + interest + taxes + D&A, no normalization. Source: CSRS 4400 review engagement.`
- If figures come from audited statements: `EBITDA = net income + interest + taxes + D&A, no normalization. Source: audited financial statements.`
- If figures come from management accounts or owner-provided: `EBITDA = net income + interest + taxes + D&A, no normalization. Source: management-prepared financial statements — unverified.`

**Do not proceed to formatting if EBITDA figures seem mathematically inconsistent**
(e.g. EBITDA > Gross Profit without explanation). Flag the discrepancy and ask the user
to confirm or correct before continuing.

---

## Step 3 — Generate the project reference code

Format: `SP-[INDUSTRY CODE]-[2-DIGIT YEAR]`

**Industry code table (2 letters):**

| Industry | Code |
|---|---|
| Automotive aftermarket (lube, tires, mechanical) | QL |
| HVAC (heating, cooling, ventilation) | HV |
| Plumbing | PL |
| Electrical | EL |
| General construction / renovation | GC |
| Landscaping / lawn care | LS |
| Commercial cleaning / janitorial | CC |
| Residential cleaning | RC |
| Childcare / daycare | CD |
| Dental / medical practice | DM |
| Veterinary | VT |
| Pharmacy | PH |
| Fitness / gym / studio | FT |
| Food & beverage (restaurant, café, QSR) | FB |
| Grocery / specialty food retail | GR |
| Retail (general) | RT |
| E-commerce / online retail | EC |
| Manufacturing | MF |
| Distribution / logistics | DL |
| Technology / SaaS | TK |
| Professional services (accounting, law, consulting) | PS |
| Marketing / agency | MK |
| Property management / real estate services | PM |
| Staffing / recruitment | SR |
| Funeral / death care | FC |
| Jewelry / watch retail | JW |
| Pet services | PT |
| Other / unlisted | XX |

Year = last 2 digits of the current calendar year (e.g. 2026 → 26).

If a project reference already exists in the user's input, use it as provided — do not generate a new one.

If the same industry code has already been used this session (user is producing multiple teasers),
ask: "This would also generate SP-[CODE]-[YY] — do you want to differentiate with a suffix like SP-[CODE]-[YY]-B, or do you have an existing project number?"

---

## Step 4 — Format the teaser (plain markdown)

Produce the teaser as a markdown document using the exact section order and heading style below.
Do not add sections, reorder sections, or introduce sub-headings that don't appear in the template.

---

### Teaser output template

```
CONFIDENTIAL BUYER TEASER
[Business type / descriptor — do NOT use legal name if blind]
[Location descriptor] · [City, Province]
Project Reference: [SP-CODE]  Prepared [Month YYYY]

Industry: [Industry description]
Location: [City, Province]
Format: [Facility description]
[Brand line — omit entirely if not disclosing brand]
Transaction: [Structure description] — [owner situation]; [deal positioning phrase]

BUSINESS OVERVIEW
[2–4 sentence paragraph. Write in third person. No first-person. Do not name the business.
Cover: what it does, how long established, operating model, trade area, why it is attractive.
Match the register of the QuickLube example — factual, concise, no hype words like "amazing"
or "incredible".]

FINANCIAL HIGHLIGHTS (CAD)
Fiscal Year ([Month] YE)   [FY Label 1]    [FY Label 2]    [FY Label 3]
Revenue                    $[#]            $[#]            $[#]
Gross Profit               $[#]            $[#]            $[#]
Gross Margin               [#.#]%          [#.#]%          [#.#]%
EBITDA                     $[#]            $[#]            $[#]
EBITDA Margin              [#.#]%          [#.#]%          [#.#]%

Source: [Source footnote per Step 2 rules]. [Any special terms, e.g. "Premises lease at preferred rate, assumable."]
[IF_PENDING_FINANCIALS: [FYxxxx] financials expected [timeframe]; teaser will be updated on receipt.]

TRAILING PERFORMANCE — [PERIOD LABEL] ([DURATION] POS DATA)
$[NET SALES] NET SALES | [INVOICE COUNT] INVOICES | $[AVG TICKET] AVG TICKET | [NEW CUSTOMERS] NEW CUSTOMERS
[One sentence: what this implies for annualized run-rate, if supportable.]
[Omit this section entirely if no trailing data is available.]

INVESTMENT HIGHLIGHTS
- [Highlight 1 — lead with the strongest financial proof point, format: what + number + significance]
- [Highlight 2]
- [Highlight 3]
- [Highlight 4]
- [Highlight 5]
- [Highlight 6 — optional]
- [Highlight 7 — optional]
- [Highlight 8 — optional]

GROWTH OPPORTUNITIES
- [Opportunity 1]
- [Opportunity 2]
- [Opportunity 3]
- [Opportunity 4 — optional]
- [Opportunity 5 — optional]

TRANSACTION PROCESS
Structure: [Share sale / Asset sale / Share or asset sale — negotiable]
Process: Confidential off-market; CIM and data room released post-NDA
Timeline: Targeting close in [year]
Asking Price: Available to qualified buyers post-NDA

ScalePoint M&A — Confidential Advisor
To request additional information, please contact your ScalePoint representative to execute an NDA.
scalepointma.com
```

---

## Step 5 — Investment highlights phrasing guide

Apply these phrasing patterns when polishing raw bullet points.
Do not invent facts — only reframe what the user provides.

| Raw input | SP-style phrasing |
|---|---|
| "makes good money" | "Proven cash flow — $[EBITDA] EBITDA on $[Revenue] revenue (~[X]% margin) in most recent fiscal year" |
| "revenue is going up" | "Accelerating growth — revenue +[X]% over [N] years; FY[YY] +[X]% YoY" |
| "lots of new customers" | "Strong customer acquisition — [N] new customers in trailing [period]" |
| "does different things" | "Diversified service mix — [service 1], [service 2], [service 3]" |
| "known brand" | "Recognized brand — turn-key [franchise/chain] with marketing & supplier programs" |
| "nice building" | "Modern facility — [description]" |
| "no debt" | "Clean balance sheet — [specific debt retired or absent]; positive retained earnings" |
| "can run without owner" | "Optional owner-operator — trained team supports absentee or semi-absentee structure" |
| "platform opportunity" | "Platform for [industry] expansion — [specific opportunity description]" |

---

## Step 6 — Output and review (markdown)

1. Output the full teaser as a clean markdown code block (so it can be pasted directly into Word or email).
2. Below the teaser, show a brief **Formatting notes** section that lists:
   - Project reference generated (or confirmed)
   - EBITDA source and footnote wording used
   - Any fields that were left blank or omitted and why
   - Any flags (e.g. "Gross margin declined year-over-year — buyer will notice; consider whether to address in business overview")
3. Proceed immediately to Step 7 to produce the branded HTML version.
4. After both outputs are shown, ask: "Does this look right? Any figures or wording to adjust before this goes out?"

Do not send, email, or store the teaser until the user explicitly confirms it.

---

## Step 7 — Produce the branded HTML document

After the plain markdown output, produce a fully branded, self-contained HTML teaser using
the ScalePoint visual system. Output it as a single fenced ```html code block so the user
can save it directly as a .html file and open it in any browser.

The HTML must be completely self-contained: all CSS is inlined in the `<head>`, no external
stylesheets, no external images. The only external dependency permitted is the Google Fonts
import for Libre Baskerville (single `<link>` tag).

### 7.1 — Complete HTML template

Use the following template structure, substituting all `[PLACEHOLDER]` values with the
collected data. Do not output placeholder text — if a field was omitted (e.g. trailing
performance, brand line, asking price), omit the corresponding HTML block entirely.

````html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>[BUSINESS DESCRIPTOR] — Confidential Buyer Teaser | ScalePoint M&A</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Libre+Baskerville:ital,wght@0,400;0,700;1,400&display=swap" rel="stylesheet">
<style>
  :root {
    --sp-green: #0A2D2A;
    --sp-green-dark: #061C1A;
    --sp-green-mid: #1A4540;
    --sp-gold: #CB9D43;
    --sp-gold-deep: #D7A848;
    --sp-gold-light: #F6E279;
    --sp-olive: #869846;
    --sp-teal: #18766A;
    --sp-cream: #FAF8F2;
    --sp-near-white: #F7F5EF;
    --sp-paper: #ffffff;
    --sp-body: #0A2D2A;
    --sp-secondary: #4A5B58;
    --sp-light: #8A9995;
    --sp-rule: #D8D2C5;
    --sp-warn: #B65B3A;
    --sp-gold-soft: #E8D08A;
    --sp-ink: #0A2D2A;
    --sp-grey: #4A5B58;
  }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    font-family: Helvetica, Arial, sans-serif;
    color: var(--sp-body);
    background: var(--sp-cream);
    line-height: 1.55;
    font-size: 14px;
  }
  .page {
    max-width: 900px;
    margin: 0 auto;
    background: var(--sp-paper);
    box-shadow: 0 2px 24px rgba(0,0,0,0.10);
  }

  /* ── COVER ── */
  .cover {
    background: #0A2D2A;
    padding: 56px 56px 0;
    position: relative;
    overflow: hidden;
  }
  .cover::before {
    content: "";
    position: absolute;
    top: -100px; right: -100px;
    width: 400px; height: 400px;
    background: radial-gradient(circle, rgba(203,157,67,0.18) 0%, transparent 65%);
    border-radius: 50%;
  }
  .cover::after {
    content: "";
    position: absolute;
    bottom: -150px; left: -50px;
    width: 350px; height: 350px;
    background: radial-gradient(circle, rgba(203,157,67,0.10) 0%, transparent 65%);
    border-radius: 50%;
  }
  .cover-inner {
    position: relative;
    z-index: 1;
    padding-bottom: 72px;
  }
  .cover .wordmark {
    font-family: "Libre Baskerville", "Times New Roman", Times, serif;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: var(--sp-gold);
    margin-bottom: 40px;
    display: block;
  }
  .cover .eyebrow {
    letter-spacing: 0.24em;
    text-transform: uppercase;
    font-size: 11px;
    color: var(--sp-gold);
    font-weight: 700;
    margin-bottom: 18px;
  }
  .cover h1 {
    font-family: "Libre Baskerville", "Times New Roman", Times, serif;
    font-size: 46px;
    line-height: 1.08;
    margin: 0 0 22px;
    color: var(--sp-paper);
    font-weight: 700;
    letter-spacing: -0.5px;
  }
  .cover .subtitle {
    font-family: "Libre Baskerville", "Times New Roman", Times, serif;
    font-style: italic;
    font-size: 18px;
    color: var(--sp-gold-soft);
    margin-bottom: 30px;
    max-width: 700px;
    line-height: 1.5;
  }
  .cover .meta {
    font-size: 11px;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--sp-gold);
    font-weight: 700;
  }
  .cover-wave {
    display: block;
    width: 100%;
    height: 48px;
    margin-bottom: -1px;
  }

  /* ── CONTENT ── */
  .content {
    padding: 50px 56px 70px;
  }

  h2 {
    font-family: "Libre Baskerville", "Times New Roman", Times, serif;
    font-size: 28px;
    color: var(--sp-green);
    margin: 52px 0 4px;
    font-weight: 700;
    line-height: 1.1;
  }
  .section-bar {
    height: 5px;
    background: linear-gradient(90deg, #F6E279 0%, #CB9D43 25%, #D7A848 50%, #CB9D43 75%, #F6E279 100%);
    border-radius: 2px;
    margin: 8px 0 26px;
    width: 100%;
  }
  h3 {
    font-family: "Libre Baskerville", "Times New Roman", Times, serif;
    font-size: 20px;
    color: var(--sp-green);
    margin: 36px 0 10px;
    font-weight: 700;
  }
  p {
    margin: 0 0 14px;
    font-size: 14px;
    line-height: 1.65;
  }

  /* ── FINANCIAL TABLE ── */
  table {
    width: 100%;
    border-collapse: collapse;
    margin: 16px 0 22px;
    font-size: 13px;
  }
  th, td {
    text-align: left;
    padding: 10px 14px;
    vertical-align: top;
    border-bottom: 1px solid var(--sp-rule);
  }
  th {
    background: var(--sp-green);
    color: var(--sp-paper);
    font-weight: 600;
    letter-spacing: 0.04em;
    font-size: 11px;
    text-transform: uppercase;
  }
  tr:nth-child(even) td {
    background: var(--sp-near-white);
  }
  td:first-child {
    font-weight: 600;
    color: var(--sp-green-dark);
    white-space: nowrap;
  }
  td.num {
    text-align: right;
    font-variant-numeric: tabular-nums;
    font-family: Helvetica, Arial, sans-serif;
    font-size: 13px;
  }
  .footnote {
    font-size: 11px;
    color: var(--sp-secondary);
    font-style: italic;
    margin-top: 6px;
    line-height: 1.5;
  }

  /* ── STAT BOXES (trailing performance) ── */
  .stat-row {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
    gap: 16px;
    margin: 20px 0 28px;
  }
  .stat-box {
    background: var(--sp-paper);
    border: 1px solid var(--sp-rule);
    border-top: 4px solid var(--sp-gold);
    padding: 18px 16px 16px;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.06);
  }
  .stat-box .stat-val {
    font-family: "Libre Baskerville", "Times New Roman", Times, serif;
    font-size: 24px;
    font-weight: 700;
    color: var(--sp-green);
    margin-bottom: 4px;
    line-height: 1.1;
  }
  .stat-box .stat-label {
    font-size: 10px;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--sp-gold);
    font-weight: 700;
  }

  /* ── PULLQUOTE (investment highlights bullet block) ── */
  .pullquote {
    border-left: 5px solid var(--sp-gold);
    padding: 18px 24px;
    margin: 20px 0 8px;
    background: var(--sp-near-white);
    border-radius: 10px;
  }
  .pullquote ul {
    list-style: none;
    padding: 0;
    margin: 0;
  }
  .pullquote ul li {
    font-family: "Libre Baskerville", "Times New Roman", Times, serif;
    font-size: 14px;
    color: var(--sp-green-dark);
    line-height: 1.65;
    padding: 6px 0 6px 20px;
    position: relative;
    border-bottom: 1px solid var(--sp-rule);
  }
  .pullquote ul li:last-child {
    border-bottom: none;
  }
  .pullquote ul li::before {
    content: "›";
    position: absolute;
    left: 0;
    color: var(--sp-gold);
    font-weight: 700;
    font-size: 16px;
    line-height: 1.5;
  }

  /* ── GROWTH OPPORTUNITIES (plain bullets) ── */
  .bullet-list {
    list-style: none;
    padding: 0;
    margin: 0 0 20px;
  }
  .bullet-list li {
    font-size: 14px;
    color: var(--sp-body);
    line-height: 1.65;
    padding: 5px 0 5px 20px;
    position: relative;
  }
  .bullet-list li::before {
    content: "—";
    position: absolute;
    left: 0;
    color: var(--sp-gold);
    font-weight: 700;
  }

  /* ── TRANSACTION TABLE ── */
  .tx-table {
    width: 100%;
    border-collapse: collapse;
    margin: 16px 0 22px;
    font-size: 13px;
  }
  .tx-table td {
    padding: 10px 14px;
    border-bottom: 1px solid var(--sp-rule);
    vertical-align: top;
  }
  .tx-table td:first-child {
    width: 180px;
    font-size: 10px;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--sp-gold);
    font-weight: 700;
    background: var(--sp-green);
    color: var(--sp-gold);
    white-space: nowrap;
  }
  .tx-table td:last-child {
    color: var(--sp-body);
    font-size: 13px;
  }
  .tx-table tr:nth-child(even) td:last-child {
    background: var(--sp-near-white);
  }

  /* ── DOCUMENT FOOTER ── */
  .doc-footer {
    background: var(--sp-green);
    padding: 28px 56px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 12px;
  }
  .doc-footer .footer-brand {
    font-family: "Libre Baskerville", "Times New Roman", Times, serif;
    font-size: 14px;
    font-weight: 700;
    color: var(--sp-gold);
    letter-spacing: 0.04em;
  }
  .doc-footer .footer-url {
    font-size: 11px;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--sp-gold-soft);
  }
  .doc-footer .footer-cta {
    font-size: 12px;
    color: var(--sp-gold-soft);
    font-style: italic;
    font-family: "Libre Baskerville", "Times New Roman", Times, serif;
    max-width: 360px;
    text-align: right;
    line-height: 1.5;
  }

  /* ── CONFIDENTIALITY STRIP ── */
  .confid-strip {
    background: var(--sp-green-dark);
    padding: 10px 56px;
    font-size: 10px;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: var(--sp-light);
    text-align: center;
  }

  @media print {
    .page { box-shadow: none; max-width: 100%; }
    .cover { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
    .doc-footer { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
    .confid-strip { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
    th { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
    .tx-table td:first-child { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
  }
</style>
</head>
<body>
<div class="page">

  <!-- CONFIDENTIALITY STRIP (top) -->
  <div class="confid-strip">
    This document is confidential and intended solely for the named recipient. Do not distribute.
  </div>

  <!-- COVER -->
  <div class="cover">
    <div class="cover-inner">
      <span class="wordmark">ScalePoint M&amp;A</span>
      <div class="eyebrow">Confidential Buyer Teaser &middot; [PROJECT REF]</div>
      <h1>[BUSINESS DESCRIPTOR]</h1>
      <div class="subtitle">[CITY, PROVINCE] &middot; [INDUSTRY]</div>
      <div class="meta">Prepared [Month YYYY] &middot; ScalePoint M&amp;A</div>
    </div>
    <!-- Wave transition from dark green to white -->
    <svg class="cover-wave" viewBox="0 0 900 48" preserveAspectRatio="none" xmlns="http://www.w3.org/2000/svg">
      <path d="M0,48 L0,24 Q225,0 450,24 Q675,48 900,24 L900,48 Z" fill="#ffffff"/>
    </svg>
  </div>

  <!-- MAIN CONTENT -->
  <div class="content">

    <!-- BUSINESS OVERVIEW -->
    <h2>Business Overview</h2>
    <div class="section-bar"></div>
    <p>[BUSINESS OVERVIEW PARAGRAPH]</p>

    <!-- FINANCIAL HIGHLIGHTS -->
    <h2>Financial Highlights <span style="font-family:Helvetica,Arial,sans-serif;font-size:13px;font-weight:400;color:var(--sp-secondary);letter-spacing:0;">(CAD)</span></h2>
    <div class="section-bar"></div>
    <table>
      <thead>
        <tr>
          <th>Fiscal Year ([MONTH] YE)</th>
          <th class="num">[FY LABEL 1]</th>
          <th class="num">[FY LABEL 2]</th>
          <th class="num">[FY LABEL 3]</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>Revenue</td>
          <td class="num">$[#]</td>
          <td class="num">$[#]</td>
          <td class="num">$[#]</td>
        </tr>
        <tr>
          <td>Gross Profit</td>
          <td class="num">$[#]</td>
          <td class="num">$[#]</td>
          <td class="num">$[#]</td>
        </tr>
        <tr>
          <td>Gross Margin</td>
          <td class="num">[#.#]%</td>
          <td class="num">[#.#]%</td>
          <td class="num">[#.#]%</td>
        </tr>
        <tr>
          <td>EBITDA</td>
          <td class="num">$[#]</td>
          <td class="num">$[#]</td>
          <td class="num">$[#]</td>
        </tr>
        <tr>
          <td>EBITDA Margin</td>
          <td class="num">[#.#]%</td>
          <td class="num">[#.#]%</td>
          <td class="num">[#.#]%</td>
        </tr>
      </tbody>
    </table>
    <p class="footnote">[SOURCE FOOTNOTE]. [SPECIAL TERMS IF ANY]</p>
    <!-- IF_PENDING_FINANCIALS: add a second footnote line here -->

    <!-- TRAILING PERFORMANCE — omit this entire block if no trailing data -->
    <h3>Trailing Performance &mdash; [PERIOD LABEL]</h3>
    <div class="stat-row">
      <div class="stat-box">
        <div class="stat-val">$[NET SALES]</div>
        <div class="stat-label">Net Sales</div>
      </div>
      <div class="stat-box">
        <div class="stat-val">[INVOICE COUNT]</div>
        <div class="stat-label">Invoices</div>
      </div>
      <div class="stat-box">
        <div class="stat-val">$[AVG TICKET]</div>
        <div class="stat-label">Avg Ticket</div>
      </div>
      <div class="stat-box">
        <div class="stat-val">[NEW CUSTOMERS]</div>
        <div class="stat-label">New Customers</div>
      </div>
    </div>
    <p>[RUN-RATE IMPLICATION SENTENCE IF SUPPORTABLE]</p>

    <!-- INVESTMENT HIGHLIGHTS -->
    <h2>Investment Highlights</h2>
    <div class="section-bar"></div>
    <div class="pullquote">
      <ul>
        <li>[HIGHLIGHT 1]</li>
        <li>[HIGHLIGHT 2]</li>
        <li>[HIGHLIGHT 3]</li>
        <li>[HIGHLIGHT 4]</li>
        <li>[HIGHLIGHT 5]</li>
        <!-- Add or remove <li> items as needed -->
      </ul>
    </div>

    <!-- GROWTH OPPORTUNITIES -->
    <h2>Growth Opportunities</h2>
    <div class="section-bar"></div>
    <ul class="bullet-list">
      <li>[OPPORTUNITY 1]</li>
      <li>[OPPORTUNITY 2]</li>
      <li>[OPPORTUNITY 3]</li>
      <!-- Add or remove <li> items as needed -->
    </ul>

    <!-- TRANSACTION PROCESS -->
    <h2>Transaction Process</h2>
    <div class="section-bar"></div>
    <table class="tx-table">
      <tbody>
        <tr>
          <td>Structure</td>
          <td>[SHARE SALE / ASSET SALE / NEGOTIABLE]</td>
        </tr>
        <tr>
          <td>Process</td>
          <td>Confidential off-market; CIM and data room released post-NDA</td>
        </tr>
        <tr>
          <td>Timeline</td>
          <td>Targeting close in [YEAR]</td>
        </tr>
        <tr>
          <td>Asking Price</td>
          <td>Available to qualified buyers post-NDA</td>
        </tr>
      </tbody>
    </table>

  </div><!-- /content -->

  <!-- DOCUMENT FOOTER -->
  <div class="doc-footer">
    <div>
      <div class="footer-brand">ScalePoint M&amp;A &mdash; Confidential Advisor</div>
      <div class="footer-url">scalepointma.com</div>
    </div>
    <div class="footer-cta">
      To request additional information, please contact your<br>ScalePoint representative to execute an NDA.
    </div>
  </div>

  <!-- CONFIDENTIALITY STRIP (bottom) -->
  <div class="confid-strip">
    This document is confidential and intended solely for the named recipient. Do not distribute.
  </div>

</div><!-- /page -->
</body>
</html>
````

### 7.2 — HTML substitution rules

When generating the HTML, apply these rules precisely:

**Dollar formatting in the financial table:**
- Format all dollar figures with a `$` prefix and comma thousands separator: `$1,240,000`
- Do not abbreviate to "M" or "K" in the table — use full numbers
- Margins are shown as `XX.X%` with one decimal place

**Trailing performance stat boxes:**
- Format net sales as `$X.XXM` or `$XXX,XXX` (use M abbreviation only if ≥ $1M and it reads cleaner)
- Format avg ticket as `$XXX`
- Format invoice count and new customers as plain integers with commas if ≥ 1,000
- If trailing performance data is absent, remove the entire `<h3>Trailing Performance...` block through the closing `</p>` of the run-rate sentence

**Project ref in eyebrow:**
- Use the SP code generated in Step 3, e.g. `CONFIDENTIAL BUYER TEASER · SP-QL-26`

**Brand / franchise line:**
- If brand is not being disclosed, the subtitle on the cover shows only `[CITY, PROVINCE] · [INDUSTRY]`
- If brand is being disclosed, append to the cover subtitle: `[CITY, PROVINCE] · [INDUSTRY] · [BRAND NAME]`

**Asking price row:**
- If the seller has explicitly provided and approved showing the asking price pre-NDA,
  replace "Available to qualified buyers post-NDA" with the actual figure and any terms

**Special deal terms:**
- Append to the source footnote `<p class="footnote">` in the financial section
- If there is a pending-financials note, add a second `<p class="footnote">` immediately after

**Investment highlights list:**
- Remove any `<li>` placeholder lines that were not filled with real content
- The pullquote block must have at least 3 `<li>` items; if only 3 highlights were provided,
  remove the remaining placeholder items

**HTML entities:**
- Use `&mdash;` for em-dashes, `&middot;` for centre dots, `&amp;` for ampersands in the cover/footer copy
- Dollar signs in the HTML body do NOT need escaping

---

## Step 8 — Final output sequence

Present outputs in this order:

1. `**Plain Markdown Version**` heading, then the markdown teaser in a fenced ` ```markdown ` block
2. `**Formatting Notes**` section (project ref, EBITDA footnote, omissions, flags)
3. `**Branded HTML Version**` heading with instruction: *"Save as `[SP-CODE]-teaser.html` and open in any browser. No internet connection required except for the Libre Baskerville font."*
4. The complete fenced ` ```html ` block containing the finished HTML document
5. `**Review prompt**`: "Does this look right? Any figures or wording to adjust before this goes out?"

---

## Rules

- Never use the seller's legal business name in the teaser unless the user explicitly says "not blind" or "use real name."
- Use real company names in HubSpot and all internal records. Codenames are for external (buyer-facing) documents only.
- Do not normalize EBITDA. Format only. If the user asks about normalization, explain it must be done separately with the seller's accountant before running this skill.
- Do not invent financial figures, growth rates, or highlights. If the user has not provided a data point, leave the field blank or omit the block — do not extrapolate.
- Do not include the asking price unless the user explicitly provides it and confirms it should appear pre-NDA.
- All dollar figures in CAD unless otherwise stated.
- The trailing performance section must be omitted entirely (not shown as blank or with placeholder text) if no trailing data is provided.
- The brand line in the cover subtitle must be omitted if brand is not being disclosed at teaser stage.
- The HTML output must be self-contained. Do not reference any external CSS files, image files, or scripts. The Google Fonts `<link>` tag is the only permitted external reference.
- Do not send, email, or store either output until the user explicitly confirms the content.
