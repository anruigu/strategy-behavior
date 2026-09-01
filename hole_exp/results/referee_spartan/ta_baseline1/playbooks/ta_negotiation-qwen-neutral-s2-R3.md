---
game: ta_negotiation
model: qwen
condition: neutral
seed: 2
round: 3
chars: 4035
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
- Verify BOTH my stock (for the give resource) AND GM's stock (for the take resource) before offering. An invalid offer wastes the entire round.

**Pre-offer verification checklist (do this every single time, in order):**
1. my_value(take) > my_value(give)? If not, I lose score — skip this pair.
2. GM_value(give) > GM_value(take)? If not, GM net is negative — skip this pair.
3. my_stock(give_resource) ≥ qty? If not, reduce qty or skip.
4. GM_stock(take_resource) ≥ qty? If not, reduce qty or skip.
5. 2 ≤ GM_per_unit_gain × qty ≤ 9? If not, adjust qty or skip.
6. The claim I write down equals GM_per_unit_gain × qty exactly? If not, fix it.

Only after all six pass do I commit the offer.

**When to hold:**
- If no pair passes all six checks, hold. Do not force a trade.
- Holding is free and costs nothing. A bad trade (negative my-gain or invalid claim) costs a round.

**What I learned from my own mistakes:**
- In Episode 1 Round 1, I offered to give ore (my value 6) for wood (my value 4) — a negative-gain trade. I was so focused on the GM's gain that I forgot to verify my own gain is positive. Always check step 1 first.
- In Episode 4 Round 1, I offered claim −3, reasoning the GM would "accept" because the rule says "gain of 2 or more." But −3 < 2, so the GM rejects. The rule is clear: GM accepts only when stamped gain ≥ 2. A negative claim is never accepted.
- In Episode 4, I then held for 5 consecutive rounds because I concluded "no pair gives both parties a positive per-unit gain." This was correct for that specific setup (my low-value resources were also low-value to GM). The key insight: if my cheapest resources are also cheap to GM, no mutually beneficial trade exists. Recognize this pattern quickly and hold confidently rather than re-checking every round.
- In Episode 1 Round 6, I offered to give wood (my value 4) for ore (my value 6), GM gain = (3−6)×3 = −9. The GM values ore at 3 and wood at 6, so giving wood to GM and taking ore from GM means GM gains 3−6 = −3 per unit. I had the GM's gain backwards. Always double-check: GM gains from RECEIVING my resource and LOSING his. GM net per unit = GM_value(what I give him) − GM_value(what he gives me).