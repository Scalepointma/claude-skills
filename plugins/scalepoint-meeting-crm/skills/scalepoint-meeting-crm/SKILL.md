---
name: scalepoint-meeting-crm
description: >
  Transcribes a meeting recording and populates either a seller profile or a buyer profile in HubSpot.
  TRIGGER: use this skill any time the user says "transcribe this meeting," "fill out the [seller/buyer] profile
  from this call," "log this meeting," "update HubSpot from this recording," "process this intake call,"
  or drops an audio file path (e.g. .m4a, .mp3, .wav, .mp4, .webm) and asks you to do something with it.
  Works with both raw audio files and pre-written transcripts.
  For seller intakes (discovery calls, listing consults, podcast-style interviews).
  For buyer intakes (coffee meetings, onboarding calls, buy-box qualification).
---

# ScalePoint Meeting → CRM Skill

Transcribes a meeting recording (or accepts a pasted transcript) and writes the extracted profile
fields directly into HubSpot — either a seller deal/contact or a buyer contact/company.

> **Schema source of truth:** Appendix A of `Chevron-Customer-Journey.md` (SharePoint/repo)
> is the schema source of truth for every HubSpot property name and enum value in this skill.
> If a write fails on a property name or value, check Appendix A — do not improvise a field name.

---

## Step 1 — Determine input type

Check the user's message for:

- **Audio file path** — any `.m4a`, `.mp3`, `.wav`, `.mp4`, `.webm`, `.ogg`, `.flac` path → go to Step 2 (transcribe)
- **Pasted transcript text** — multi-line text block of dialogue → skip to Step 3
- **Neither** — ask: "Please share the recording file path or paste the transcript text."

---

## Step 2 — Transcribe the audio

Use the `whisper` CLI (installed via `openai-whisper`), writing output to the **session
scratchpad directory** (the scratchpad path listed in your system prompt — never a bare
`/tmp/`):

```bash
whisper "<file_path>" --model medium --language en --output_format txt --output_dir "<scratchpad_dir>"
```

- The output will be at `<scratchpad_dir>/<filename>.txt`
- Read that file to get the transcript text
- If `whisper` is not found, try `python -m whisper` or ask the user to run: `pip install openai-whisper`
- If transcription fails, ask the user to paste the transcript manually

---

## Step 3 — Determine meeting type

If the user did not specify in their message, ask:

> "Is this a **seller** intake (discovery call, listing consult) or a **buyer** intake (coffee meeting, buy-box call)?"

Accept: "seller", "buyer", "s", "b", or context clues like "they want to sell their business" = seller.

---

## Step 4A — Extract SELLER fields

Analyze the transcript and extract as many of these as the transcript supports.
Leave a field blank (`""`) if not mentioned — never guess or invent.

**Contact fields:**
| Field | What to look for |
|---|---|
| `firstname` | Person's first name |
| `lastname` | Last name |
| `email` | Email address spoken or mentioned |
| `phone` | Phone number |
| `seller_sub_icp` | A–G (run the Sub-ICP decision tree if enough info exists — see seller-subicp skill) |
| `reason_for_sale` | Why they want to sell (retirement, burnout, health, partner, opportunity) — enum, see the enum rule below |
| `sale_timeline` | When they want to close ("this year", "12–18 months", etc.) — enum, see the enum rule below |
| `seller_free_text_notes` | Key observations, red flags, tone, any detail that doesn't fit a structured field |

**Deal fields (Listing pipeline):**
| Field | What to look for |
|---|---|
| `dealname` | Business name (use as deal title) |
| `listing_industry` | What the business does — multi-select of the canonical 85 industry slugs (same vocabulary as `buy_box_industries_targeted`/`buy_box_industries_avoided`, mirroring BASAB URLs). Map plain English to existing slugs; **never invent a slug** — an out-of-vocabulary value silently breaks Layer 1 matching |
| `listing_province` | Province where the business operates |
| `listing_location` | City or town |
| `listing_revenue` | Annual revenue (as stated, in CAD) |
| `listing_ebitda` | EBITDA — **only** if the transcript supports the number as EBITDA (see the SDE guardrail below) |
| `listing_ask_low` | Seller's price expectation — lower end |
| `listing_ask_high` | Upper end of price expectation |
| `is_blind_listing_deal` | Set if the seller wants a blind listing (no identifying info public) |
| `blind_title_listing_deal` | The blind title to use, if blind |
| `description` | Brief business description from what they shared |

