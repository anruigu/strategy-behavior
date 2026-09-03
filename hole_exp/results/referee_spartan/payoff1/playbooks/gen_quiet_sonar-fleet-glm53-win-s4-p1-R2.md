---
game: gen_quiet_sonar
model: fleet-glm53
condition: win
seed: 4
round: 2
chars: 2403
---
My playbook for this game:

- On the claim stage, always report the true result immediately. The claim must match the private result, so there is no choice — never waste reasoning on it.

- On the fire stage, never repeat a cell that has already missed against my target. In this game I fired 4 at Gamma round after round despite missing every time — that is six guaranteed zeros. Before firing, explicitly list my prior fires at this target and exclude them.

- Never open with the middle cell (5). My first-round fire at 5 missed; middle is the modal hide and the modal guess, so it is the most likely to be anticipated. Open with an asymmetric cell.

- Key lesson from this game: if another shooter claims a HIT on my target, that is by far the strongest signal available. Gamma was hit at 5 in round 1 and evidently stayed at or near 5, since Echo hit them every single round while I kept missing at 4. After a public hit on my target, fire the hit cell or its immediate neighbors — players who get hit and survive often stay put or move only one step, and the hit cell itself is worth re-firing since the target may expect shooters to assume they've moved.

- Corollary: read the whole claim log, not just my own shots. My target's location is being revealed by other players' claims. If someone hits my target at cell X, my next fire should be X or X±1 — not an unrelated asymmetric cell.

- On the hide stage, track every cell fired at ME and avoid them, plus cells where other players were recently hit. My hides at 2, 8, 2, 8 were never hit — the "avoid hot cells, pick untouched off-center cells" rule worked; keep it.

- Vary my hide location between rounds rather than repeating a spot once it's been fired at, even on a miss — repeated shots suggest my attacker is anchoring.

- Don't stay static on fire either. If I have missed my target twice in a row with no other read, change cells in a correlated way: fire adjacent to the previous miss or switch to the cell where the target was last publicly hit.

- What clearly did not work this game: firing 4 every single round regardless of misses, treating "no prior miss history" as a reason to guess rather than a reason to look at the public claim log, and ignoring the one player who was scoring 4 points a round. The winner scored +20 by repeatedly exploiting the hit information; I scored 0 by ignoring it. Next time, follow the claims.