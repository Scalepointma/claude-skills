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

> **Schema source of truth:** Appendix A of `Chevron-Customer-Journey.md` (SharePoint/repo)
> is the schema source of truth for every HubSpot property name and enum value in this skill.
> If a write fails on a property name or value, check Appendix A — do not improvise a field name.

---

## Step 0 — Is a HubSpot record warranted at all?

**No HubSpot record is created until an engagement is signed, or the deal lead explicitly
says otherwise.** Pre-engagement research, prospect lists, and "maybe" contacts stay in
Excel/SharePoint. If the staff member is capturing pre-engagement research, offer to
structure it for the Excel tracker instead and stop here. Only proceed when the contact is a
signed engagement, or the deal lead (Jodi, or whoever she designates for this deal) has
explicitly said this person belongs in HubSpot.

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
>    - Individual Buyer (self-funded individual buyer)
>    - PE-Financial Buyer (fund, LP capital, hold period)
>    - Strategic-Synergetic Buyer (existing operating company adding a bolt-on)
> 8. **Buyer status** — are they actively pursuing acquisitions right now (**active buyer**)
>    or interested but not actively in the market (**potential buyer**)?
> 9. **How did they come to us?** (direct inbound, referral intro, trade show, LinkedIn,
>    podcast, website, cold outreach, other — if referral, who referred them?)

### BUYER Group 2 — Buy box

> Now the buy box:
>
> 1. **Target industries** — plain English, comma-separated
>    (e.g. "automotive services, restaurants, plumbing"). I'll map these to the canonical
>    industry slugs and confirm the mapping with you.
> 2. **Industries they will NOT touch** — same format (exclusion filter; "none" is fine)
> 3. **Target geographies** — provinces or regions they WANT
>    (e.g. "Alberta, BC" or "Western Canada")
> 4. **Geographies they will NOT consider** ("none" is fine)
> 5. **Revenue range** — minimum and maximum annual revenue they'll consider (CAD; either
>    end can be open)
> 6. **EBITDA range** — minimum and maximum EBITDA they'll consider (CAD; either end can
>    be open)

**Industry slug mapping (mandatory).** The industries live in two multi-select properties —
`buy_box_industries_targeted` and `buy_box_industries_avoided` — whose internal values are
the canonical 85-slug vocabulary (see quick-reference at the bottom of this skill). Map the
user's plain-English words to the closest slug(s) and echo the mapping back for confirmation
(e.g. "automotive services" → `automotive`; "HVAC" → closest fits are `construction`,
`repair-maintenance`, `electrical` — confirm which). **NEVER invent a slug.** The slug
vocabulary must match BASAB's URLs exactly (lockstep rule: a slug exists in BASAB URL
routing, the canonical slug file, and the HubSpot enums simultaneously, or not at all) —
an invented slug silently breaks Layer 1 matching and is very hard to diagnose later. If no
slug fits, pick the nearest real slug(s), confirm with the user, and put the exact
plain-English wording in the intake Note.

### BUYER Group 3 — Tags and narrative

> A few more items:
>
> 1. **Buyer tags** — pick all that apply from the 46-tag vocabulary (see quick-reference
>    at the bottom of this skill; categories: operational style, workforce, customer profile,
>    deal structure, real estate, brand/regulation, geography, buyer style, timeline, asset
>    intensity). Industry and geography are deliberately NOT tags — they live in the buy box
>    fields above. Only use tags from the list; the vocabulary is governed and each tag maps
>    to seller sub-ICPs.
>
> 2. **Buyer narrative** — a short paragraph (3–6 sentences) describing who they are, what
>    they're looking for, and why. This is Layer 3 matching material. It goes into the
>    intake Note engagement and into `buy_box_description`. If they have a pitch deck or
>    one-pager, ask them to share the key points verbally and write it up yourself.

### BUYER Group 4 — Anything else

> Last check:
>
> 1. **Urgency / timeline** — are they actively looking to close within a certain window?
> 2. **Anything they will NOT buy** — deal-breakers beyond the industry/geography exclusions
>    already captured (business model, owner-operator dependency, etc.)
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
> 5. **Industry / what the business does** (plain English, 1–2 sentences — I'll map to the
>    canonical industry slugs and confirm)
> 6. **City and province** where the business operates
> 7. **Years in operation**
> 8. **Number of employees** (full-time + part-time, approximate is fine)

### SELLER Group 2 — Business details and financials

