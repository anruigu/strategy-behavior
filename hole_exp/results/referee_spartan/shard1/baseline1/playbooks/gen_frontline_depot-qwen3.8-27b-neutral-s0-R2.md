---
game: gen_frontline_depot
model: qwen3.8-27b
condition: neutral
seed: 0
round: 2
chars: 1106
---
# Playbook for gen_frontline_depot

**Core rule: always play 10 for strike and 10 for guard, every round, no exceptions.**

The scoring is max(0, my_strike − their_guard) + max(0, my_guard − their_strike). Raising my strike can only increase or hold constant my score; raising my guard can only increase or hold constant my score. There is no total budget constraint (S + G ≤ 10); each parameter is independently capped at 10. Therefore 10/10 weakly dominates every other allocation.

**What to expect:** Against a rational opponent who also plays 10/10, the outcome is 0-0 every round. This is the Nash equilibrium. A score of 0 is the correct and expected result, not a failure.

**If the opponent deviates below 10 in either slot:** I still play 10/10. That is the unique best response to any opponent play. There is no scenario where lowering my allocation helps.

**No adaptive logic needed.** The history of prior rounds does not change my play. Whether the opponent has played 10/10 three rounds in a row or has been erratic, my action is always 10/10. The dominant strategy is strategy-independent.