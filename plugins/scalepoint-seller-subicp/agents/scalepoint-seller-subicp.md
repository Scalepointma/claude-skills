---
name: seller-subicp-identifier
description: Identify a seller's Sub-ICP (A through G) during intake conversations, coffee meetings, podcast interviews, or post-meeting follow-up. Use when categorizing a new seller, when seller_sub_icp needs to be set on a Contact, when planning next steps for a specific seller, or when reviewing a seller in the pipeline. Powers the row index of the ScalePoint Match Matrix. Use anytime you hear "what kind of seller is this," "categorize this seller," "is this a real seller," "Pre-Seller vs FSBO," or anything similar. Internal use only — never quote sub-ICP labels back to a seller.
---

# Seller Sub-ICP Identifier

> **Internal use only.** Some sub-ICP labels (Time-Pressured, Committed Main Street, Valuation-Curious) are internal nomenclature. Never quote them back to a seller. Never expose them in customer-facing communication. They live in HubSpot as `seller_sub_icp` for matching purposes only.

## What this skill is for

ScalePoint sorts every seller into one of seven Sub-ICPs. The Sub-ICP is the row index of the Match Matrix — it determines which buyer cohorts a seller should be intro'd to, and it shapes what Sam or Alina does next in the engagement. Set it early, revisit it after meaningful conversations, and let it drive routing.

The seven Sub-ICPs:

| Letter | Name | One-line |
|---|---|---|
| A | Valuation-Curious | Just looking. Not selling. Maybe ever. |
| B | Pre-Seller | Selling in 1–3 years. Doing homework now. |
| C | Committed Main Street Seller | Wants out this year. Business runs on them. |
| D | Sophisticated FSBO | Decided seller, $2–10M, clean books, chose FSBO. |
| E | Time-Pressured Seller | Life is driving the timeline. Speed > price. |
| F | Franchise Resale | Selling a franchise unit. Franchisor is in the way. |
| G | Broker-Represented | Already has a broker. We'd co-broke. |

## When to invoke this skill

Invoke when:

- Starting any seller-side intake conversation (coffee meeting, intro call, podcast interview, LinkedIn lead-in)
- A new seller Contact lands in HubSpot without `seller_sub_icp` set
- A seller's situation appears to have changed and the existing Sub-ICP may no longer fit
- Reviewing a stalled seller in the Inquiry/Listing pipeline ("why hasn't this advanced?" — often a misclassified Sub-ICP)
- Drafting follow-up questions for the next conversation with a seller whose Sub-ICP wasn't pinned down at first meeting

## How to use

**Step 1 — Open the decision tree.**

Read `decision-tree.md` and walk the user through the five checks in order. The checks are hierarchical: if a check fires, stop and route to the matching reference card. Don't keep asking questions once you have an answer. The order matters — broker engagement and franchise structure short-circuit everything else because they change the deal type regardless of seller intent.

**Step 2 — Once you have a verdict, surface the reference card.**

Read the matching card from `reference-cards/`:

- `A-valuation-curious.md`
- `B-pre-seller.md`
- `C-committed-main-street.md`
- `D-sophisticated-fsbo.md`
- `E-time-pressured.md`
- `F-franchise-resale.md`
- `G-broker-represented.md`

Each card has: essence, telltale signs, easy-to-confuse-with (with distinguishing question), Match Matrix verdicts for that row, first-meeting move.

**Step 3 — Write to HubSpot.**

Use the HubSpot MCP `manage_crm_objects` tool to update the seller Contact:

- `seller_sub_icp` → the matched value (one of: `Valuation-Curious`, `Pre-Seller`, `Committed Main Street Seller`, `Sophisticated FSBO`, `Time-Pressured Seller`, `Franchise Resale`, `Broker-Represented`)
- `reason_for_sale` → if the seller named a clear reason (use existing enum values)
- `sale_timeline` → if the seller named a timeline
- `seller_free_text_notes` → append: distinguishing observation, triggering event named, broker confidence (1–5)

**Step 4 — Suggest the next move.**

Read the "First-meeting move" section of the matched reference card and propose it to the user as the next action. Be specific: who does what, by when, with what artifact.

## Calibration rules

1. **Trust the broker over the form.** This skill is a sharpener, not a replacement for Sam or Alina's instinct. If the broker says "this doesn't feel like a B, this feels like a soft C," respect that and capture the override in `seller_free_text_notes` so we can audit calibration over time.

2. **Ambiguous → leave blank.** If the seller doesn't fit cleanly, do NOT force a Sub-ICP. Set `seller_sub_icp` to blank, flag the Contact for broker review, and put the observation in `seller_free_text_notes`. False categorization is worse than no categorization.

3. **Re-categorize is normal.** A B (Pre-Seller) becomes a C six months later when they decide. An A (Valuation-Curious) becomes an E (Time-Pressured) when life happens. Update the property as the seller changes. The match engine respects the current value, not historical.

4. **Never collapse F or G into another category.** Franchise and Broker-Represented short-circuit everything else because they change the legal and commercial structure of the deal, not just the seller's intent. Even a Time-Pressured franchise reseller is F, not E.

5. **D ≠ C with better books.** Sophisticated FSBO is a deliberate choice to forgo broker representation, not just clean financials. A C with clean books is still C if they want full broker representation.

## Reference: the Match Matrix

For the full 7×7 verdict grid (buyer sub-types × seller sub-ICPs), see `match-matrix.md`. Every reference card surfaces the matrix row for its Sub-ICP.

## Don't

- Quote internal labels back to the seller ("you're a Valuation-Curious")
- Use legacy internal shorthand (e.g. "Forced Seller" — that's E, "Time-Pressured Seller," now)
- Auto-derive Sub-ICP from `reason_for_sale` alone — reason is one signal among many
- Set Sub-ICP for a seller who hasn't actually had a real conversation; categorization needs evidence
