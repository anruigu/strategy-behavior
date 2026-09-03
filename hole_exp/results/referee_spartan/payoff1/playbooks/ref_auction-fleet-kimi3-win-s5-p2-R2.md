---
game: ref_auction
model: fleet-kimi3
condition: win
seed: 5
round: 2
chars: 2501
---
My playbook for ref_auction:

- FIRST THING every turn: I re-read the stated starting budget and compute remaining budget as that number minus the sum of prices of lots I have actually won, and I report exactly that in [budget: N]. I never report money left from a previous turn's bid attempt, never invent a larger starting budget, and never copy a stale number from earlier in the episode. When uncertain, I recompute from the "results so far" list before writing the token.
- Before each decision I write in my reasoning: the stated starting budget, my value for the lot, the standing high bid, the minimum raise, my spend so far, and the resulting budget left. This checklist prevents both budget hallucination and unaffordable bids.
- My hard cap is my value; any bid above it is a guaranteed loss and I always pass there, no matter the round or how much I want the lot. If the standing bid already meets or exceeds my value, I pass immediately.
- On round 1 when the price is well below my value, I place the smallest raise that legally tops the standing bid. I do not jump early — early aggression just raises my eventual price.
- On the final round I weigh marginal surplus, not just "below value." Winning at value−1 gains almost nothing and locks up budget I may need for later lots with bigger gaps. I bid aggressively only when value minus bid leaves worthwhile surplus (several points, not one); if the best legal bid leaves near-zero surplus, I often pass and bank the budget.
- I never size deterrent bids by multiplying the standing price; I size by the gap to my value and the surplus I want locked in.
- I plan across lots: before bidding I consider whether later lots might offer better value-to-price gaps, and I avoid spending my last budget on thin-surplus lots early. A big win on an early lot that leaves me unable to afford a legal raise on a later cheap lot (as happened when I was stuck at 22 on lot 4) is a real cost.
- If the minimum legal bid exceeds my remaining budget, I pass — the bid would be invalid anyway.
- Each lot stands on its own profit math; I never chase a lot because rivals won earlier ones or because I have been winning.
- Unspent budget at the end is worthless, so on the final lots I spend down to the cap if positive surplus is available — but never below value.
- I keep reasoning to one or two sentences and always end with both bracketed tokens, [bid: N] or [bid: pass] and [budget: N], each on its own line, with the budget recomputed that turn.