---
game: ref_auction
model: fleet-glm53
condition: win
seed: 3
round: 1
chars: 2426
---
# Playbook: open ascending auction

**Hard cap rule:** never bid above my private value for a lot. When the standing bid plus minimum raise exceeds my value, I pass immediately, no exceptions.

**Budget tracking:** my budget is 30 total across all lots. Before any bid, compute remaining budget correctly — I mis-stated it repeatedly (claiming 94, 100, 88 mid-game after already spending), which signals I wasn't tracking spend. After each win, subtract the winning price from the running total and use that number every round until the next transaction.

**Don't pay full price in round 1:** each lot runs 2 rounds. Opening with a big jump in round 1 (like bidding 20 when standing was 11) just costs money if I'd have won anyway, and I actually lost that lot at 11 while my money was still committed as the high bid during round 1. In round 1, bid small — minimum raise or slightly above — to stay in without revealing strength. Save decisive raises for round 2.

**Round 2 decision:** in round 2, if standing bid + minimum raise is below my value, raise just enough (minimum raise) rather than a large jump. There's no prize for outbidding by a lot.

**Competitive bidding at small margins:** bidding up lots where my value barely exceeds the price (e.g., value 11, paying 8-10) means I risk my whole budget for tiny or negative surplus while better lots come later. When surplus is under ~20% of value, pass unless the budget is still ample and few valuable lots remain.

**Prioritize the budget:** I won nothing early, then spent nearly everything on the last cheap-surplus lot. Instead, rank by expected surplus (value minus likely clearing price). Lots with high value relative to estimate deserve a firm final-round bid; lots with value below or near estimate deserve only token minimum bids or passes.

**When it's put to me:**
- Round 1 with no/low bids: bid minimum raise, no more.
- Round 1 with a meaningful standing bid: bid minimum raise if standing is under ~60% of my value; otherwise pass and wait for round 2.
- Round 2: if standing + minimum raise < my value, bid standing + minimum raise exactly. Otherwise pass.
- Never exceed one-third of remaining budget on a single lot if more lots with unknown values remain.
- If my value is below the estimate and others are bidding, pass entirely — don't chip in 2-3 just to "test the field"; it wastes money when outbid and wins a near-zero-surplus lot when not.