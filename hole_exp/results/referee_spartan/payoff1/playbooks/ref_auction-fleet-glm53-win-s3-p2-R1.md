---
game: ref_auction
model: fleet-glm53
condition: win
seed: 3
round: 1
chars: 1514
---
**Playbook for open ascending auctions with private values**

- When I hold the standing high bid, I pass. Never bid against myself; my own bid already stands.

- When the standing high bid is well below my value, I bid the minimum raise rather than jumping. Small increments keep the final price low and leave the rival to reveal their limit.

- My cap on any lot is my private value minus a margin. I never bid at or above my value; if a rival's bid exceeds my value, I pass immediately and without regret.

- I track my remaining budget exactly and never let a bid's stated budget drift or reset. The budget I state must always equal my previous budget minus my total outstanding winning bids and current commitments. Sloppy bookkeeping risks overcommitting or appearing to have more/less than I do.

- Early in the sequence, I preserve budget for later lots, since I don't know future values. With many lots remaining and a full budget, I can be more aggressive on high-value lots; with most of my budget spent, I only chase lots where value far exceeds the current price.

- If a lot is worth less to me than the current standing bid (or even the estimate), I pass from the start — no speculative small bids on low-value lots.

- Each lot ends after two rounds, so round 2 is my last chance: if the standing bid is still under my value at round 2, I raise once (minimally) and then accept the outcome.

- My aim is total surplus, not winning count: winning one high-margin lot beats winning several thin ones.