---
name: scalepoint-intake
description: >
  Guides ScalePoint M&A staff through filling out a structured buyer or seller intake form,
  then writes all collected data directly into HubSpot. TRIGGER on any of these phrases or
  situations: "intake", "buyer intake", "seller intake", "fill out the form", "add a buyer",
  "add a seller", "new buyer", "new seller", "new client intake", "buyer profile", "seller profile",
  "log a new buyer", "log a new seller", "register a buyer", "register a seller",
  "create a buyer record", "create a seller record", "onboard a buyer", "onboard a seller",
  "fill in the buyer form", "fill in the seller form", "capture buy box", "record buy box",
  "update buy box", "new lead intake", "prospect intake", "record this seller",
  "write up a buyer", "write up a seller", or whenever a staff member says they have a new
  buyer or seller to capture. Works for both live conversation (staff answering on behalf of
  the contact) and self-serve (staff entering info they already have). Internal use only.
---

# ScalePoint Intake Skill

Guides Alina, Sam, or Gurpreet through collecting a complete buyer or seller profile in a
structured, grouped conversation, then writes all data directly into HubSpot.

This skill is self-contained — all field definitions, enum values, and HubSpot write
instructions are included here. No need to consult another document.

---

## Step 1 — Determine intake type

If the user's message already makes it clear (e.g. "add a buyer", "seller intake"), proceed
directly. Otherwise ask:

> "Is this a **buyer** intake (someone looking to acquire a business) or a **seller** intake
> (a business owner looking to sell)?"

Accept: "buyer", "seller", "b", "s", or clear context clues.

---

## Step 2 — Collect data in grouped asks (BUYER)

Ask the four groups below, one group at a time. Present all fields in a group together as a
single message so the user can answer in one go. Do not ask one field per message.

### BUYER Group 1 — Identity

> Please share the following:
>
> 1. **Contact name** (first and last)
> 2. **Contact email**
> 3. **Contact phone** (optional)
> 4. **Company / firm name** — if they represent no company, use "Individual — [First Last]"
> 5. **Company website / domain** (optional)
> 6. **Firm type** — choose one:
>    - PE Fund
>    - Family Office
>    - Independent Sponsor
>    - Search Fund
>    - Holdco
>    - Strategic Acquirer
>    - Searcher – ETA
>    - Owner-Operator
>    - Searcher – Broker (individual searching through a broker channel)
> 7. **Buyer type** — choose one:
>    - Individual (self-funded individual buyer)
>    - PE-Financial (fund, LP capital, hold period)
>    - Strategic-Synergetic (existing operating company adding a bolt-on)
> 8. **How did they come to us?** (direct inbound, referral intro, trade show, LinkedIn,
>    podcast, website, cold outreach, other — if referral, who referred them?)

### BUYER Group 2 — Buy box

> Now the buy box:
>
> 1. **Target industries** — plain English, comma-separated
>    (e.g. "automotive services, HVAC, plumbing")
> 2. **Target geographies** — provinces or regions
>    (e.g. "Alberta, BC" or "Western Canada")
> 3. **Deal size range** — minimum and maximum deal value in CAD
>    (e.g. "$500K to $3M" — enter 0 for no minimum if truly open)
> 4. **Minimum EBITDA** they'll consider (CAD, or "none" if not a constraint)
> 5. **Minimum revenue** they'll consider (CAD, or "none")

### BUYER Group 3 — Tags and narrative

