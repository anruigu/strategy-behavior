---
game: ref_auction
model: fleet-qwen38
condition: win
seed: 2
round: 2
chars: 3175
---
# Playbook: Ref Auction

**Budget discipline is the first rule.** My starting budget is hard. Before every bid, I calculate: starting budget minus the sum of prices I've already won at. That number is my true remaining budget. I never bid an amount that, if I win, would push my total spending past my remaining budget. I report this true number as my budget every time.

**When I'm the high bidder in round 1 and the price is cheap relative to my value:** I stay in for round 2 by passing (no need to raise my own bid). A low round-1 bid is a probe, not a commitment.

**When round 2 arrives and the minimum raise is at or above my value:** I pass. Bidding at or above my value in the final round guarantees zero or negative surplus. There is no reason to do it.

**When round 2 arrives and the minimum raise is below my value and I can afford it:** I always bid. I never pass in a situation where I have a positive-surplus opportunity. Passing guarantees zero; bidding at least gives me a chance to win.

**How much to bid in round 2 when I'm below my value:**
- If my value is only modestly above the minimum raise (surplus ≤ 15): bid the minimum raise. I don't want to inflate the price on a thin-margin lot.
- If my value is well above the minimum raise (surplus > 15): bid above the minimum. A practical target is roughly 60–70% of my value, capped at what I can afford. The rationale: a competitor who outbid me in round 1 is likely to raise again in round 2. Bidding only the minimum invites them to win cheaply. Bidding higher increases my probability of winning while still preserving meaningful surplus.

**When I'm opening a lot (no standing bid) in round 1:** I bid the minimum. This costs me nothing if I lose and secures my right to compete in round 2. I do not open with a moderate or high bid — it only anchors the auction upward.

**When I've already won expensive lots and my remaining budget is small:** I only enter auctions where my value exceeds (remaining budget + expected final price). If I can't afford to win, I don't enter. Passing is free.

**What I got wrong last time and what I got right:**
- Right: Budget tracking was accurate throughout. I consistently reported 83 after winning lot 1 at 17.
- Right: Opening at minimum in round 1 and passing when already the high bidder both worked well (lots 1 and 5).
- Wrong: On lot 2, I passed in round 2 when the minimum raise (20) was well below my value (41) and within my budget. I should have bid. This was a pure error — no rule justified passing.
- Wrong: On lot 4, I bid only the minimum (20) on a lot worth 39 to me, and lost to a competitor who bid 28. My surplus at 20 would have been 19 (large by my threshold), so I should have bid higher — around 24–27 — to increase my chance of winning.

**Summary decision flow for each round-2 call:**
1. Is the minimum raise ≥ my value? → Pass.
2. Can I afford the minimum raise within my true remaining budget? → If no, pass.
3. Is my surplus at the minimum raise ≤ 15? → Bid the minimum raise.
4. Is my surplus at the minimum raise > 15? → Bid roughly 60–70% of my value (or the minimum raise, whichever is higher), as long as it's within budget.