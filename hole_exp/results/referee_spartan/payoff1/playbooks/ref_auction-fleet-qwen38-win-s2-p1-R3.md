---
game: ref_auction
model: fleet-qwen38
condition: win
seed: 2
round: 3
chars: 3383
---
# Playbook: Ref Auction

**Budget discipline is the first rule.** My starting budget is hard. Before every bid, I calculate: starting budget minus the sum of prices I've already won at. That number is my true remaining budget. I never bid an amount that, if I win, would push my total spending past my remaining budget. I report this true number as my budget every time.

**Budget pacing across lots.** With multiple lots, I must pace my spending. If I burn most of my budget on early high-value lots, I may be unable to compete on later lots that also have high value to me. Before bidding in round 2, I should consider: if I win this lot at my target price, will I still have enough to compete on a reasonable number of remaining lots? This doesn't mean I pass on a good opportunity, but it does mean I should be willing to accept a lower bid (closer to minimum) on a lot where my surplus is large, to preserve budget for later.

**When I'm opening a lot (no standing bid) in round 1:** I bid the minimum. This costs me nothing if I lose and secures my right to compete in round 2. I do not open with a moderate or high bid — it only anchors the auction upward.

**When I'm the high bidder entering round 2 and the price is cheap relative to my value:** I pass. I stay in without raising. A low round-1 bid is a probe, not a commitment. If no one challenges me, I win at the minimum — the best possible outcome. This was the single most valuable rule in this episode (won a lot at 2, surplus 25).

**When round 2 arrives and the minimum raise is at or above my value:** I pass. Bidding at or above my value in the final round guarantees zero or negative surplus.

**When round 2 arrives and the minimum raise is below my value and I can afford it:** I always bid. Passing guarantees zero; bidding at least gives me a chance to win.

**How much to bid in round 2 when I'm below my value:**
- If my surplus at the minimum raise is ≤ 15: bid the minimum raise. I don't want to inflate the price on a thin-margin lot.
- If my surplus at the minimum raise is > 15: bid above the minimum. A practical target is roughly 60–70% of my value, capped at what I can afford. The rationale: a competitor who outbid me in round 1 is likely to raise again in round 2. Bidding only the minimum invites them to win cheaply. Bidding higher increases my probability of winning while still preserving meaningful surplus.
- If my remaining budget after this lot would leave me unable to compete on any remaining lots, pull my target down toward the minimum raise.

**When my remaining budget is too small to meet the minimum raise:** I pass. There is nothing to be done.

**Summary decision flow for each round:**
1. Round 1, no standing bid → bid the minimum.
2. Round 1, standing bid exists and I'm considering entering → apply the round-2 logic below (value vs. min raise, budget check).
3. Round 2, I'm already the high bidder → pass. Let others raise or let me win cheap.
4. Round 2, I'm not the high bidder:
   a. Is the minimum raise ≥ my value? → Pass.
   b. Can I afford the minimum raise within my true remaining budget? → If no, pass.
   c. Is my surplus at the minimum raise ≤ 15? → Bid the minimum raise.
   d. Is my surplus at the minimum raise > 15? → Bid roughly 60–70% of my value (or the minimum raise, whichever is higher), capped by remaining budget and budget-pacing considerations.