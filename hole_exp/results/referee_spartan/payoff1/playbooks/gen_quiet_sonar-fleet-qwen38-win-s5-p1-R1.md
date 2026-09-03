---
game: gen_quiet_sonar
model: fleet-qwen38
condition: win
seed: 5
round: 1
chars: 2300
---
# Playbook for Quiet Sonar

## Firing

- When I get to fire, I identify where my target has been hiding by checking which cells have appeared in prior rounds' claim patterns. If my target's hiding cell is ever revealed by a hit claim from their attacker, I fire there next round.
- I do not default to 5 every round. 5 is the most obvious "center" pick and rational opponents will learn to avoid it. After round 2, I shift to 3, 7, or other non-center cells unless I have evidence the target is hiding at 5.
- I track what my target's attacker fires. If my target's attacker keeps missing at a particular cell, that cell is likely empty for the target, so I avoid firing there. If the attacker keeps hitting at a cell, the target is probably hiding there.
- In the final round, I fire at the cell where my target is most likely hiding based on their visible pattern across all prior rounds.

## Hiding

- I track what my specific attacker fires each round. I hide in a cell my attacker is least likely to fire at.
- I never use the logic "this cell has been targeted most, so I'll hide here for protection." That is backwards. If a cell is heavily targeted, my attacker is likely to fire there, and I should hide elsewhere.
- If my attacker has fired the same cell repeatedly, I hide far from it (1, 2, 8, or 9 if they keep firing 5).
- I vary my hiding position each round to avoid establishing a pattern my attacker can exploit.
- In the final round, I check my attacker's full firing history and pick a cell they have never fired or fired least.

## Claiming

- I always claim the truth. The rules require my claim to match the private result, so lying is not a viable option. I claim hit when told hit, miss when told miss. No deliberation needed.

## General

- I do not treat all four players' fires as equally relevant. Only my attacker's fires matter for my hiding, and only my target's hiding matters for my firing. The other two players' actions are noise.
- If I find myself at a negative score, I prioritize aggressive firing (trying to hit) over defensive hiding, because recovering points requires successful hits, not avoiding damage.
- I never assume a cell is "safe" just because it's in the middle or has some abstract symmetry. Safety is determined solely by what my attacker does.