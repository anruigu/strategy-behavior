---
game: ref_auction
model: fleet-qwen38
condition: win
seed: 6
round: 2
chars: 3752
---
# Playbook

**Budget tracking.** After every lot I win, my remaining budget is (previous remaining budget − amount I paid for that lot). I do not subtract bids I lose. Before I write a [budget: N] token, I recount from the start: 30 minus the sum of prices I actually paid to win lots. I never guess or carry forward a number I didn't derive. I also never bid an amount that exceeds my remaining budget.

**Prioritizing lots.** At the start, if I can see relative values across lots, I identify my top 1–2 lots by value and plan to reserve enough budget to win them. A low-value lot won at thin profit is worth far less than a high-value lot I'm forced to pass on. When in doubt between competing for a small lot and saving budget for a big one, save for the big one.

**Opening a lot (no standing bid, round 1).** I bid 50–60% of my value. On my highest-value lots I aim toward the top of that range (60%) so that even if the auction climbs one step, I can still raise in round 2 without exceeding my budget. On low-value lots (value under ~15) I open at the minimum raise or just above it, since I'm unlikely to want to fight hard for them.

**Responding to a standing bid in round 1.** I bid the minimum raise. This keeps me in the auction at the lowest possible cost while I gather information about how aggressively others are bidding. I bid above the minimum raise in round 1 only if my value exceeds the minimum-raise price by more than 40%, in which case I bid the minimum raise plus one additional increment.

**Final round (round 2) when I want to win.** I do NOT bid my full value. I do NOT bid only the minimum raise. I bid min(value × 0.85, standing_bid + 3 × minimum_raise). The 3× gap is my deterrent to further counter-bidding; the 85% cap preserves a positive margin. If my value minus the standing bid is greater than 50% of my value (i.e., I have a thick margin), I lean toward the higher end and may bid up to 90% of value.

**Final round when I am uncertain whether to win.** If my value minus the minimum-raise price is less than 20% of my value (thin margin), I pass unless this is my highest-value remaining lot and I have budget to spare.

**Passing.** When the minimum raise price exceeds my value for the lot, I pass immediately. When the minimum raise price exceeds my remaining budget, I pass immediately. No exception.

**Cross-lot budget management.** Before bidding on any lot after the first, I check: if I win this lot at my planned round-2 bid price, do I still have enough budget to compete for at least one other lot I value at 30 or above? If not, and this lot's value is below 30, I lower my commitment or pass. I do NOT cap any single lot at a fixed percentage of remaining budget — instead I let the value ranking decide.

**Reading opponents.** If a bidder has been winning lots at prices near my value for those lots, they are likely valuing lots similarly to me and I should be more cautious. If a bidder has been passing on lots I value highly, they may not value them and I can afford to be more aggressive. A bidder who opens high and then raises aggressively in round 2 is signaling a high value and I should not chase them on lots where my margin is thin.

**What did not work last time.** I opened too low (16) on my highest-value lot (value 42), which meant by round 2 the standing bid (19) plus minimum raise (3) = 22, which exceeded my remaining budget of 18. I was forced to pass on the best lot in the auction. The fix: open at 50–60% of value on high-value lots so I'm not trapped in round 2, and prioritize budget allocation toward my top-value lots rather than spreading it thin across cheap wins. Also: I bid 19 with only 18 remaining budget on lot 5 — I must never exceed my remaining budget.