> A few more items:
>
> 1. **Sector tags** — pick all that apply from this list (just list the ones that fit):
>
>    *Sector:* auto-services, hvac, plumbing, electrical, landscaping, cleaning-commercial,
>    cleaning-residential, childcare, dental-medical, veterinary, pharmacy, fitness,
>    food-beverage, grocery-specialty, retail-general, ecommerce, manufacturing, distribution,
>    technology-saas, professional-services, marketing-agency, property-management, staffing,
>    funeral, jewelry-watch, pet-services
>
>    *Geography:* alberta, bc, ontario, quebec, prairie-provinces, western-canada, national
>
>    *Deal size:* sub-1m, 1m-3m, 3m-7m, 7m-15m, 15m-plus
>
>    *Buyer type:* searcher-eta, owner-operator, search-fund, pe-fund, family-office,
>    independent-sponsor, holdco, strategic-acquirer
>
>    *Other:* franchise-experience, absentee-ok, semi-absentee-ok, turnaround-ok,
>    real-estate-included, real-estate-preferred, vendor-financing-required, urgent-timeline
>
> 2. **Buyer narrative** — a short paragraph (3–6 sentences) describing who they are, what
>    they're looking for, and why. This goes into HubSpot as-is and may be used for matching.
>    If they have a pitch deck or one-pager, ask them to share the key points verbally and
>    write it up yourself.

### BUYER Group 4 — Anything else