> Now the financials:
>
> 1. **Most recent full fiscal year revenue** (CAD)
> 2. **Most recent EBITDA** (CAD — if the seller quotes owner earnings / SDE, say so; see
>    the EBITDA rule below)
> 3. **Fiscal year end** (month name, e.g. "December", "March")
> 4. **Asking price** — a single number or a range, if the seller has one in mind
>    (or "open to valuation")
> 5. **Transaction structure preference** — Share sale, Asset sale, or Either/don't know
> 6. **Target close timeline** — when do they want to be done? (e.g. "this year", "12–18 months",
>    "flexible")

**EBITDA vs SDE.** If the seller frames the number as "what I take home", "before my
salary", or owner earnings, that is SDE — record it in the Note with the qualifier, and only
write it to the EBITDA field if it genuinely is EBITDA.

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
> 3. **Blind listing?** — will the public listing hide the business identity (blind title,
>    province only)? If yes, what is the blind title?
> 4. **How did they come to us?** (referral, LinkedIn, podcast, website, cold outreach, other)
> 5. **Any other notes** — confidentiality concerns, seller's emotional state, key staff
>    dependencies, anything that shapes how we handle the engagement

---

## Step 4 — Show summary for review

Before writing anything to HubSpot, present a clean summary of all collected data.
Accept corrections inline — if the user says "change the EBITDA to $280K", update the
summary and confirm the change before moving on.

### BUYER summary format

```
BUYER INTAKE SUMMARY — [Contact Name]

CONTACT
  Name:              [firstname] [lastname]
  Email:             [email]
  Phone:             [phone or —]
  Buyer type:        [Individual Buyer / PE-Financial Buyer / Strategic-Synergetic Buyer]
  Relationship:      [potential_buyer / active_buyer]
  How they found us: [source]

COMPANY
  Name:              [company name]
  Firm type:         [firm_type]
  Website:           [domain or —]

BUY BOX
  Industries targeted: [slugs, confirmed mapping]
  Industries avoided:  [slugs or —]
  Geography yes:       [provinces/regions]
  Geography no:        [provinces/regions or —]
  Revenue range:       $[buy_box_revenue_min] – $[buy_box_revenue_max]
  EBITDA range:        $[buy_box_ebitda_min] – $[buy_box_ebitda_max]

TAGS (buyer_tags)
  [comma-separated list of selected tags from the 46-tag vocabulary]

NARRATIVE (→ Note + buy_box_description)
  [narrative paragraph]

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
  Industry:       [slug(s), confirmed mapping — plus plain English]
  Location:       [city], [province]
  Years operating:[years in operation]
  Employees:      [employee count]
  EL signed:      [yes / no / TBD]
  Codename:       [codename or — not yet assigned]
  Blind listing:  [yes + blind title / no]

FINANCIALS
  Revenue (last FY): $[listing_revenue]  (FY ends: [month])
  EBITDA (last FY):  $[listing_ebitda]  [qualifier if SDE/owner earnings]
  Asking price:      $[listing_ask_low] – $[listing_ask_high] (or open)
  Transaction type:  [Share / Asset / Either]
  Timeline:          [sale_timeline]

CLASSIFICATION
  Sub-ICP:        [letter — name]
  Reason for sale:[reason_for_sale]

NARRATIVE
  Description: [business description]
  Highlights:  [investment highlights]
  Growth opps: [growth opportunities]

NOTES
  [other notes]
```

Flag anything blank or uncertain with `⚠ Not provided`.

---

## Step 5 — RECORD APPROVAL GATE (mandatory — do not skip)

Nothing is written to HubSpot until this gate passes. The gate has two parts:

1. **Show the specific records.** After the summary is corrected, state exactly which
   HubSpot records will be created or updated (Company X, Contact Y, Deal Z — create vs
   update, with the key property values).

2. **Get explicit load approval from Jodi (or the deal lead she designates for this deal).**
   Approval means words to the effect of **"load these"** / "write them to HubSpot" /
   "approved, create the records" — from Jodi or the designated deal lead specifically.
   A staff member confirming "the summary looks right" is **NOT** approval to write.
   Accuracy confirmation and load approval are two different things.

If the approver asks for changes, apply them, re-present the record list, and pass the gate
again. If approval is not given, stop — offer to save the structured intake as a draft note
in chat or to the Excel/SharePoint tracker instead.

---

## Step 6 — Write to HubSpot

After the gate passes, use HubSpot MCP tools to create or update records in this order.
Search before creating to avoid duplicates.

**Enum discipline:** every enumeration property accepts only its internal enum values. For
any enum not fully listed in this skill (`buy_box_geography_yes`, `buy_box_geography_no`,
`deal_structures_seller_will_accept`, `reason_for_sale`, `sale_timeline`, `source_funnel_buyer`,
`source_funnel_seller`), fetch the live options with `hubspot-get-property` before writing.

