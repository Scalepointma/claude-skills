# Sub-ICP G · Broker-Represented Seller

> **Internal label.** Co-broking scenario, not direct representation.

## Essence

I have a broker, but I want BASAB's tools.

Seller has already signed a representation engagement with a different broker. ScalePoint would be co-broking or providing tools rather than full representation. The classification is about the *engagement structure*, not the seller's underlying profile.

## Telltale signs

- Mentions another broker by name in the first meeting
- First contact often comes from the broker, not the seller
- Forms and documents arrive broker-completed
- Seller defers timeline and procedural questions to their broker
- Commission structure is fixed by their existing engagement, not negotiable by us

## Easy to confuse with

- **D (Sophisticated FSBO).** Distinguishing question: *"Are you currently under engagement with another broker?"* G yes; D no by choice. If they say "I worked with one before but we parted ways," that's D (or whatever profile they fit), not G.

## Match Matrix verdicts for row G

| Buyer cohort | Verdict |
|---|---|
| Strategic Acquirer | **Strong** |
| Searcher (ETA) | Possible |
| Owner-Operator | Weak |
| LP / Passive | **Strong** |
| Family Office | **Strong** |
| Holdco / Roll-up | **Strong** |
| Searcher-Broker | Possible |

**Four Strong matches: Strategic, LP, Family Office, Holdco.** Funds and Strategic Acquirers can absorb the additional broker friction in pricing. Owner-Operator is Weak — broker friction adds time and cost that small buyers won't absorb. Searcher and Searcher-Broker are Possible depending on deal size and fund flexibility.

## First-meeting move

Lead with the broker, not the seller.

- Establish co-broking terms first; involve the seller only after broker-to-broker clarity
- Avoid any move that looks like circumvention of the existing engagement
- Confirm the split: standard co-broke is 50/50 of the seller-side fee, but verify
- Capture the listing broker's firm and contact in HubSpot
- Sam-type brokers (operator-leaning, transparent, professional) can become long-term referral partners — treat them that way, not as competitors

## Suggested HubSpot writes

- `seller_sub_icp` = `Broker-Represented`
- `seller_free_text_notes` → append "G: listing broker firm {firm}; listing broker contact {name + email}; co-broke split {%}; Sam-type referral potential {yes|no}"
- Consider associating the broker as a separate Contact with `contact_type_referrer` set, so the relationship is tracked

## What changes G → something else

- The seller terminates their existing engagement (cooling-off period or contract end) → re-evaluate as whatever their underlying profile is (most commonly C or D)
- The seller's broker is the introducer for a different deal entirely (not their own business) → that broker is a referrer, not co-broke; reassign appropriately
