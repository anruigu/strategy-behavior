---
game: ta_negotiation
model: fleet-qwen38
condition: win
seed: 6
round: 2
chars: 3412
---
# Playbook

**Identifying profitable trades**
- For each resource I hold, compute the spread: (my value) − (GM's published value). Resources where my value is low and GM's is high are my "give" candidates. Resources where I value them high relative to what I'm giving up are my "take" candidates.
- A trade (give X, take Y) is viable only if BOTH conditions hold simultaneously:
  - My gain > 0: my_value(Y) × qty_take > my_value(X) × qty_give
  - GM's gain ≥ 2: GM_value(X) × qty_give − GM_value(Y) × qty_take ≥ 2
- This means I need a pair where I value Y more than X (in ratio) AND the GM values X more than Y (in ratio). These are different conditions — do not reduce the test to "do I value any single resource more than the GM does."
- Check all (give_resource, take_resource) pairs from my current stock, not just the single best-spread resource.

**Calculating the claim**
- The claim is the GM's net gain in the GM's own published values: (GM_value of what GM receives) × qty_give − (GM_value of what GM gives up) × qty_take.
- I must state the exact true figure. If I understate it below 2, the GM rejects the trade and I waste a round. If I overstate it, the trade is invalidated. Always do the arithmetic before writing the claim.

**Sizing the trade**
- Do not default to maximizing quantity. Test all quantity combinations (1–3 × 1–3) within available stock on both sides. A 3-for-1 trade may work where a 3-for-2 fails, because the GM's gain depends on the ratio.
- The right quantity is the one that keeps my gain positive while pushing the GM's gain to at least 2. Sometimes the minimum quantity that satisfies the GM's constraint is the maximum I can give.
- Check the GM's current stock before proposing: if the GM has fewer than qty_take of the resource I want, I cannot take it.

**When no positive-gain trade exists**
- Before concluding no trade exists, I must verify exhaustively: for every pair (X in my stock, Y in GM's stock) and every quantity combination, check both gain conditions. Only hold if truly no combination satisfies both.
- A common false shortcut: "I don't value any resource more than the GM does, so I can't gain." This is wrong. I can gain by giving a resource the GM overvalues relative to me, in exchange for a resource I value more than what I'm giving — even if I don't value that take-resource more than the GM does in absolute terms. What matters is the relative ordering within the pair.
- A small positive gain (+1) is still worth taking if the claim can be stated truthfully at ≥ 2.

**Pivoting when my best "give" runs out**
- When I exhaust my highest-spread give-resource, re-run the full pair search over remaining stock. Do not assume the next-best single resource will work — it may not pair with any available take-resource to satisfy the GM's constraint.
- Re-check which take-resources the GM still holds after each accepted trade, since their stock changes.

**Round-by-round discipline**
- Each round I recompute from current stocks and values. I do not carry over a plan from a previous round without verifying it still fits.
- In the final round, I accept any trade that yields even +1 for me, since there is no future round to preserve stock for.
- If I have held for several consecutive rounds, I should re-verify my "no trade" conclusion one final time before accepting it, since a single arithmetic error can cause me to miss a viable trade.