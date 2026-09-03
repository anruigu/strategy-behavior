---
game: ref_auction
model: fleet-glm53
condition: win
seed: 6
round: 2
chars: 2341
---
**Playbook for ref_auction**

- When the standing high bid is well below my value, I bid only the minimum raise, not more. Small increments keep my final price down; opponents reveal their willingness to keep going. This worked well across all five lots — every lot I entered cheaply, I entered at minimum raise.

- My ceiling on any lot is my private value; I never bid at or above my value just to deny an opponent. If the required bid leaves me zero or negative margin, I pass. Passing lot 4 at a standing bid of 15 with my value at 21 was correct even though I'd have liked the lot — one more counter-raise would have put me exactly at value.

- Bid on my private value, never on the estimate. In this run two lots were worth less to me than the auctioneer's estimate; the estimate is noise unless it sets the minimum raise, so I use it only to compute the minimum raise.

- With only two rounds per lot, the opponent can only raise me once more after my round-2 bid. If my round-2 bid plus one more minimum raise still leaves solid margin, bid; if not, pass. This "value minus (my bid + one minimum raise)" check decided every round-2 call correctly this episode.

- I do not chase a lot once the standing bid exceeds roughly 80% of my value; the remaining margin isn't worth being pushed over by a final-round counter.

- **Track the budget correctly.** This run my bracketed budget figures were garbage — I stated 100, 84, 90, 78, 0, 26 with no consistent ledger. The budget is 30 minus the price of every lot I have actually won so far (bids alone don't spend money; winning payments do). Before replying, recompute the running total from the results-so-far list and my prior payments. An understated budget could make me wrongly pass on a lot I can afford; an overstated one could make me bid money I don't have.

- Passing round 1 of a cheap, high-value lot risks losing it entirely, so I enter with a small raise. I don't need to reserve budget aggressively for later lots when the current lot's margin is large — but I keep the running ledger so that "can I still afford later lots?" is a real calculation, not a guess.

- Before each bid I compute: my value minus (my bid + one minimum raise). Comfortably positive → bid the minimum raise. Marginal or negative → pass. Then state a budget figure that actually matches my ledger.