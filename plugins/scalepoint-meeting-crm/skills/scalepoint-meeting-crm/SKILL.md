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

---

## Step 1 — Determine input type

Check the user's message for:

- **Audio file path** — any `.m4a`, `.mp3`, `.wav`, `.mp4`, `.webm`, `.ogg`, `.flac` path → go to Step 2 (transcribe)
- **Pasted transcript text** — multi-line text block of dialogue → skip to Step 3
- **Neither** — ask: "Please share the recording file path or paste the transcript text."

---

## Step 2 — Transcribe the audio

Use the `whisper` CLI (installed via `openai-whisper`):

```bash
whisper "<file_path>" --model medium --language en --output_format txt --output_dir /tmp/
```

- The output will be at `/tmp/<filename>.txt`
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
| `reason_for_sale` | Why they want to sell (retirement, burnout, health, partner, opportunity) |
| `sale_timeline` | When they want to close ("this year", "12–18 months", etc.) |
| `seller_free_text_notes` | Key observations, red flags, tone, any detail that doesn't fit a structured field |

**Deal fields:**
| Field | What to look for |
|---|---|
| `dealname` | Business name (use as deal title) |
| `industry` | What the business does |
| `province` | Province where the business operates |
| `location` | City or town |
| `revenue` | Annual revenue (as stated, in CAD) |
| `ebitda` | EBITDA or owner earnings |
| `ask_low` | Seller's price expectation — lower end |
| `ask_high` | Upper end of price expectation |
| `description` | Brief business description from what they shared |
| `highlights` | Key strengths mentioned (strong staff, recurring clients, no lease risk, etc.) |
| `reason_for_sale` | (same as contact field — write to both) |
| `source` | How they found ScalePoint (referral, LinkedIn, podcast, website, etc.) |

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
| `outcome_statement` | In their words: what they're trying to accomplish — "I want to own and operate," "grow our platform," etc. |

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

Deal
  Industry:   HVAC services
  Province:   Ontario
  Revenue:    $1.4M
  EBITDA:     $320K
  Ask:        $900K–$1.1M
  Source:     Referral from accountant

  Highlights: 18-year-old business, 3 lead technicians, mostly commercial recurring
  Notes:      Nervous about staff finding out. Wants confidential process.

⚠ Blank: location, ask_high (only mentioned "around a million")
```

Ask: "Does this look right? Anything to correct before I write to HubSpot?"

---

## Step 6 — Write to HubSpot

After the user confirms (or makes corrections), use HubSpot MCP tools to write the data.

### For SELLER meetings:

1. **Find or create the contact** using `manage_crm_objects` (object type: `contacts`):
   - Search first by email or full name to avoid duplicates
   - Update if found; create if not

2. **Find or create the deal** using `manage_crm_objects` (object type: `deals`):
   - Search by `dealname`
   - Update if found; create if not
   - Set `pipeline` to the seller intake pipeline

3. **Associate contact to deal** if both exist.

4. Confirm to user: "Written to HubSpot. [Contact name] and deal [dealname] are updated."

### For BUYER meetings:

1. **Find or create the contact** using `manage_crm_objects` (object type: `contacts`):
   - Search first by email or full name

2. **Find or create the company** using `manage_crm_objects` (object type: `companies`):
   - Search by company name
   - Associate contact to company after both exist

3. Confirm to user: "Written to HubSpot. Buyer [name] at [company] is updated."

---

## Rules

- Never write fabricated data. If a field is blank, leave it blank — do not infer from tone.
- Never write the seller's name or business name into public-facing fields if `is_blind` is true.
- Use real company names in HubSpot — codenames are for external email only.
- BCC `342889181@bcc.na3.hubspot.com` on any follow-up emails you draft from this skill.
- `seller_free_text_notes` should always get something — even if structured fields are complete, capture the human texture of the conversation (energy level, hesitation, specific phrasing that signals intent).
- For Sub-ICP classification, if sufficient signals exist, run the seller-subicp skill inline. Otherwise, leave `seller_sub_icp` blank and note it in `seller_free_text_notes`.
