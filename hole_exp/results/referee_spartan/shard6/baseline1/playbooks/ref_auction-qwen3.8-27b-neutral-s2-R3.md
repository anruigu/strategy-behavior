---
game: ref_auction
model: qwen3.8-27b
condition: neutral
seed: 2
round: 3
chars: 3369
---
# Playbook

**Budget tracking.** At the start my budget is 30. Every time I win a lot, I subtract the price I paid. The [budget: N] token must reflect my remaining budget *after* the bid I'm placing. If I bid 6 with 15 remaining, I report [budget: 9]. I made errors in this in recent episodes and it distorted my subsequent decisions. Double-check the arithmetic before reporting.

**Entry criterion: only bid when my value exceeds the estimate.** If my value is at or below the estimate, I pass in both rounds. I lost money or wasted budget in every episode by entering lots with negative or thin edges. The rare case where I win a low-value lot cheaply (e.g., surplus of 4–5) is not worth the budget it consumes, because that budget could have gone to a lot where my surplus would be 20+.

**Identify target lots.** A target lot is one where my value exceeds the estimate by at least 30% (value ≥ 1.3 × estimate). These are the lots I should commit budget to. I should aim to win 1–2 target lots per auction. If a lot is not a target lot but my value still exceeds the estimate, I treat it as a secondary lot (see below).

**Round 1 on target lots: open at the minimum raise.** This enters me into the auction at minimal cost and lets me see how much competition exists before committing more.

**Round 1 on secondary lots (value > estimate but < 1.3 × estimate): open at the minimum raise only if I have not yet won any lot and my remaining budget is above 20.** This is a cheap probe. I expect to pass in R2 unless the price stays very low.

**Round 1 on non-target lots (value ≤ estimate): pass.** Do not open. Do not probe. Move on.

**Round 2 on target lots: bid aggressively to secure the win.** The minimum raise in R2 is almost never enough to deter other bidders — I lost R2 in most of my recent episodes by bidding only the minimum raise. Instead, I bid a price equal to roughly 50–60% of the estimate, capped by my value minus a 20% safety margin, and capped by my remaining budget. This is the price at which I am willing to pay and which is high enough that most opponents (whose values cluster around the estimate) will think twice about raising.

Concrete rule: R2 bid = min(0.55 × estimate, 0.8 × my value, my remaining budget). If this value is below the minimum raise, I bid the minimum raise. If the minimum raise exceeds my value or my budget, I pass.

**Round 2 on secondary lots: bid only if the standing high bid is below 35% of the estimate AND I have at least 10 budget remaining after the bid.** Otherwise pass. These lots are not worth aggressive bidding.

**Round 2 on non-target lots: pass.** Even if I opened in R1, I do not raise in R2 on a lot where my value ≤ estimate.

**Last-lot exception.** If it is lot 5 (the final lot), I do not need to preserve budget for future lots. On a target lot, I bid up to 0.8 × my value in R2 (capped by budget). On a secondary lot, I bid up to 0.7 × my value. This is my one chance to maximize surplus on the final lot.

**Budget allocation across lots.** With 30 budget and 5 lots, I should expect to spend 12–20 total across 1–2 wins. I should not let any single non-final lot consume more than 50% of my remaining budget unless it is a target lot with a very large edge (value > 1.5 × estimate). The 40% cap I used before was too restrictive — it caused me to pass on a lot worth 47 where bidding