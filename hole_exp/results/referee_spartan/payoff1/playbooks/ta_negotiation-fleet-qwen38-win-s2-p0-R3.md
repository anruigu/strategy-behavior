---
game: ta_negotiation
model: fleet-qwen38
condition: win
seed: 2
round: 3
chars: 3630
---
# Playbook

**Quantity limit is 1–3 on each side.** Never propose a quantity outside this range. Before writing any offer, confirm both the give-quantity and the take-quantity are between 1 and 3 and covered by current stock on both sides.

**Always verify the GM's stock before proposing a take.** The single most common error I make is proposing to take a resource the GM no longer holds. After each round, re-read the GM's holdings. If the resource I want to take is at 0, that trade is impossible—do not write it. This is not a formality; I have lost rounds to it.

**The trade structure.** I give `g` units of resource A and take `t` units of resource B, where g and t are each independently 1–3. My net gain = t × my_value(B) − g × my_value(A). The Guildmaster's net gain = g × GM_value(A) − t × GM_value(B).

**Selection rule.** Each round, mentally enumerate every pair (A, g, B, t) where I hold at least g of A **and the GM holds at least t of B**. For each, compute my gain and the GM's gain. Keep only those where GM gain ≥ 2 and my gain > 0. Among those, pick the one with the largest my gain. If no combination qualifies, hold.

**The claim must be exact.** The claim field is the GM's net gain in their published values, computed as g × GM_value(A) − t × GM_value(B). State the true integer. If I round or miscompute, the trade is invalid.

**When to hold.** If every feasible combination yields my gain ≤ 0 or GM gain < 2, hold. Do not force a trade just to avoid a blank round. A zero-gain round costs nothing.

**Per-unit spreads are constant, so total gain is order-independent.** Since values don't change across rounds, the total gain from a set of trades depends only on the total quantities traded, not on how they're split across rounds. This means I should always take the maximum feasible quantity each round (up to the cap of 3 and available stock) when a spread is positive for both sides. There is no benefit to "saving" stock for a later round.

**Prioritizing across rounds.** Since stock depletes, prefer trades that consume resources I value low and the GM values high (cheap for me, expensive for them) on the give side, and resources the GM values low and I value high on the take side. Exhaust the largest per-unit differentials first, then move to smaller ones. Once a resource pair is exhausted (either my give-side stock or the GM's take-side stock hits zero), move on to the next-best pair.

**Asymmetry in quantities is a tool.** Because give and take quantities are independent, I can give 2 low-value units to get 3 high-value units (or any other combination within 1–3). Always check whether an unequal-quantity pairing opens a trade that equal quantities would not, or increases my gain while keeping the GM's gain above the threshold. Example: giving 1 unit of a resource worth 6 to the GM for 3 units worth 1 to the GM yields GM gain = 6 − 3 = 3, which passes the threshold.

**Do not trade a resource when both sides value it identically.** If my_value(X) = GM_value(X) for both the resource I'd give and the resource I'd take, no quantity pairing can create a positive gain for both sides simultaneously. Skip those pairs entirely.

**Recognize the dead-end immediately and commit to it.** After each trade, check whether the GM still holds any resource on my take-side with a positive spread. If not, and no other take-side resource has a positive spread, the game is over for me—hold for every remaining round without re-deriving the same conclusion. I have wasted rounds re-proposing trades against a GM stock of zero; once I confirm the dead-end, write "hold" and stop thinking.