> Last check:
>
> 1. **Urgency / timeline** — are they actively looking to close within a certain window?
> 2. **Anything they will NOT buy** — deal-breakers (geography, industry, business model,
>    owner-operator dependency, etc.)
> 3. **Other notes** — anything that doesn't fit the fields above but is useful for matching
>    (e.g. "has LOI experience", "prefers businesses with real estate", "wants a warm intro
>    to seller before NDA")

---

## Step 3 — Collect data in grouped asks (SELLER)

### SELLER Group 1 — Identity and business overview

> Please share the following:
>
> 1. **Seller's name** (first and last)
> 2. **Seller's email**
> 3. **Seller's phone** (optional)
> 4. **Business name** — if the seller doesn't want the name disclosed yet, use a short
>    blind description (e.g. "Southern Alberta HVAC company")
> 5. **Industry / what the business does** (plain English, 1–2 sentences)
> 6. **City and province** where the business operates
> 7. **Years in operation**
> 8. **Number of employees** (full-time + part-time, approximate is fine)

### SELLER Group 2 — Business details and financials

> Now the financials:
>
> 1. **Most recent full fiscal year revenue** (CAD)
> 2. **Most recent EBITDA** (CAD — owner earnings / SDE if they call it that is fine)
> 3. **Fiscal year end** (month name, e.g. "December", "March")
> 4. **Asking price** — if the seller has one in mind (or "open to valuation")
> 5. **Transaction structure preference** — Share sale, Asset sale, or Either/don't know
> 6. **Target close timeline** — when do they want to be done? (e.g. "this year", "12–18 months",
>    "flexible")

### SELLER Group 3 — Narrative and motivation

> A few more items:
>
> 1. **Business description** — 2–4 sentences suitable for a confidential information
>    memorandum teaser. What does the business do, who does it serve, what makes it work?
> 2. **Investment highlights** — key strengths (recurring revenue, strong team, niche market,
>    proprietary process, etc.). Bullet points are fine.
> 3. **Growth opportunities** — what could a buyer do to grow the business?
> 4. **Reason for selling** — retirement, burnout, health, partnership disagreement,
>    relocation, new opportunity, other
> 5. **Engagement letter status** — has the seller signed an Engagement Letter (EL) with
>    ScalePoint yet? (yes / no / not yet discussed)

### SELLER Group 4 — Classification and notes

> Last section:
>
> 1. **Seller Sub-ICP** — which of these best describes the seller? (If unsure, skip and
>    describe their situation — we'll derive it.)
>    - A — Valuation-Curious (just exploring, not committed to selling)
>    - B — Pre-Seller (plans to sell in 1–3 years, doing homework now)
>    - C — Committed Main Street Seller (wants out this year, business runs on them)
>    - D — Sophisticated FSBO (decided seller $2–10M, clean books, was trying FSBO)
>    - E — Time-Pressured Seller (life event driving timeline, speed > price)
>    - F — Franchise Resale (selling a franchise unit, franchisor approval required)
>    - G — Broker-Represented (already has a broker, co-brokerage scenario)
> 2. **Codename** — if a wine codename has already been assigned for this seller, enter it.
>    If not yet assigned, leave blank (we'll assign one before any external communication).
> 3. **How did they come to us?** (referral, LinkedIn, podcast, website, cold outreach, other)
> 4. **Any other notes** — confidentiality concerns, seller's emotional state, key staff
>    dependencies, anything that shapes how we handle the engagement

---

## Step 4 — Show summary for review

Before writing anything to HubSpot, present a clean summary of all collected data.
Wait for explicit confirmation ("looks good", "correct", "go ahead") before proceeding.
Accept corrections inline — if the user says "change the EBITDA to $280K", update the
summary and confirm the change before writing.

### BUYER summary format

```
BUYER INTAKE SUMMARY — [Contact Name]

CONTACT
  Name:              [firstname] [lastname]
  Email:             [email]
  Phone:             [phone or —]
  Buyer type:        [Individual / PE-Financial / Strategic-Synergetic]
  How they found us: [source]

COMPANY
  Name:              [company name]
  Firm type:         [firm_type]
  Website:           [domain or —]

BUY BOX
  Industries:        [buy_box_industry]
  Geography:         [buy_box_geography]
  Deal size:         $[min] – $[max]
  Min EBITDA:        $[value or —]
  Min revenue:       $[value or —]

TAGS
  [comma-separated list of all selected tags]

NARRATIVE
  [buyer_narrative paragraph]

TIMELINE / NOTES
  [urgency, deal-breakers, other notes]
```

Flag anything blank or uncertain with a note like `⚠ Not provided`.

### SELLER summary format

```
SELLER INTAKE SUMMARY — [Business Name or Blind Description]

CONTACT (SELLER)
  Name:           [firstname] [lastname]
  Email:          [email]
  Phone:          [phone or —]
  How found us:   [source]

BUSINESS
  Name:           [business name]
  Industry:       [industry]
  Location:       [city], [province]
  Years operating:[years_in_operation]
  Employees:      [num_employees]
  EL signed:      [yes / no / TBD]
  Codename:       [codename or — not yet assigned]

FINANCIALS
  Revenue (last FY): $[revenue_last_fy]  (FY ends: [month])
  EBITDA (last FY):  $[ebitda_last_fy]
  Asking price:      $[asking_price or open]
  Transaction type:  [Share / Asset / Either]
  Timeline:          [seller_timeline]

CLASSIFICATION
  Sub-ICP:        [letter — name]
  Reason for sale:[seller_motivation]

NARRATIVE
  Description: [business_description]
  Highlights:  [investment_highlights]
  Growth opps: [growth_opportunities]

NOTES
  [other notes]
```

Flag anything blank or uncertain with `⚠ Not provided`.

---

## Step 5 — Write to HubSpot

After confirmation, use HubSpot MCP tools to create or update records in this order.
Search before creating to avoid duplicates.

### BUYER — HubSpot write sequence

**1. Find or create Company**

Search `companies` by `name`. If found and it looks like the same entity, update it.
If not found, create with:

| HubSpot field | Value |
|---|---|
| `name` | Company name (or "Individual — [First Last]") |
| `sp_company_type` | `buyer_lead` |
| `firm_type` | One of: `PE_Fund`, `Family_Office`, `Independent_Sponsor`, `Search_Fund`, `Holdco`, `Strategic_Acquirer`, `Searcher_ETA`, `Owner_Operator`, `Searcher_Broker` |
| `domain` | Website domain if provided |

**2. Find or create Contact**

Search `contacts` by email. If found, update. If not found, create with:

| HubSpot field | Value |
|---|---|
| `firstname` | First name |
| `lastname` | Last name |
| `email` | Email |
| `phone` | Phone |
| `contact_relationship` | Source (e.g. `direct_inbound`, `referral_intro`, `trade_show`, `linkedin`, `podcast`, `website`) |
| `buyer_type` | `Individual`, `PE-Financial`, or `Strategic-Synergetic` |
| `buy_box_industry` | Plain-English industry string |
| `buy_box_geography` | Provinces/regions string |
| `buy_box_deal_size_min` | Integer (CAD) |
| `buy_box_deal_size_max` | Integer (CAD) |
| `buy_box_ebitda_min` | Integer (CAD) or blank |
| `buy_box_revenue_min` | Integer (CAD) or blank |
| `buyer_narrative` | Full narrative paragraph |

**3. Associate Contact to Company**

Use `batch-create-associations` or the association endpoint to link the Contact to the Company.

**4. Add a note to the Contact**

Create a note (engagement type: `NOTE`) on the Contact record with:
- All selected tags formatted as a comma-separated list under the heading "Buy Box Tags:"
- Deal-breakers and any other notes from Group 4
- Attribution: "Intake logged by [staff name if known, otherwise ScalePoint intake skill] on [today's date]"

---

### SELLER — HubSpot write sequence

**1. Find or create Company**

Search `companies` by business name. If found, update. If not found, create with:

| HubSpot field | Value |
|---|---|
| `name` | Business name (or blind description) |
| `sp_company_type` | `active_client` if EL signed, `prospect` if not |
| `sp_sell_side_status` | `active_client` if EL signed, `prospect` if not |
| `industry` | Plain-English industry |

**2. Find or create Contact**

Search `contacts` by email. If found, update. If not found, create with:

| HubSpot field | Value |
|---|---|
| `firstname` | First name |
| `lastname` | Last name |
| `email` | Email |
| `phone` | Phone |
| `contact_relationship` | `seller_client` |
| `seller_sub_icp` | One of: `Valuation-Curious`, `Pre-Seller`, `Committed Main Street Seller`, `Sophisticated FSBO`, `Time-Pressured Seller`, `Franchise Resale`, `Broker-Represented` (or blank if not determined) |

**3. Associate Contact to Company**

Link the Contact to the Company record.

**4. Create a Deal in the Listing pipeline**

Create a new Deal with:

| HubSpot field | Value |
|---|---|
| `dealname` | Business name (or blind description) — same as company name |
| `pipeline` | Seller Listing pipeline (use the appropriate pipeline ID — search `deal_pipelines` if unsure) |
| `dealstage` | "Prospect" stage (first stage of the Listing pipeline) |
| `asking_price` | Integer (CAD) or blank |
| `revenue_last_fy` | Integer (CAD) |
| `ebitda_last_fy` | Integer (CAD) |
| `fiscal_year_end` | Month name |
| `business_description` | 2–4 sentence description |
| `years_in_operation` | Integer |
| `num_employees` | Integer |
| `location_city` | City |
| `location_province` | Province |
| `transaction_structure` | `share_sale`, `asset_sale`, or `either` |
| `seller_timeline` | Free text |
| `seller_motivation` | Reason for selling |
| `seller_subicp` | Same value as on Contact |
| `codename` | Wine codename if assigned, otherwise blank |

**5. Associate Contact and Company to Deal**

Link both the Contact and the Company to the new Deal.

**6. Add a note to the Deal**

Create a NOTE engagement on the Deal with:
- Investment highlights (bullet points)
- Growth opportunities (bullet points)
- Any other notes from Group 4
- Attribution: "Intake logged by [staff name if known] on [today's date]"

---

## Step 6 — Confirm and report

After all writes complete, report back with:

```
HubSpot records created/updated:

Company:  [name]              → https://app.hubspot.com/contacts/[portal-id]/company/[id]
Contact:  [firstname lastname] → https://app.hubspot.com/contacts/[portal-id]/contact/[id]
[Deal:    [dealname]          → https://app.hubspot.com/contacts/[portal-id]/deal/[id]]  ← seller only

All fields written. Review links above to verify.
```

If any field failed to write (e.g. invalid enum value, property not found), flag it clearly
and suggest the manual fix.

---

## Rules and constraints

1. **Real names in HubSpot always.** Codenames are for external emails only. HubSpot records
   always use the real business name. See: Codename usage rule.

2. **Never send email from this skill.** This skill writes to HubSpot only. If a follow-up
   email is needed, draft it and wait for explicit approval before sending. Zero autonomous
   outbound to clients or prospects.

3. **Never delete companies.** If you find a duplicate or a mismatched company, flag it for
   manual review. Do not delete.

4. **Company is the primary object.** Contacts must be associated to a Company — never
   create a Contact floating without a Company link. If the buyer has no firm, create a
   company named "Individual — [First Last]".

5. **Search before creating.** Always search by email (for contacts) and by name (for
   companies) before creating new records. Duplicates are harder to clean up than they are
   to prevent.

6. **Sub-ICP for sellers.** If the seller Sub-ICP is unclear from the intake, leave it blank.
   Do not guess. Flag it in the note so Sam or Alina can set it after the first real
   conversation. A wrong Sub-ICP misleads the Match Matrix.

7. **Blank fields stay blank.** Never populate a field with invented, inferred, or
   placeholder data. If the user didn't provide it, leave it empty. Flag it in the summary.

8. **Today's date in notes.** Every note written to HubSpot must include the date it was
   logged (use the current date from context).

9. **BCC logging.** If this skill causes any email to be drafted (e.g. a welcome email),
   BCC `342889181@bcc.na3.hubspot.com` on it.

10. **Seller privacy.** If the seller asked for confidentiality, note it explicitly in the
    Deal note. Do not put the seller's personal details (home address, health information)
    in any field that appears on a Deal or listing document.

---

## Quick-reference: field enums

### `firm_type` (Company — buyer)
`PE_Fund` · `Family_Office` · `Independent_Sponsor` · `Search_Fund` · `Holdco` ·
`Strategic_Acquirer` · `Searcher_ETA` · `Owner_Operator` · `Searcher_Broker`

### `buyer_type` (Contact — buyer)
`Individual` · `PE-Financial` · `Strategic-Synergetic`

### `sp_company_type` (Company)
`buyer_lead` · `active_client` · `prospect` · (others exist — do not overwrite unless directed)

### `contact_relationship` (Contact — common values)
`direct_inbound` · `referral_intro` · `trade_show` · `linkedin` · `podcast` · `website` ·
`cold_outreach` · `seller_client`

### `seller_sub_icp` (Contact — seller)
`Valuation-Curious` · `Pre-Seller` · `Committed Main Street Seller` ·
`Sophisticated FSBO` · `Time-Pressured Seller` · `Franchise Resale` · `Broker-Represented`

### `transaction_structure` (Deal — seller)
`share_sale` · `asset_sale` · `either`

### 46-tag vocabulary (go into Contact note for buyers)
**Sector:** auto-services · hvac · plumbing · electrical · landscaping · cleaning-commercial ·
cleaning-residential · childcare · dental-medical · veterinary · pharmacy · fitness ·
food-beverage · grocery-specialty · retail-general · ecommerce · manufacturing · distribution ·
technology-saas · professional-services · marketing-agency · property-management · staffing ·
funeral · jewelry-watch · pet-services

**Geography:** alberta · bc · ontario · quebec · prairie-provinces · western-canada · national

**Deal size:** sub-1m · 1m-3m · 3m-7m · 7m-15m · 15m-plus

**Buyer type:** searcher-eta · owner-operator · search-fund · pe-fund · family-office ·
independent-sponsor · holdco · strategic-acquirer

**Other:** franchise-experience · absentee-ok · semi-absentee-ok · turnaround-ok ·
real-estate-included · real-estate-preferred · vendor-financing-required · urgent-timeline
