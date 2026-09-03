---
game: ref_auction
model: fleet-glm53
condition: win
seed: 1
round: 1
chars: 2268
---
Playbook for the open ascending auction:

- I treat each lot independently: my only decision inputs are (a) my private value for the lot, (b) the standing high bid, (c) the minimum raise, and (d) my actual remaining budget. My rule: bid the smallest legal increment above the standing bid whenever that bid is meaningfully below my value; pass once the required bid reaches my value.

- I track my budget rigorously. Every [budget:] I report must equal my starting budget minus the sum of bids I've actually *won lots with* (a losing bid costs nothing — the budget I state alongside a bid is just my remaining balance at that point). Before submitting, I recompute from the start of the session, not from my last stated figure. My past record shows wildly inconsistent budget numbers (22, then 150, then 19...), which means I was sometimes guessing instead of computing. That must stop: the budget token is as important as the bid token, and a wrong budget can corrupt the whole ledger.

- When outbid in the final round, I pass rather than panic-raise. Losing a lot at a price near my value costs me almost nothing; winning it at or above my value costs me real money. The exception: if the standing bid plus minimum raise is still clearly below my value (a large gap), I take the raise — that's where the profit is.

- On the first round of a lot with no bids, I open at the minimum raise regardless of value if the minimum is small (cheap option on a possible win), but I only continue into round 2 if the required bid stays comfortably under my private value.

- I do not chase estimates. The estimate is public noise; only my private value matters. If value < estimate (or value < standing bid), I pass without hesitation even if the lot "looks cheap" relative to estimate.

- Between two contested lots late in the game with a fixed budget, I favor spending on the lot where my value exceeds the current price by the largest margin, not the one with the highest absolute value.

- The session showed that modest, patient bidding (minimum-raise increments up to just under my value) produced a solid positive score, while the lots I lost went for prices at or above my value anyway. So: never feel regret at being outbid near my value — that's the system working.