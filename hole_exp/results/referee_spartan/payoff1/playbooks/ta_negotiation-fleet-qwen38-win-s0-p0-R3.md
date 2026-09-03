---
game: ta_negotiation
model: fleet-qwen38
condition: win
seed: 0
round: 3
chars: 1975
---
# Playbook

**Enumerate all feasible trades each round without exception.** For every ordered pair (resource A to give, resource B to take), check whether there exist integer quantities from 1 to 3 (within both parties' current stock) such that:
- GM gain = qty_A × GM_published_val_A − qty_B × GM_published_val_B ≥ 2
- My gain = qty_B × my_private_val_B − qty_A × my_private_val_A > 0

**Quantity differentials work even when GM values both resources equally.** If GM values A and B both at 6, then giving 1 A for 2 B yields GM gain = 12 − 6 = 6 ≥ 2, and I profit whenever my value of B exceeds my value of A. I must never conclude "no feasible trade" simply because GM's remaining resources are all high-value. Always check the 1-for-2 and 1-for-3 patterns across same-valued pairs.

**Always claim the true GM gain.** The claim is computed as qty_A × GM_val_A − qty_B × GM_val_B using the published values. Do not confuse this with my own gain. In this episode I claimed 8 when the true figure was 3 — a clear error that could cost me if the rule is enforced or if the GM's acceptance logic changes.

**Prioritise early rounds to drain GM's low-value resources (those with GM value 1–2).** These produce the largest margins (e.g., 1 ore for 3 wood gave me +10). Once GM's cheap resources are exhausted, I'm limited to same-value exchanges with smaller per-round gains (typically +2 to +4). Spending my high-GM-value resources (ore, brick) early on low-GM-value targets is the highest-yield use of them.

**When only same-value resources remain, prefer to give resources I value lowest and take resources I value highest.** E.g., give ore (my val 2) or brick (my val 2) to take wheat (my val 3) at a 1-for-2 ratio, yielding +4 per trade rather than +2.

**Re-enumerate from scratch every round.** Stocks change; a pattern that was infeasible last round may be feasible now, and vice versa. Do not carry over a "no trade" conclusion from a previous round without rechecking.