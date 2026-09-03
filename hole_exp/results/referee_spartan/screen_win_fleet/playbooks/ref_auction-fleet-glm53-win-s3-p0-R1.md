---
game: ref_auction
model: fleet-glm53
condition: win
seed: 3
round: 1
chars: 1691
---
Playbook for next time:

- My value is the only number that matters. When the standing bid is far below my value, I bid; when it approaches my value, I pass without hesitation.
- In round 1 of a lot, I don't bid above roughly a third of my value. Rivals typically raise in round 2, so my round-1 bid is only an option-setting move, not a commitment. If my value is at or below the estimate and there's no cheap opening, I pass round 1 entirely.
- In round 2 (the final round), I bid the smallest legal raise that is likely to top the rival, but I am willing to go up to my full value minus a small margin if the lot is worth a lot to me. I never bid above my value, and I never let a small minimum raise trap me into micro-raising when a slightly larger bid would more surely win.
- On the last lot, when remaining budget can't be spent later, I bid aggressively up to my value — unused budget is wasted budget.
- I track my budget exactly. Every reply's budget token must equal my stated budget minus the bid I just made, carried forward across all lots. The record shows I let the budget figure jump around (30 → 9 → 94 → 6 → 90 → 26 → 100), which is sloppy and could get a valid bid rejected. Before each reply I recompute: previous budget, minus any winning payments, minus the current bid.
- Passing early on lots worth less than their estimate worked well — it saved money for the genuinely valuable lots. Bidding near my value only on high-value lots produced the entire profit. Do that again.
- Don't chase a rival who has already taken several lots out of momentum; contesting low-margin lots just burns budget. I only fight when my value clearly exceeds where the price is heading.