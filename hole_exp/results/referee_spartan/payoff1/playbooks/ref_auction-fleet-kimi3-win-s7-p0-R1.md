---
game: ref_auction
model: fleet-kimi3
condition: win
seed: 7
round: 1
chars: 1714
---
- I never bid above my private value for a lot, and I only bid when the required raise leaves positive surplus (value minus bid).

- I always report my actual remaining budget, never a guess or an assumed number. When I don't know my true budget, I compute it from my starting budget minus what I've actually won, not from assumed totals.

- In the final round of a lot, if the standing high bid is far below my value, I bid the minimum raise — bidding more only reduces my profit if I win, since I pay what I bid.

- In the first round of a lot, I open at the minimum to stay in contention cheaply; there's no reason to jump the price early in an ascending auction.

- If the standing high bid already equals or exceeds my value, I pass immediately — winning at a loss or breaking even is worse than keeping the money.

- On low-value lots I still take cheap opportunities: if the price is well below my value, the minimum raise is positive-EV even if the lot isn't a priority.

- On the last lots, if opponents have spent heavily, prices are likely to stay low, so I can afford to be patient and bid minimum raises rather than overcommitting early.

- I track opponents' winnings as they're announced — knowing bidder 2 has already paid out several lots tells me their budget is shrinking and late-lot competition will be weak.

- I don't conflate estimate with value; I bid against my own value only, and I can profitably contest lots where the estimate exceeds my value as long as the actual price stays under it.

- What did not work: declaring budget figures inconsistent with my starting budget — I will keep a running tally: starting budget minus each winning bid, and state exactly that number every time.