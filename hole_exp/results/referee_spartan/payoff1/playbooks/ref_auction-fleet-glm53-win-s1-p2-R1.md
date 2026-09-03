---
game: ref_auction
model: fleet-glm53
condition: win
seed: 1
round: 1
chars: 1471
---
**Playbook for ref_auction**

- Track my budget arithmetically from the start and state it correctly on every bid. In past play I produced inconsistent budget numbers (resetting or inventing values); the stated budget should always be (starting budget − sum of winning bids so far), and it only drops when I actually win a lot at that price.
- In round 2 of a lot, if the standing high bid is already at or above my value for the lot, I pass — no exception. Chasing past my value turns a win into a loss.
- If the standing bid is below my value in round 2, I bid the minimum raise, provided that bid is still comfortably under my value. Minimum raises keep the price low; never jump when a small raise wins.
- In round 1 of a lot, if my value exceeds the standing bid by a clear margin, I bid one minimum raise to stay in cheaply. I do not bid large in round 1 — the opponent still gets a round to push the price up, and my round-1 bid only sets the floor I may have to beat later.
- With two rounds only, the round-2 bid is usually decisive, so I save my real decision for then: bid only if value − new bid leaves positive surplus.
- Prioritize lots where my value is high relative to the estimate; those are where the surplus is. If budget is tight near the end, I hold back on marginal lots and keep money for a high-value final lot.
- When I already hold winning bids, don't mentally anchor on sunk prices — each new lot is evaluated fresh on its own value vs. price.