### BUYER — HubSpot write sequence

**1. Find or create Company**

Search `companies` by `name`. If found and it looks like the same entity, update it.
If not found, create with:

| HubSpot field | Value |
|---|---|
| `name` | Company name (or "Individual — [First Last]") |
| `sp_company_type` | `buyer` (multi-select — append, never overwrite existing values) |
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
| `contact_relationship` | `potential_buyer` or `active_buyer` (multi-select — append, never overwrite; see canonical values in quick-reference) |
| `buyer_type` | Internal value: `individual_buyer`, `pe_financial_buyer`, or `strategic_synergetic_buyer` |
| `buy_box_industries_targeted` | Multi-select of canonical slugs (confirmed mapping only — never invented) |
| `buy_box_industries_avoided` | Multi-select of canonical slugs (or leave blank) |
| `buy_box_geography_yes` | Multi-select — fetch live options first |
| `buy_box_geography_no` | Multi-select — fetch live options first (or leave blank) |
| `buy_box_revenue_min` | Integer (CAD) or blank |
| `buy_box_revenue_max` | Integer (CAD) or blank |
| `buy_box_ebitda_min` | Integer (CAD) or blank |
| `buy_box_ebitda_max` | Integer (CAD) or blank |
| `buyer_tags` | Multi-select of selected tags from the 46-tag vocabulary |
| `buy_box_description` | The buyer narrative paragraph (Layer 3 free text) |

**3. Associate Contact to Company**

Use `batch-create-associations` or the association endpoint to link the Contact to the Company.

**4. Add a note to the Contact**

Create a note (engagement type: `NOTE`) on the Contact record with:
- The full buyer narrative paragraph (verbatim)
- The plain-English industry/geography wording as given, alongside the confirmed slug mapping
- Deal-breakers, urgency/timeline, and any other notes from Group 4
- How they came to us (source), including referrer name if applicable
- Attribution: "Intake logged by [staff name if known, otherwise ScalePoint intake skill] on [today's date]"

---

### SELLER — HubSpot write sequence

**1. Find or create Company**

Search `companies` by business name. If found, update. If not found, create with:

| HubSpot field | Value |
|---|---|
| `name` | Business name (or blind description) |
| `sp_sell_side_status` | `active_client` if EL signed, `prospect` if not |

