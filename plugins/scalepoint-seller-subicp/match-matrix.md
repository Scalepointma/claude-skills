# Match Matrix

The 7×7 verdict grid. Rows are seller Sub-ICPs. Columns are buyer sub-types. Cell value is the verdict Delta returns when evaluating a potential pair.

**Verdict legend:**

- **S · Strong** — Auto-add to Sam's outreach list. Highest priority.
- **P · Possible** — Surface for review. Sam decides whether to include.
- **W · Weak** — Skip on first round. Resurface only if first-tier outreach doesn't fill the room.
- **B · Block** — Never intro. Wrong on principle.

---

| Seller ↓ / Buyer → | Strategic Acquirer | Searcher (ETA) | Owner-Operator | LP / Passive | Family Office | Holdco / Roll-up | Searcher-Broker |
|---|---|---|---|---|---|---|---|
| **A · Valuation-Curious** | B | B | B | B | B | B | B |
| **B · Pre-Seller** | W | P | **S** | W | W | W | P |
| **C · Committed Main Street** | **S** | **S** | **S** | W | W | P | **S** |
| **D · Sophisticated FSBO** | **S** | P | W | **S** | **S** | **S** | P |
| **E · Time-Pressured** | **S** | **S** | **S** | W | P | P | **S** |
| **F · Franchise Resale** | **S** (within brand) | **S** | P | W | W | P | **S** |
| **G · Broker-Represented** | **S** | P | W | **S** | **S** | **S** | P |

---

## Where the matrix actually lives

In production, the verdicts are stored in `match-matrix.json` on Delta (the Mac Mini automation host), NOT as a HubSpot property. This means we can tune verdicts without touching HubSpot or paying for a workflow operation. Delta looks up `(buyer_sub_type, seller_sub_icp)` and applies the verdict.

This markdown file is the human-readable source of truth. If you change a verdict here, also update `match-matrix.json` on Delta. They must stay in sync.

## How the match engine uses this

1. **Match Matrix first.** Before any other matching logic, Delta looks up the (buyer_sub_type, seller_sub_icp) pair. If verdict = B (Block), the buyer-seller pair is dropped immediately and never advances to the three-layer match.
2. **Then three-layer match** (Layer 1 canonical fields → Layer 2 tags → Layer 3 LLM free-text), but only on pairs that pass the matrix.
3. **Final ranking** produces the top-30 outreach list per listing, with one-line reasoning beside each name.

## Verdict reasoning

A few of the trickier verdicts explained:

- **Row A (Valuation-Curious) = all Block.** These sellers aren't actually selling. Intro'ing them to any buyer wastes the buyer's trust and Alina's relationship capital.
- **B (Pre-Seller) vs Searcher = P (Possible), not Strong.** Searchers want to deploy capital on a defined timeline. Pre-Sellers are 1–3 years out. Mismatch on urgency. Only escalate if the Pre-Seller's timeline tightens.
- **B (Pre-Seller) vs Owner-Operator = S.** Owner-Operator buyers are patient and prep-friendly. They're the one buyer cohort that can actually wait for a B seller to be ready.
- **C (Committed Main Street) vs LP/Family Office = W.** Deal too small. Funds need $5M+ to justify their cost structure.
- **D (Sophisticated FSBO) vs Owner-Operator = W.** Owner-Operator buyers can't afford $2–10M and don't want a business they can't run themselves.
- **F (Franchise) Strategic = S "within brand," P out-of-brand.** Strategic Acquirers within the same franchise system close fast (already approved). Strategic from a different brand has to clear approval, which adds friction.
- **G (Broker-Represented) vs Owner-Operator = W.** Broker friction adds time and cost that small buyers won't absorb.
