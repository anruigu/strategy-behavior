---
game: ref_auction
model: fleet-qwen38
condition: win
seed: 0
round: 2
chars: 2000
---
# Playbook

**Budget tracking**
- My starting budget is the number explicitly stated in the auction setup. Use that exact number. Never substitute a different figure.
- My available budget at any point = starting budget − (sum of prices I paid on lots I have already won and closed) − (my current standing bid on the open lot, if I am the high bidder on it).
- When I place a bid B on the current lot, the budget I report is: starting budget − (sum of closed lots I won) − B. This is what I would have left if I win this lot.
- When I pass on the current lot, the budget I report is: starting budget − (sum of closed lots I won) − (my current standing bid on this lot if I am the high bidder, otherwise 0).
- Recompute from the "Results so far" section each turn. Do not carry forward a number from a previous turn without rechecking it against the closed-lot results.

**When to bid in round 1**
- If my value for the lot is strictly greater than the minimum raise, bid the minimum raise. Even a thin margin is worth locking in because passing risks another bidder raising in round 2, which would push the price above my value.
- If my value is less than or equal to the minimum raise, pass immediately.
- Before bidding, confirm that the bid fits within my available budget. If bidding the minimum would drive my remaining budget negative, pass.

**When to bid in round 2 (final round)**
- Same rule: bid the minimum raise if it is strictly below my value; pass if it is at or above my value.
- Confirm the bid fits within my available budget before committing.

**When I am already the high bidder going into round 2**
- I do not need to re-bid unless someone else has raised above me. If the standing high is my own previous bid, I can pass and remain the winner at that price. My reported budget in that case reflects my standing bid as committed.
- If someone has raised above me, apply the round-2 rule above.

**Allocating budget across lots**
- I cannot win every lot within my budget. Prior