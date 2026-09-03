---
game: ref_auction
model: fleet-glm53
condition: win
seed: 5
round: 1
chars: 1489
---
Key lesson: my budget bookkeeping was chaotic — I reported inconsistent leftover budgets (24, 34, 100, 40, 88, 76...) that had no relation to my actual starts and spends. The budget token must track real money: start 30, subtract every winning payment, and never report a number I haven't computed from that ledger. A winning bid at price P reduces my budget by P only if I actually win the lot; bids that lose cost nothing.

Bidding rules:
- When I see a lot, set my ceiling at my private value minus a small margin, and never bid above value.
- Round 1: if standing bid is far below my value, bid minimum raise to stay in cheaply. If standing bid is already near or above my value, pass immediately rather than probing.
- Round 2 (final): this is my last chance. If the standing bid plus minimum raise is still comfortably below my value, bid one minimum raise. If it's within ~20% of my value, weigh passing — rivals often push to near estimate, and thin margins aren't worth the budget drain when later lots may suit me better.
- Don't spend my whole budget on one marginal lot early; there are 5 lots and rivals' values differ from mine, so some lots will come cheap.
- When I've already won a lot, recompute remaining budget before the next bid and size bids to preserve at least enough for one more strong-value opportunity.

If I'm unsure of the budget number, recompute from scratch: initial budget minus sum of my winning payments so far, then subtract the bid I'm about to make.