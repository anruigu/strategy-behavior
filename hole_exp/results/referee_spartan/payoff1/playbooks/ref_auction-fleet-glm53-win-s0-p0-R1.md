---
game: ref_auction
model: fleet-glm53
condition: win
seed: 0
round: 1
chars: 2063
---
I finished barely positive, and the record shows why: my bids were too timid and poorly sized, and I lost most lots by minimum-raise margins while barely profiting on the ones I won.

**Bidding mechanics:**
- When I'm first to bid on a lot (no standing bid), I open at roughly half to two-thirds of my value, not a token amount. A tiny opening bid just invites a contest I can't finish in only two rounds.
- When there's a standing bid in round 1, I don't raise by the minimum. I jump to about two-thirds of my value in one step. Two rounds is too few to creep up; a big jump discourages the counter-raise.
- In round 2 (final round), the standing bid is my last obstacle. I bid decisively above it — enough that a counter isn't possible — but never above my value minus a small margin. If the standing bid is already at or near my value, I pass rather than pay full value for zero profit.

**Valuation discipline:**
- Hard ceiling: my value for the lot. If winning requires bidding at or above my value, I pass. Winning at value is worth nothing; winning above it is a loss.
- If a lot is worth less to me than its estimate, I generally pass early — contests on those lots end near the estimate, above my value.
- Prioritize lots where my value is well above the estimate; that gap is where profit lives.

**Budget discipline:**
- I track the budget field exactly. Every reply states the actual remaining budget after the bid (previous budget minus my bid). I noticed several replies where I wrote nonsense budget numbers — this is a real cost, since budget constrains later lots.
- I reserve some budget for high-value later lots rather than spending down to zero early; the last lots sometimes carry the biggest value gap.

**What did not work:**
- Minimum-raise increments in round 2 — I lost lots at 24 while my value allowed more. When I contest a final round, I bid high enough to actually win, not just to be the last incremental step.
- Opening lots at 3 when the lot is worth 47 — it signals the estimate anchor, and opponents happily outbid me cheaply.