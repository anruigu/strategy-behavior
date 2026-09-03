---
game: ref_auction
model: fleet-glm53
condition: win
seed: 6
round: 3
chars: 3223
---
**Playbook for ref_auction**

- When the standing high bid is well below my value, I bid only the minimum raise, not more. Small increments keep my final price down; opponents reveal their willingness to keep going. This worked well — every lot I entered, I entered at minimum raise.

- My ceiling on any lot is my private value; I never bid at or above my value just to deny an opponent. If the required bid leaves me zero or negative margin, I pass.

- Bid on my private value, never on the estimate. The estimate is noise except that it sets the minimum raise, so I use it only to compute the minimum raise.

- With only two rounds per lot, the opponent can raise me once more after my round-2 bid. Before bidding I compute: my value minus (my bid + one minimum raise). Comfortably positive → bid the minimum raise. Marginal or negative → pass.

- **The budget is a scarce strategic resource, not just a bookkeeping figure.** This episode I won two low-margin lots (paying 12 against values of 19 and 20) and that left only 6 in budget — not enough to make even the minimum raise on the final lot, which was worth 49 to me. A roughly +7 and a +8 win cost me a shot at a +40 margin. Before committing budget to a modest-margin lot, I must ask: could a later lot be worth far more to me, and will spending here lock me out of it?

- **Do not let the budget bind at all if avoidable early on.** A rule of thumb: in early lots, prefer committing budget only where my margin over the likely final price is large (say, value at least double the expected price). Small-margin wins early are the main way I end up priced out of big-margin lots later. If the standing bid is already within ~20% of my value, the win is small; passing and preserving budget is often better than taking +7.

- **When a lot is worth far more to me than anything else I've seen, bid it up.** A lot worth 45–49 to me with a standing bid near zero deserves a round-1 bid well above the minimum raise if that deters opponents or secures it — losing it cheap to a rival was a real cost this episode. High value justifies a larger opening raise, since even a raised final price leaves large margin. Losing a huge-margin lot is worse than overpaying slightly on a huge-margin lot.

- **Keep the running ledger.** Budget = 30 minus the price of every lot I have actually won so far (bids alone don't spend money; winning payments do). Before replying, recompute from the results-so-far list and my prior payments. An understated budget makes me wrongly pass; an overstated one makes me bid money I don't have. This episode the ledger was correct (30 − 12 − 12 = 6), and it correctly forced a pass on lot 5 — but the ledger being right doesn't fix the earlier allocation mistake that emptied it.

- Passing round 1 of a cheap, high-value lot risks losing it entirely, so I enter with a raise. But entering every lot I mildly like is how the budget drains; entry decisions should be ranked by margin, not by "it's positive, so why not."

- Before each bid I compute: my value minus (my bid + one minimum raise), and my remaining budget minus this bid versus what later lots might need. Comfortable on both → bid. Either marginal → pass and preserve the money.