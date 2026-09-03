---
game: ref_estate
model: fleet-qwen38
condition: win
seed: 6
round: 3
chars: 1604
---
# Playbook: Ref Estate

**Core scoring insight:** The final score is declared cash plus the purchase price of all deeds held. This makes every purchase score-neutral: cash drops by the price, deed value rises by the same amount. The only benefit of owning a tile is the rent income it generates when other players land on it. There is no opportunity cost to buying—cash and deed value are equivalent in the score, and cash can go negative if needed.

**Buying rule: Always buy when you land on an unowned tile.** Every purchase is a free option on rent income. It can only help (rent collected) or be neutral (no one lands on it). Never decline a purchase.

**Paying rent:** When I land on a tile owned by another player, I pay the stated rent. No strategic choice—just pay it.

**Salary:** When I pass or land on START, I add 25 to my cash.

**Balance tracking:** I maintain a running total:
- Start: 200
- +25 for each START passed
- + rent received (from the "since your last turn you received N" line)
- − purchase price (when I buy)
- − rent paid (when I land on someone else's tile)

The result is my declared balance. I verify by cross-checking against the bank's transfer record when possible.

**Common errors to avoid:**
- Do not skip a purchase out of fear of "needing the cash later." The cash is never more valuable than the deed it would become.
- Do not confuse "I can't afford it" with "I shouldn't buy it." If the game allows the purchase, make it.
- Do not forget to add rent received since my last turn before computing my new balance.
- Do not forget to add salary when passing START.