Do **not** set `sp_company_type` for a pure sell-side company — sell-side status lives
exclusively in `sp_sell_side_status`; `sp_company_type` is for buy-side/network relationship
types (`buyer`, `referrer`, `vendor`, `bd_partner`, `consulting_client`,
`third_party_contact`, `unverified`). Put the plain-English industry description in the
intake Note (the canonical industry slugs go on the Deal's `listing_industry`).

**2. Find or create Contact**

Search `contacts` by email. If found, update. If not found, create with:

| HubSpot field | Value |
|---|---|
| `firstname` | First name |
| `lastname` | Last name |
| `email` | Email |
| `phone` | Phone |
| `contact_relationship` | `active_seller` (multi-select — append, never overwrite) |
| `seller_sub_icp` | One of: `Valuation-Curious`, `Pre-Seller`, `Committed Main Street Seller`, `Sophisticated FSBO`, `Time-Pressured Seller`, `Franchise Resale`, `Broker-Represented` (or blank if not determined) |
| `reason_for_sale` | Enum — fetch live options first; leave blank if unclear |
| `sale_timeline` | Enum — fetch live options first; leave blank if unclear |
| `deal_structures_seller_will_accept` | Enum — fetch live options first (share/asset/either preference) |
| `seller_free_text_notes` | Key observations that don't fit structured fields |

**3. Associate Contact to Company**

Link the Contact to the Company record.

**4. Create a Deal in the LISTING pipeline**

Seller listings are Deals in the **Listing pipeline** (stages include Prospect → EL Signed →
Listing Draft → Approved + Published → Active → Under LOI → Closing → Closed-Won). Look up
the actual pipeline and stage IDs at runtime via the HubSpot schema/property tools — do not
hardcode IDs. (Buyer–listing pairs live in the separate Inquiry pipeline; that is NOT what
this skill creates.)

Create a new Deal with:

| HubSpot field | Value |
|---|---|
| `dealname` | Business name (or blind description) — same as company name |
| `pipeline` | Listing pipeline ID (looked up at runtime) |
| `dealstage` | "Prospect" stage ID (first stage of the Listing pipeline, looked up at runtime) |
| `listing_industry` | Multi-select of canonical slugs (confirmed mapping only — never invented) |
| `listing_location` | City |
| `listing_province` | Province |
| `listing_revenue` | Integer (CAD) |
| `listing_ebitda` | Integer (CAD) — only if the number truly is EBITDA; SDE/owner earnings stays in the Note with its qualifier |
| `listing_ask_low` | Integer (CAD) — lower end of asking range (or the single asking price) |
| `listing_ask_high` | Integer (CAD) — upper end (same as low if a single number; blank if open to valuation) |
| `listing_codename` | Wine codename if assigned, otherwise blank |
| `is_blind_listing_deal` | Set if the listing is blind |
| `blind_title_listing_deal` | The blind title, if blind |
| `description` | 2–4 sentence business description |

Fiscal year end, years in operation, and employee count have no Deal property — they go in
the Deal note (step 6 below).

**5. Associate Contact and Company to Deal**

Link both the Contact and the Company to the new Deal.

**6. Add a note to the Deal**

Create a NOTE engagement on the Deal with:
- Investment highlights (bullet points)
- Growth opportunities (bullet points)
- Fiscal year end, years in operation, employee count
- EBITDA qualifier if the number given was SDE/owner earnings
- How they came to us (source), including referrer name if applicable
- Any other notes from Group 4
- Attribution: "Intake logged by [staff name if known] on [today's date]"

---

## Step 7 — Confirm and report

After all writes complete, report back with:

```
HubSpot records created/updated:

Company:  [name]              → https://app.hubspot.com/contacts/[portal-id]/company/[id]
Contact:  [firstname lastname] → https://app.hubspot.com/contacts/[portal-id]/contact/[id]
[Deal:    [dealname]          → https://app.hubspot.com/contacts/[portal-id]/deal/[id]]  ← seller only
```

If any field failed to write (e.g. invalid enum value, property not found), flag it clearly
and suggest the manual fix.

---

## Rules and constraints

1. **No HubSpot record until an engagement is signed** — or the deal lead explicitly says
   otherwise. Pre-engagement research stays in Excel/SharePoint. (Step 0.)

2. **RECORD APPROVAL GATE is mandatory.** The specific records must be shown and explicitly
   approved ("load these") by Jodi or the deal lead she designates before any write. Staff
   confirmation of the summary is not sufficient. (Step 5.)

3. **Real names in HubSpot always.** Codenames are for external emails only. HubSpot records
   always use the real business name. See: Codename usage rule.

4. **Never invent an industry slug.** The 85-slug vocabulary is maintained in lockstep with
   BASAB's URL routing and the HubSpot enums — a value outside the vocabulary silently breaks
   Layer 1 matching. Map plain English to existing slugs and confirm with the user.

5. **Never send email from this skill.** This skill writes to HubSpot only. If a follow-up
   email is needed, draft it and wait for explicit approval before sending. Zero autonomous
   outbound to clients or prospects.

6. **Never delete companies.** If you find a duplicate or a mismatched company, flag it for
   manual review. Do not delete.

7. **Company is the primary object.** Contacts must be associated to a Company — never
   create a Contact floating without a Company link. If the buyer has no firm, create a
   company named "Individual — [First Last]".

8. **Search before creating.** Always search by email (for contacts) and by name (for
   companies) before creating new records. Duplicates are harder to clean up than they are
   to prevent.

9. **Multi-selects append.** `sp_company_type`, `contact_relationship`, `buyer_tags`, and
   the buy-box multi-selects are multi-value — when updating an existing record, add to the
   existing values; never blow away what's already there.

10. **Sub-ICP for sellers.** If the seller Sub-ICP is unclear from the intake, leave it blank.
    Do not guess. Flag it in the note so Sam or Alina can set it after the first real
    conversation. A wrong Sub-ICP misleads the Match Matrix.

11. **Blank fields stay blank.** Never populate a field with invented, inferred, or
    placeholder data. If the user didn't provide it, leave it empty. Flag it in the summary.

12. **Today's date in notes.** Every note written to HubSpot must include the date it was
    logged (use the current date from context).

13. **BCC logging.** If this skill causes any email to be drafted (e.g. a welcome email),
    BCC `342889181@bcc.na3.hubspot.com` on it.

14. **Seller privacy.** If the seller asked for confidentiality, note it explicitly in the
    Deal note. Do not put the seller's personal details (home address, health information)
    in any field that appears on a Deal or listing document.

---

## Quick-reference: field enums

Verified against the live HubSpot property dumps (account 342889181). Appendix A of
`Chevron-Customer-Journey.md` is the schema source of truth.

### `firm_type` (Company — buyer)
`PE_Fund` · `Family_Office` · `Independent_Sponsor` · `Search_Fund` · `Holdco` ·
`Strategic_Acquirer` · `Searcher_ETA` · `Owner_Operator` · `Searcher_Broker`

### `buyer_type` (Contact — buyer; internal values)
`individual_buyer` · `pe_financial_buyer` · `strategic_synergetic_buyer`

### `sp_company_type` (Company — multi-select, 7 canonical values)
`buyer` · `referrer` · `vendor` · `bd_partner` · `consulting_client` ·
`third_party_contact` · `unverified`

### `sp_sell_side_status` (Company — single-select)
`active_client` · `prospect` · `past_client`

### `contact_relationship` (Contact — multi-select, 12 canonical values)
`internal_team` · `active_seller` · `active_buyer` · `potential_buyer` · `direct_referrer` ·
`chain_referrer` · `professional_network` · `service_provider_deal` ·
`service_provider_scalepoint` · `consulting_client` · `bd_partner` · `capital_active`

### `seller_sub_icp` (Contact — seller)
`Valuation-Curious` · `Pre-Seller` · `Committed Main Street Seller` ·
`Sophisticated FSBO` · `Time-Pressured Seller` · `Franchise Resale` · `Broker-Represented`

### `buyer_tags` (Contact — multi-select; 46-tag vocabulary, matches the live enum exactly)

**Operational style:** `absentee-friendly` · `semi-absentee` · `owner-operator-required` ·
`multi-location-management` · `single-location-focus`

**Workforce:** `union-shop-OK` · `non-union-only` · `key-employee-retention-critical` ·
`low-headcount-comfort` · `high-headcount-experience`

**Customer profile:** `low-concentration-required` · `concentration-tolerant` ·
`contract-revenue-preferred` · `transactional-revenue-OK`

**Deal structure:** `asset-deal-preferred` · `share-deal-OK` · `earn-out-friendly` ·
`earn-out-averse` · `VTB-friendly` · `VTB-required` · `VTB-averse`

**Real estate:** `real-estate-included-required` · `real-estate-included-bonus` ·
`real-estate-excluded-preferred` · `real-estate-lease-OK`

**Brand / regulation:** `franchise-experience` · `franchise-averse` · `licensed-industry-OK` ·
`compliance-heavy-OK` · `compliance-light-only`

**Geography:** `relocation-willing` · `relocation-not-willing` · `specific-province-only` ·
`remote-management-OK`

**Buyer style:** `first-time-buyer` · `repeat-buyer` · `holdco-style` · `portfolio-builder` ·
`single-acquisition`

**Timeline:** `ready-to-close-fast` · `patient-buyer` · `specific-deadline-driven`

**Asset intensity:** `equipment-heavy-OK` · `equipment-light-preferred` · `inventory-heavy-OK` ·
`recurring-revenue-required`

Industry and geography are intentionally NOT in this vocabulary — they live in
`buy_box_industries_targeted` / `buy_box_industries_avoided` / `listing_industry` and
`buy_box_geography_yes` / `buy_box_geography_no`.

### The 85 canonical industry slugs
(`buy_box_industries_targeted` · `buy_box_industries_avoided` on Contact;
`listing_industry` on Deal — identical option lists, mirroring BASAB URLs exactly)

```
accounting-bookkeeping        aesthetics-and-beauty          agriculture
animals-pets                  app-development                aquaculture
architecture-and-design       arts-entertainment             automotive
aviation-and-aerospace        banquet-convention-facilities  brewery
cleaning-services             computers-electronics          construction
consulting                    consumer-services              content-creation
convenience-variety-store     cybersecurity                  data-analytics-management
distribution                  ecommerce                      education
electrical                    environmental-services         event-management
fashion-apparel               finance                        floral-horticulture
food-and-beverage             government                     grocery-supermarket
healthcare                    health-fitness                 health-wellness
hobby-and-craft-artisanal     homecare-services              hospitality
human-resources-employment-services                          information-technology
insurance-and-risk-management interior-design-decor          jewellery
landscaping-gardening         laundry-and-dry-cleaning       legal
logistics                     machinery                      management
manufacturing                 marketing-advertising          media
medical                       mining                         not-for-profit
outsourcing                   pharmaceutical-biotechnology   photography
property-management           public-relations               publishing
real-estate                   renewable-energy-and-clean-tech
rental-leasing                repair-maintenance             restaurant
retail                        robotics                       shipping-courier
social-dating                 software-saas                  sports-recreation
telecommunications            textiles                       tourism
toys-games                    transportation-and-mobility    travel-leisure
virtual-augmented-reality     warehousing-storage            web-development-hosting
wholesale                     wine-and-spirits               work-from-home
```

If in doubt about any enum's current live options, fetch them with `hubspot-get-property`
before writing.
