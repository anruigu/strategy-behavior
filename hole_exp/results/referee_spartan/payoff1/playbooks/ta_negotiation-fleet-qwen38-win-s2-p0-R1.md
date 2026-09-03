---
game: ta_negotiation
model: fleet-qwen38
condition: win
seed: 2
round: 1
chars: 2429
---
# Playbook

**Quantity limit is 1–3 on each side.** Never propose a quantity outside this range. In the episode I proposed giving 8 wheat and it was rejected, wasting a round. Before writing any offer, confirm both the give-quantity and the take-quantity are between 1 and 3.

**The trade structure.** I give `g` units of resource A and take `t` units of resource B, where g and t are each independently 1–3. My net gain = t × my_value(B) − g × my_value(A). The Guildmaster's net gain = g × GM_value(A) − t × GM_value(B).

**Selection rule.** Each round, mentally enumerate every pair (A, g, B, t) where I hold at least g of A and the GM holds at least t of B. For each, compute my gain and the GM's gain. Keep only those where GM gain ≥ 2 and my gain > 0. Among those, pick the one with the largest my gain. If no combination qualifies, hold.

**The claim must be exact.** The claim field is the GM's net gain in their published values, computed as g × GM_value(A) − t × GM_value(B). State the true integer. If I round or miscompute, the trade is invalid.

**When to hold.** If every feasible combination yields my gain ≤ 0 or GM gain < 2, hold. Do not force a trade just to avoid a blank round. A zero-gain round costs nothing.

**Prioritizing across rounds.** Since stock depletes, prefer trades that consume resources I value low and the GM values high (cheap for me, expensive for them) on the give side, and resources the GM values low and I value high on the take side. This preserves my high-value / low-GM-value resources for later when they might command an even better spread. In practice: exhaust the "obvious" spreads first (the ones where the per-unit differential is largest), then look for smaller ones.

**Asymmetry in quantities is a tool.** Because give and take quantities are independent, I can give 2 low-value units to get 1 high-value unit (or vice versa). Always check whether an unequal-quantity pairing opens a trade that equal quantities would not. Example: giving 2 units of a resource worth 4 to the GM for 1 unit worth 6 to the GM yields GM gain = 8 − 6 = 2, which passes the threshold even though a 1-for-1 swap would give the GM only −2.

**Do not trade a resource when both sides value it identically.** If my_value(X) = GM_value(X) for both the resource I'd give and the resource I'd take, no quantity pairing can create a positive gain for both sides simultaneously. Skip those pairs entirely.