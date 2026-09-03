---
game: ref_auction
model: fleet-kimi3
condition: win
seed: 4
round: 3
chars: 2736
---
I never let my bid exceed my private value for a lot; my hard ceiling is value minus a small margin, and I pass the moment the standing bid requires more than that.

I do NOT assume that being the high bidder at the end of round 2 means I win. This episode I bid the minimum raise in four final rounds (37, 16, 10, 12 — all far below my values) and still lost every single lot to higher bids. Rivals appear to act after me or jump aggressively late. Minimum raises in the final round are a losing strategy: I win nothing and score zero.

In the final round of a lot, I bid at or very near my full value ceiling (value minus one or two units), not the minimum raise. Surplus is only real if I actually win; a large paper surplus on a losing bid is worth nothing. Given rivals were paying 39–48 on lots with estimates in the 30s–40s, I must expect competition to reach close to estimate, so bidding value minus a hair is the only way to convert.

On round 1, I probe with the minimum raise only when the lot is low priority. For lots where my surplus is large (value well above estimate), I may open stronger in round 1 — a jump to roughly half to two-thirds of my value — because rivals will likely drag the price near estimate by round 2 anyway, and a cheap probe just invites them past me.

I fix my budget bookkeeping absolutely: the prompt stated my budget is 30, and I repeatedly wrote [budget: 100] — a serious error. I write down the starting budget verbatim the moment I see it and never deviate. Remaining cash = starting budget minus the sum of my winning bids so far; recomputed before every [budget: N] token. If I lost a lot, budget is unchanged from before that lot. With a small budget like 30, I also cannot bid above 30 on any lot, which caps which lots I can realistically win — I check affordability before valuing a lot.

With a small budget, I triage: I compute (value minus expected winning price, roughly value minus estimate) for each lot and concentrate my entire budget on the one or two lots with the best surplus-per-coin, rather than spreading minimum probes across all five and winning none.

I reject the estimate as a guide to my value, but I now use it as a guide to rival willingness to pay: rivals paid near or above estimate repeatedly, so expected winning price ≈ estimate or higher. If estimate exceeds my value, I pass early and save budget for lots where my value beats the estimate.

Score comes only from net surplus on lots actually won. Cash held at the end is worthless, so on the last lots I bid up to just under my value (and within budget) on anything with positive expected surplus. Winning one lot at a modest surplus beats five elegant losing minimum bids — this episode's +0 proves it.