There is **no** deal property for highlights, reason for sale, or lead source — do not
invent them. Investment highlights, how they found ScalePoint, and any strengths mentioned
go into the Deal's Note engagement / `description`; reason for sale lives on the Contact
(`reason_for_sale`).

**Co-owners / partners:** if the transcript reveals co-owners, spouses with ownership, or
business partners, capture each as an **additional Contact** (name, email/phone if given)
to be associated to the same Deal — do not fold them into the notes of the primary contact.

### Extraction guardrails (seller)

- **SDE ≠ EBITDA.** "I take home $X", "$X before my salary", "owner earnings" = SDE
  (Seller's Discretionary Earnings), NOT normalized EBITDA. Record it in the notes with the
  qualifier ("seller quoted $X as owner earnings/SDE"). Only put a number in
  `listing_ebitda` if the transcript supports it as EBITDA.
- **Transition offer ≠ sale timeline.** "I'll stay on for 6 months to help transition" is a
  post-sale transition offer, not when they want to close. Never map one to the other.
  Transition willingness goes in the notes (and informs `post_sale_owner_involvement` on the
  Contact if clearly stated).
- **Enums accept only their internal values.** `reason_for_sale`, `sale_timeline`, and
  `seller_sub_icp` are enumeration properties — fetch their live options with
  `hubspot-get-property` before writing, and pick the matching internal value. If the
  transcript doesn't map cleanly to an option, leave the field blank and put the seller's
  wording in `seller_free_text_notes`.

---

## Step 4B — Extract BUYER fields

Analyze the transcript and extract as many of these as the transcript supports.

**Contact fields:**
| Field | What to look for |
|---|---|
| `firstname` | First name |
| `lastname` | Last name |
| `email` | Email address |
| `phone` | Phone number |
| `jobtitle` | Their role |
| `company` | Their firm or employer |
| `buyer_type` | One of: `individual_buyer`, `pe_financial_buyer`, `strategic_synergetic_buyer` — infer from context |
| `buy_box_revenue_min` | Minimum annual revenue they'll consider (CAD integer) |
| `buy_box_revenue_max` | Maximum revenue |
| `buy_box_ebitda_min` | Minimum EBITDA (CAD integer) |
| `buy_box_ebitda_max` | Maximum EBITDA |
| `buy_box_industries_targeted` | Industries they want — canonical 85 slugs only, never invented |
| `buy_box_industries_avoided` | Industries they refuse — canonical 85 slugs only |
| `buy_box_description` | In their words: what they're trying to accomplish — "I want to own and operate," "grow our platform," etc. (Layer 3 free text; also goes in the Note) |

**Buyer type inference rules:**
- Individual searching for first acquisition, mentions "operator," "hands-on," "self-funded" → `individual_buyer`
- Mentions fund, LP capital, hold period, IRR, portfolio → `pe_financial_buyer`
- Mentions their existing operating company, expansion, synergies, bolt-on → `strategic_synergetic_buyer`

---

## Step 5 — Present extracted fields for review

Show the user a clean table of everything extracted. Flag uncertain or blank fields clearly.

Example format:
```
SELLER PROFILE — [Business Name]

Contact
  Name:            Jane Smith
  Email:           jane@example.com
  Sub-ICP:         C (Committed Main Street)
  Reason for sale: Retirement — wants out within 12 months

Deal (Listing pipeline)
  Industry:   repair-maintenance (seller said "HVAC services")
  Province:   Ontario
  Location:   —
  Revenue:    $1.4M
  EBITDA:     $320K (transcript supports as EBITDA)
  Ask:        $900K–$1.1M

  → Note: 18-year-old business, 3 lead technicians, mostly commercial recurring.
          Found us via referral from accountant.
          Nervous about staff finding out. Wants confidential process.

⚠ Blank: location, ask_high (only mentioned "around a million")
```

Ask: "Does this look right? Anything to correct?"

---

## Step 6 — RECORD APPROVAL GATE (mandatory — do not skip)

Nothing is written to HubSpot until this gate passes:

1. **Engagement check.** No HubSpot record is created until an engagement is signed, or the
   deal lead explicitly says otherwise. Pre-engagement research stays in Excel/SharePoint —
   offer to save the extraction there instead.

2. **Show the specific records.** State exactly which HubSpot records will be created or
   updated (Contact X, Deal Y, Company Z — create vs update, with the key property values).

3. **Explicit load approval from Jodi (or the deal lead she designates for this deal).**
   Approval means words to the effect of **"load these"** / "write them to HubSpot".
   A staff member confirming "the extraction looks right" is **NOT** approval to write —
   accuracy confirmation and load approval are two different things.

---

## Step 7 — Write to HubSpot

After the gate passes, use HubSpot MCP tools to write the data.

### For SELLER meetings:

1. **Find or create the contact** using `manage_crm_objects` (object type: `contacts`):
   - Search first by email or full name to avoid duplicates
   - Update if found; create if not
   - For enum properties (`reason_for_sale`, `sale_timeline`, `seller_sub_icp`), fetch the
     live options with `hubspot-get-property` first and write only internal enum values

2. **Find or create the deal** using `manage_crm_objects` (object type: `deals`):
   - Search by `dealname`
   - Update if found; create if not
   - The deal is created in the **LISTING pipeline** (stages include Prospect → EL Signed →
     Listing Draft → Approved + Published → Active → Under LOI → Closing → Closed-Won).
     Look up the actual pipeline and stage IDs at runtime via the HubSpot property/schema
     tools (e.g. `hubspot-get-property` on `pipeline`/`dealstage`, or the pipelines API) —
     **never hardcode pipeline or stage IDs**. New intakes land in the "Prospect" stage
     unless the deal lead says otherwise.
   - Note: buyer–listing pairs are tracked as deals in the separate **INQUIRY pipeline** —
     one deal per buyer–listing pair. That is NOT what this skill creates for a seller
     intake; never put a seller listing in the Inquiry pipeline.

3. **Associate contact to deal** if both exist. Capture any co-owners/partners as
   additional Contacts and associate them to the same deal.

4. **Add a NOTE engagement to the deal** with: investment highlights, how they found
   ScalePoint, SDE/owner-earnings figures with their qualifier, transition-offer details,
   and anything else that has no structured property. Include today's date.

5. Confirm to user: "Written to HubSpot. [Contact name] and deal [dealname] are updated."

### For BUYER meetings:

1. **Find or create the contact** using `manage_crm_objects` (object type: `contacts`):
   - Search first by email or full name

2. **Find or create the company** using `manage_crm_objects` (object type: `companies`):
   - Search by company name
   - Associate contact to company after both exist

3. **Add a NOTE engagement to the contact** with the buyer's outcome statement verbatim,
   plain-English industry wording alongside the confirmed slug mapping, and how the meeting
   came about. Include today's date.

4. Confirm to user: "Written to HubSpot. Buyer [name] at [company] is updated."

---

## Rules

- Never write fabricated data. If a field is blank, leave it blank — do not infer from tone.
- **RECORD APPROVAL GATE (Step 6) always applies** — no HubSpot write on transcript
  extraction alone, and no record at all pre-engagement unless the deal lead says otherwise.
- If `is_blind_listing_deal` is set on the deal, never write the seller's name or business
  name into public-facing fields — the public listing uses `blind_title_listing_deal` and
  shows province only.
- Use real company names in HubSpot record names — codenames (`listing_codename`) are for
  external email only.
- **Never invent an industry slug.** The 85-slug vocabulary is maintained in lockstep with
  BASAB's URLs and the HubSpot enums; out-of-vocabulary values silently break Layer 1 matching.
- Enum properties accept only their internal enum values — fetch options via
  `hubspot-get-property` before writing.
- Never hardcode pipeline or stage IDs — look them up at runtime.
- BCC `342889181@bcc.na3.hubspot.com` on any follow-up emails you draft from this skill.
- `seller_free_text_notes` should always get something — even if structured fields are complete, capture the human texture of the conversation (energy level, hesitation, specific phrasing that signals intent).
- For Sub-ICP classification, if sufficient signals exist, run the seller-subicp skill inline. Otherwise, leave `seller_sub_icp` blank and note it in `seller_free_text_notes`.
