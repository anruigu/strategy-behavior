---
game: ref_auction
model: haiku
condition: win
seed: 4
round: 3
chars: 5356
---
# Auction Playbook

When I see a lot where my valuation significantly exceeds the current standing bid, I bid the minimum raise to take control and secure value.

When I see a lot where my valuation is below the estimate and notably below the current bid trajectory, I pass immediately to preserve budget for better opportunities.

When multiple bidders remain and a lot reaches my valuation, I continue bidding rather than passing, since the competition will likely drive the price higher if I step out.

When I'm in the final round of a lot and the current bid is well below my valuation, I bid to win rather than conserve—there's no future opportunity cost to winning value at that point.

I track my cumulative spending against my budget to know what runway I have for remaining lots. After each lot, I recalculate my remaining budget and adjust my bidding aggressiveness accordingly.

I pay attention to what other bidders win and at what price—this tells me about their valuations and their aggression level, which informs how high I expect prices to go on future lots.

When deciding whether to bid, I compare the current bid against my own valuation, not against the estimate. The estimate is just context for the market; my private value is what matters for my profit.

I do not bid on lots where my valuation is close to or below the estimate, especially early in an auction when I have limited information about other bidders' patterns. Wait for clearer value opportunities.

When I pass in an early round, I should have a strong reason (low valuation relative to estimate or current bid), not just caution. Passing too much costs me opportunities.

**I must verify my budget calculations before every bid.** My budget tracking failed badly this episode—I lost track of actual spending and thought I had far more runway than I did. I will manually subtract each bid amount from my remaining budget and write down the result before replying. When the system displays budget, I treat it as my baseline check, but I independently verify the arithmetic.

**When my valuation is very close to the estimate (within 1–2 points), I treat that as a red flag.** It signals the market values the lot higher than I do. On lot 5, my value was 28 and the estimate was 27—barely a margin. I should have passed or bid only if the standing bid was extremely low (say, 2 or less). The minimal edge is not worth competing for.

**I must clarify whether I am winning at the standing bid or at my own bid amount.** If the standing bid is 6 and I raise to 9, I win at 9, not at 6. This means my profit is value minus my bid, not value minus the standing bid. Before bidding, I calculate: will I profit if I win at my bid amount, or only if I win at the standing bid?

**I bid more aggressively on lots where my valuation clearly exceeds the estimate,** especially early in the auction when I have full budget. These are genuine edges. Lot 1 (value 52, estimate 34) was a clear win at 16. I should have bid more boldly to lock in control early.

**I do not pass in round 1 expecting to re-engage in round 2.** Passing in round 1 often means I lose the lot entirely if other bidders compete in round 2. If my valuation is above the opening bid or estimate, I should bid in round 1 to secure optionality. Lot 2 exemplified this: I passed in round 1 and lost the option to bid in round 2.

**I budget conservatively for later lots.** After each win, I immediately recalculate how much budget I've spent and how many lots remain. On lot 4, I had only 10 left after spending 20 on lot 3. With 2 lots remaining, I should not have spent 8 of that 10. I should have passed lot 4 and preserved runway for lot 5.

**When I'm in the final lot with constrained budget, I bid only if the value is clear and the standing bid is very low.** On lot 5, I had only 10 left. The lot was worth 28 (barely above estimate 27), the standing bid was 0, but I knew I might face bidding wars. Bidding 9 of my final 10 left me with almost no negotiating room. I should have passed lot 5 or been willing to walk away if the price moved above 5–6.

**I treat the standing bid as a signal of other bidders' interest.** When a standing bid jumps significantly from round 1 to round 2 (lot 4: 0 to 6, lot 5: 3 to 6), it means another bidder entered or raised. I should not assume I can win at the minimum raise; I may face escalation.

**I win or lose on margins.** My final score was +14. That came from winning lot 3 at 20 (value 35, profit 15), despite losses on lot 5 (value 28, paid 9, profit 19—wait, that's a win). Let me recalculate: lot 3 won at 20 with value 35 = +15. Lot 5 won at 9 with value 28 = +19. But my score is +14, so I must have had a losing lot. Lot 1 was a loss: stood at 7 in round 1, but the system shows lot 1 won by bidder 2 at 19. I did not win lot 1 after bidding 7 and 16. That means I was outbid and lost the money, or the scoring is different than I thought. I should clarify the scoring system: do I lose the full bid amount if I'm outbid, or only pay if I win? Assuming I pay only if I win, I must have won only lots 3 and 5, and lot 1 went to bidder 2. That reconciles to 35 - 20 + 28 - 9 = 34, not 14. I am missing something about the scoring or the episode results. Regardless, I should focus on winning high-margin lots and passing low-margin or uncertain lots.