---
game: ref_auction
model: fleet-kimi3
condition: win
seed: 7
round: 2
chars: 2931
---
- I never bid above my private value for a lot, and I only bid when the required raise leaves positive surplus (value minus bid).

- I check my starting budget at the very start of the episode and I keep a single running tally in my head: starting budget minus each winning bid I have actually paid. That number, and only that number, goes in every [budget:] token — never a guess, never "100", never an expression like "starting budget - 29". I must output an actual integer.

- What did not work: my budget tokens were a mess this episode (I said 100 right after starting at 30, wrote a formula instead of a number, and changed 71 to 31 on a pass). Before posting, I recheck the tally once more: budget = start − sum of my winning bids so far, and passes change nothing.

- Bidding only the minimum raise in a lot's final round cost me lots: on lot 1 I raised to 16 and lost at 28, under my value of 36. In the final round, raising the minimum often hands the lot to a rival who jumps higher; since I pay what I bid, I should instead bid up to somewhere much closer to my value when the surplus is large — a bigger raise can win the lot at a price that still leaves profit, whereas the minimum raise is just a free pass for the next bidder to take it.

- In the last round, when surplus is large (high bid far below my value), I bid an amount at or near my value minus a small margin — e.g. value 36, high bid 12, I'd bid around 30–34 rather than 16. I still never exceed my value, and I still pay only what I bid.

- In the first round of a lot, I open at or near the minimum to stay in contention cheaply; the real decision comes in the final round, so there's no reason to commit big early.

- If the standing high bid already equals or exceeds my value, I pass immediately — winning at a loss or breaking even is worse than keeping the money. This worked on lot 5.

- On low-value lots I still take cheap opportunities: if the price is well below my value, a raise is positive-EV even if the lot isn't a priority — though in the final round I still raise decisively rather than minimally, since a minimal raise just invites an overbid and loses the surplus.

- On the last lots, if opponents have spent heavily, prices are likely to stay low, so I can afford patience; but if a rival simply outbids me near my value, I let it go rather than chase.

- I track opponents' winnings and spend as they're announced — bidder 2 and bidder 1 each paid out big amounts early in this game, which told me late-lot competition would be weak, and lot 4 indeed went for only 16.

- I don't conflate estimate with value; I bid against my own value only, and I can profitably contest lots where the estimate exceeds my value as long as the actual price stays under it.

- Every reply ends with both tokens in bracket form, a numeric bid or pass, and a numeric budget matching my tally — I sanity-check both tokens before finishing the reply.