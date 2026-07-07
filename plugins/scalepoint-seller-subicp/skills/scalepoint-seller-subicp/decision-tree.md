# Seller Sub-ICP Decision Tree

Walk through these five checks in order during the conversation. Stop at the first one that fires. The order matters — earlier checks short-circuit later ones because they change the deal type, not just the seller's intent.

---

## Check 1 · Engagement status

**Ask:** "Are you currently under engagement with another broker?"

| Answer | Sub-ICP | Action |
|---|---|---|
| Yes | **G · Broker-Represented** | Stop. Open `reference-cards/G-broker-represented.md`. |
| No (or "I worked with one before, but we parted ways") | Continue to Check 2 | — |

Note: "Used to have one" ≠ "have one now." Confirm explicitly that no current engagement letter exists with a competitor.

---

## Check 2 · Business structure

**Ask:** "Is this an independent business or a franchise unit?"

If franchise, follow up with: "Does the franchisor need to approve any buyer?"

| Answer | Sub-ICP | Action |
|---|---|---|
| Independent | Continue to Check 3 | — |
| Franchise + franchisor has approval rights | **F · Franchise Resale** | Stop. Open `reference-cards/F-franchise-resale.md`. |

Note: F overrides every other category. A franchise reseller in a divorce is still F (not E), because the franchisor's approval timeline drives the deal mechanics more than the seller's urgency does.

---

## Check 3 · Urgency

**Ask:** "Is there a specific event or circumstance driving when this needs to close?"

Listen for: health diagnosis, divorce, partner death, debt problem, forced relocation, hard retirement deadline.

**Distinguishing question if ambiguous:** "If this didn't close in 6 months, what would happen?"

| Answer | Sub-ICP | Action |
|---|---|---|
| Names a specific life event with a hard timeline; "I can't let that happen" | **E · Time-Pressured Seller** | Stop. Open `reference-cards/E-time-pressured.md`. |
| "I'd be disappointed but life would go on" | Continue to Check 4 | — |
| No event named | Continue to Check 4 | — |

---

## Check 4 · Commitment level

**Ask:** "If a qualified buyer walked in tomorrow with a fair offer, would you take it?"

| Answer | Sub-ICP | Action |
|---|---|---|
| "Pass — not ready" / "Just curious" | **A · Valuation-Curious** | Stop. Open `reference-cards/A-valuation-curious.md`. |
| "I'd consider, but I want to be properly prepared first" | **B · Pre-Seller** | Stop. Open `reference-cards/B-pre-seller.md`. |
| "Yes, if the number is right" | Continue to Check 5 | — |

Calibration: A and B both hedge, but the texture is different. A is curiosity without commitment. B is commitment without readiness. The distinguishing question: "In the last 90 days, have you talked to an accountant, lawyer, or family about selling?" B has. A hasn't.

---

## Check 5 · Sophistication

A committed seller is either C (Main Street) or D (Sophisticated FSBO). Three questions distinguish them:

1. **"If you stopped working tomorrow, would the business still run?"**
2. **"Do you have accountant-prepared statements (Notice-to-Reader, Review, or Audited)?"**
3. **"What's your annual revenue range?"**

| Pattern | Sub-ICP | Action |
|---|---|---|
| Business runs without owner + accountant-prepared financials + $2M–$10M revenue | **D · Sophisticated FSBO** | Stop. Open `reference-cards/D-sophisticated-fsbo.md`. |
| Business runs on owner + informal books / T4s only + $300K–$1M revenue | **C · Committed Main Street Seller** | Stop. Open `reference-cards/C-committed-main-street.md`. |
| Mixed signals or revenue $1M–$2M with partial sophistication | Leave `seller_sub_icp` blank. Flag for broker review. Capture observations in `seller_free_text_notes`. | — |

Calibration: D is a *choice*. A seller can have clean books and still be C if they want full broker representation. D is the seller who has consciously interviewed brokers and decided FSBO is the right path for their deal size.

---

## After classification

For every seller, regardless of Sub-ICP, capture these in HubSpot:

- `seller_sub_icp` → the matched value
- `seller_free_text_notes` → append (do not overwrite):
  - The distinguishing observation that pushed the verdict one way or the other
  - The triggering event if named (E especially, but also F and the rare C/D)
  - Broker confidence in the classification, 1–5
  - Re-touch interval suggestion (90 days for B; 6 months for A; 12 months for inactive G; immediate for E)

If `reason_for_sale` came up naturally, capture it too — but never derive Sub-ICP solely from `reason_for_sale`. Reason is one signal among many.

---

## When the tree doesn't fit

Some sellers genuinely don't fit any of the seven. Examples:

- Capital raise / partial sale (not really a seller)
- Family transition where the "sale" is mostly paperwork
- Asset sale rather than business sale
- Pre-revenue or pre-profitability businesses

In these cases: leave `seller_sub_icp` blank, set `inquiry_disposition` to a descriptive value, and route to Jodi for a "is this a real ScalePoint deal" conversation. Don't force one of A–G.
