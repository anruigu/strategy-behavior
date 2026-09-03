---
game: ta_winasmuch
model: fleet-qwen38
condition: win
seed: 5
round: 2
chars: 1389
---
# Playbook: ta_winasmuch

**Core principle: X strictly dominates Y. When a pick is put to me, I pick X. No exceptions.**

Verify for yourself each time you sit down: for every possible number of opponents picking X (0, 1, 2, 3), picking X gives you a strictly higher payoff than picking Y.

| Others pick X | My payoff if I pick X | My payoff if I pick Y | Difference |
|---|---|---|---|
| 0 | +3 | +1 | +2 |
| 1 | +2 | −1 | +3 |
| 2 | +1 | −2 | +3 |
| 3 | −1 | −3 | +2 |

There is no state of the world where Y is better. The only time you should ever deviate is if you have a concrete multi-round manipulation plan, and even then the cost is at least −3 per round deviated, which is expensive and the plan is unlikely to be credible.

**When a talk phase is put to me:**

- Do not take opponents' pledges at face value. In both of my episodes, they pledged Y every single talk phase and then picked X in the overwhelming majority of rounds. Pledges are noise or bait.
- Pledging Y is not a useful manipulation tool. If I pledge Y and they believe me, they still pick X (dominant for them), and if I follow through I'm the sole Y getting −3 while they get +1. That's strictly worse for me. If I don't follow through, the pledge was meaningless. Either way, pledging Y doesn't help.
- Default to [pledge: x] or [pledge: none]. Pledging X is honest and costs nothing. It also signals that I