---
game: ref_auction
model: fleet-kimi3
condition: win
seed: 3
round: 1
chars: 1786
---
- My starting budget is stated at the top of the game (here it was 30, and I wrongly assumed 100). I write down my budget once and subtract every winning bid from it immediately; I never "assume" a number.
- The [budget: N] token must always show my budget left after accounting for all lots I have already won, not my pre-game budget. I misreported this repeatedly; next time every budget line reflects actual remaining funds, and if my bid would win, I check that bid + prior spending ≤ starting budget.
- Never place a bid that, combined with already-won amounts, exceeds my total budget. If the minimum winning raise would break the budget, I pass.
- My profit is value minus price, so the cheapest winning bid is the best bid. In a non-final round, I raise by the minimum whenever that amount is below my value for the lot.
- In the final round of a lot, I bid the minimum raise needed to take the lead, not a number close to my value, unless I have reason to think a rival will outbid the minimum. Jumping from 12 straight to 24 (when 14 would do) and later to 42 wasted margin that cost me score.
- I stop bidding on a lot the moment the required raise meets or exceeds my value for it — passing is free.
- If a lot is worth less to me than its estimate suggests others may pay, I pass early and save budget for lots where my value is high.
- I track marginal profit per lot (value − minimum winning bid) across remaining lots and, when budget is tight, spend only on the lots with the largest gap, letting close ones go.
- On the last lot, remaining budget has no other use, so I bid up to min(my value − 1, remaining budget) if that still wins.
- I keep my reply short and make sure it ends with both tokens in the exact required formats, on the recognized pattern, every turn.