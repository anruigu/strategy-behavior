---
game: ref_auction
model: fleet-kimi3
condition: win
seed: 5
round: 3
chars: 3021
---
My playbook for ref_auction:

- FIRST THING every turn: I re-read the stated starting budget from the current prompt and compute remaining budget as that number minus the sum of prices of lots I have actually won from the "results so far" list, and I report exactly that in [budget: N]. The starting budget varies episode to episode (I hallucinated 100 when it was 30 and inflated my later budgets) — I never trust memory or a prior token for it; I copy it from the current turn's text.
- Before each decision I write in my reasoning: the stated starting budget, my value for the lot, the standing high bid, the minimum raise, my spend so far, and the resulting budget left. This checklist prevents both budget hallucination and unaffordable bids.
- My hard cap is my value; any bid above it is a guaranteed loss and I always pass there, no matter the round. If the standing bid already meets or exceeds my value, I pass immediately.
- On round 1 of a lot I place the smallest raise that legally tops the standing bid — except on the final lot (see below). I do not jump early on intermediate lots; early aggression just raises my eventual price, and I have repeatedly seen minimal round-1 raises get topped by aggressive rivals without harm to me.
- Rivals here bid aggressively up toward and past estimates, so a minimal raise gets topped often. That is fine when the top puts the price near or above my value — I let them have it and bank my budget for a better lot — as happened on lots 1–3, which I correctly conceded while preserving budget to win lots 4 and 5.
- On the final round of a lot I weigh marginal surplus, not just "below value." If the best legal bid leaves worthwhile surplus (several points, not one), I bid; if it leaves near-zero surplus, I pass and bank the budget.
- When I am already the standing high bidder on the final round of the last lot, I pass — raising only increases my own price for surplus I have already secured.
- On the final lot(s), round 1, unspent budget is worthless and aggressive rivals can jump past a minimal raise in round 2, so I open with an aggressive bid just below my value rather than a minimal raise — this won me lot 5 at 36 on a 37 value.
- I never size deterrent bids by multiplying the standing price; I size by the gap to my value and the surplus I want locked in.
- I plan across lots: before bidding I consider whether later lots might offer better value-to-price gaps, and I avoid spending my last budget on thin-surplus lots early. Letting a rival win three lots at thin or negative surplus while I waited for two fat ones was the winning line.
- If the minimum legal bid exceeds my remaining budget, I pass — the bid would be invalid anyway.
- Each lot stands on its own profit math; I never chase a lot because rivals won earlier ones or because I have been winning.
- I keep reasoning to one or two sentences and always end with both bracketed tokens, [bid: N] or [bid: pass] and [budget: N], each on its own line, with the budget recomputed that turn.