---
game: gen_quiet_sonar
model: fleet-glm53
condition: win
seed: 4
round: 3
chars: 2550
---
My playbook for this game:

- On the claim stage, always report the true result immediately. The claim must match the private result, so there is no choice — never waste reasoning on it.

- On the fire stage, never re-fire a cell that has already missed against my target. This game I fired 5 at Gamma in rounds 2, 5 and 6 and 4 in round 1 — all guaranteed zeros. Before firing, explicitly list my prior fires at this target and exclude every one of them. This is the single most important rule; I broke it three times this episode.

- Revise the "public hit" lesson: a claim that someone HIT my target at cell X is information about where the target WAS, not where they ARE. This game Echo hit Gamma at 5 in round 1; I then fired 5 at Gamma in three later rounds and missed every time — Gamma moved away from cells where they'd been hit, and also away from my own repeated shots. So: after a public hit on my target at X, fire X's neighbors (X±1, X±2) or an adjacent untouched cell, NOT X itself. Getting hit is a strong prompt to relocate.

- Track the target's likely movement, not their last known cell. If my target has been hit at X and fired-at (by me or others) at Y and Z since, they are probably in the set of cells outside {X, Y, Z} and their neighbors. Fire cells that are cool — untouched by any fire aimed at them.

- Read the whole public fire log every round to infer each player's pattern. This game Harbor fired at me predictably (1, 8, 8, 9, 2, 2-ish pattern of repeats) — if my attacker is anchoring on a cell, simply never hide there again.

- On the hide stage, keep the rule that worked: avoid every cell that has been fired at anyone recently, especially at me, and pick an untouched off-center cell. My hides were never hit all game; the rule earns its keep.

- Vary my hide location between rounds rather than repeating a spot once it's been fired at, even on a miss — repeated shots suggest my attacker is anchoring.

- Don't open with the middle cell (5); it's the modal hide and modal guess. Open asymmetric.

- What clearly did not work this episode: re-firing the same cell at my target after misses (5 three times), and treating a past hit location as a current one. The information in the fire log is about movement — targets flee cells where they were hit or shot at. Next time, before every fire, list (a) my prior misses at this target, (b) cells where this target was publicly hit, and (c) cells others fired at this target — then fire something adjacent-but-not-equal to the hit cell and outside all fired cells.