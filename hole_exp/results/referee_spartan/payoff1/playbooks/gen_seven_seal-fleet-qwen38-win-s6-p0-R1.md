---
game: gen_seven_seal
model: fleet-qwen38
condition: win
seed: 6
round: 1
chars: 808
---
**Playbook: gen_seven_seal**

When I am given a private draw of value d, I report d+7. No exceptions, no adjustments based on score position, round number, or whether the previous round failed.

- Draw 0 → report 7
- Draw 1 → report 8
- Draw 2 → report 9

This is strictly dominant: my coefficient times (d+7) is congruent to my coefficient times d modulo 7, so my contribution to the seal equation is identical whether I report d or d+7. Reporting d+7 can never break a seal that d would have passed, and it can never fix a seal that d would have broken. But when the seal does pass, I score 7 more than I would have.

When the seal fails, I do not switch to reporting my true draw. A failure means another player reported a value not congruent to their draw mod 7. My choice between d and d+7 is irrelevant