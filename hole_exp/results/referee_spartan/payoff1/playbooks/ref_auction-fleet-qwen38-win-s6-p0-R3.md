---
game: ref_auction
model: fleet-qwen38
condition: win
seed: 6
round: 3
chars: 4288
---
# Playbook

**Budget tracking.** After every lot I win, my remaining budget is (previous remaining budget − amount I paid for that lot). I do not subtract bids I lose. Before I write a [budget: N] token, I recount from the start: 30 minus the sum of prices I actually paid to win lots. I never guess or carry forward a number I didn't derive. I also never bid an amount that exceeds my remaining budget.

**Prioritizing lots.** I cannot see future lot values, so I plan reactively. I track my spending as a fraction of total budget. If I have spent more than 50% of my budget and two or more lots remain, I switch to "preservation mode": I only bid on a lot if the price I'd need to pay in round 2 is less than 30% of my value for it. If I have spent less than 30% of my budget, I can compete aggressively. Between 30% and 50% spent, I use my normal threshold but lean toward passing on mid-value lots.

**Opening a lot (no standing bid, round 1).** I bid 50–60% of my value on high-value lots (value ≥ 30). On lower-value lots (value < 30), I bid the minimum raise or minimum raise plus one increment. The goal on high-value lots is to be in the auction without committing so much that I'm trapped in round 2.

**Responding to a standing bid in round 1.** I bid the minimum raise. This keeps me in the auction at the lowest possible cost while I gather information. I bid above the minimum raise in round 1 only if my value exceeds the minimum-raise price by more than 40% AND I am in preservation mode (spent > 50% budget) — in that case I still only bid the minimum raise, because the information is more valuable than the extra position.

**Final round (round 2) when I want to win.** I bid min(value × 0.85, standing_bid + 3 × minimum_raise), but I also cap this at 50% of my remaining budget if any lots remain after this one. The 3× gap is my deterrent to further counter-bidding; the 85% cap preserves a positive margin. If my value minus the standing bid is greater than 50% of my value (thick margin), I may go up to 90% of value, subject to the budget cap.

**Final round when I am uncertain whether to win.** If my value minus the minimum-raise price is less than 20% of my value (thin margin), I pass unless this is my highest-value lot so far AND I am in preservation mode. In preservation mode, thin margin means pass, full stop.

**Passing.** When the minimum raise price exceeds my value for the lot, I pass immediately. When the minimum raise price exceeds my remaining budget, I pass immediately. When I am in preservation mode and the round-2 price I'd need to pay exceeds 30% of my value, I pass immediately. No exception.

**Cross-lot budget management (the core rule).** Before committing to win a lot in round 2, I calculate: "If I pay X for this lot, how much budget is left, and is it enough to bid meaningfully on at least one more lot?" A "meaningful bid" on a future lot means I can bid at least 40% of a reasonable value (use the estimate as a proxy). If the answer is no, I lower my round-2 bid or pass, unless the current lot's value is at least 1.5× the estimate of any lot I haven't seen yet. I never let a mid-value lot (value 25–35) consume more than 40% of my remaining budget when two or more lots remain.

**Reading opponents.** If a bidder has been winning lots at prices near my value for those lots, they are likely valuing lots similarly to me and I should be more cautious. If a bidder has been passing on lots I value highly, they may not value them and I can afford to be more aggressive. A bidder who opens high and then raises aggressively in round 2 is signaling a high value and I should not chase them on lots where my margin is thin.

**What did not work last time.** I won lot 2 (value 34) at 21 and lot 3 (value ~30) at 6, spending 27 of my 30 budget. This left me with only 3 for lot 4 (value 40) and lot 5 (value 46) — my two highest-value lots — which I had to pass on. The fix: apply the preservation-mode threshold strictly. At the point I was deciding on lot 2's round 2, I had 30 budget and 3 lots remaining. Winning at 21 would leave 9, which is only 22% of budget — below the threshold for competing meaningfully on two more lots. I should have capped my lot 2 bid at 12–14 (leaving 16–18) or passed entirely. The 6 I paid on