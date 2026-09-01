---
game: ta_negotiation
model: qwen
condition: neutral
seed: 2
round: 2
chars: 1965
---
# Playbook: Simple Negotiation

**Core calculation before every offer:**
- My per-unit gain = my_value(take_resource) − my_value(give_resource). Must be > 0.
- GM per-unit gain = GM_value(give_resource) − GM_value(take_resource). Must be > 0.
- GM total net = GM_per_unit_gain × qty. Must be in [2, 9] inclusive.
- My total net = my_per_unit_gain × qty. This is what I score.
- The claim I file must equal GM total net exactly.

**The claim range is the most important constraint I keep violating:**
- The claim must be a whole number from −9 to 9. If GM total net exceeds 9, the offer is invalid no matter how good the trade looks.
- Before offering, compute GM total net = GM_per_unit_gain × qty. If it exceeds 9, reduce qty until it fits. If even qty 1 gives GM net > 9, that pair is unusable.
- Similarly, if GM_per_unit_gain × qty < 2 even at qty 3, the pair is unusable.
- Valid qty range for a given pair: the set of q ∈ {1, 2, 3} such that 2 ≤ q × GM_per_unit_gain ≤ 9.

**Selection algorithm (run every round):**
1. For every ordered pair (give A, take B) where A ≠ B:
   - Compute my_per_unit_gain and GM_per_unit_gain.
   - If my_per_unit_gain ≤ 0, skip.
   - If GM_per_unit_gain ≤ 0, skip.
   - Find the largest qty in {1, 2, 3} satisfying: qty × GM_per_unit_gain ≤ 9 AND qty × GM_per_unit_gain ≥ 2 AND my_stock(A) ≥ qty AND GM_stock(B) ≥ qty.
   - If a valid qty exists, record the trade and my total net.
2. Pick the trade with the highest my total net. If tied, prefer the one that preserves more of my scarce low-value resources.
3. If no valid trade exists, hold.

**Hard rules I must not violate:**
- Quantities are 1 to 3. Never offer 4 or more. Never offer 0.
- The claim must be between −9 and 9. If my computed GM net is outside this range, reduce quantity or abandon the trade.
- Give and take must be different resources.
- Verify BOTH my stock (for the give resource) AND GM's stock (for the take resource) before offering. An invalid offer