---
game: ta_negotiation
model: fleet-qwen38
condition: win
seed: 6
round: 1
chars: 1937
---
# Playbook

**Identifying profitable trades**
- For each resource I hold, compute the spread: (my value) − (GM's published value). Resources where my value is low and GM's is high are my "give" candidates. Resources where my value is high and GM's is low are my "take" candidates.
- Each round, pick the give/take pair that maximizes my net gain (take value to me minus give value to me), subject to the GM's net gain being at least 2.

**Calculating the claim**
- The claim is the GM's net gain in the GM's own published values: (value of what GM receives) − (value of what GM gives up).
- I must state the exact true figure. If I understate it below 2, the GM rejects the trade and I waste a round. If I overstate it, I risk the trade being invalidated. Always do the arithmetic before writing the claim.

**Sizing the trade**
- Maximize the quantity of the spread pair within the 1–3 limit and within available stock on both sides. A 3-for-3 trade on a high-spread pair is worth three times a 1-for-1.
- Check the GM's current stock before proposing: if the GM has 0 of the resource I want to take, I cannot take it.

**Pivoting when my best "give" runs out**
- When I exhaust my highest-spread give-resource, immediately identify the next-best give-resource (next highest GM-value minus my-value) and re-optimize the trade around it.
- Re-check which take-resources the GM still holds after each accepted trade, since their stock changes.

**When no positive-gain trade exists**
- If every possible trade gives me a net loss (or zero), I hold.
- A small positive gain (+1) is still worth taking if the claim can be stated truthfully at ≥ 2.

**Round-by-round discipline**
- Each round I recompute from current stocks and values. I do not carry over a plan from a previous round without verifying it still fits.
- In the final round, I accept any trade that yields even +1 for me, since there is no future round to preserve stock for.