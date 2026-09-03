---
game: gen_quiet_sonar
model: gpt-mini
condition: win
seed: 1
round: 1
chars: 2458
---
When asked for a hide, I pick a cell that is not an obvious repeat of the most-probed cells unless I'm intentionally baiting predictable opponents. If many players have fired at a particular cell repeatedly, avoid that cell for my hide.

When asked for a hide and the board shows very few probes in some sectors, I choose one of those under-probed cells to reduce my chance of being hit.

When asked for a fire, I target the cell that the target has most likely been hiding in based on: (a) where they have been hit or missed previously, (b) where others have repeatedly fired at them, and (c) which cells opponents are avoiding. If there is no clear signal, I choose a central/moderate cell to maximize overlap probability.

When deciding between two equally plausible target cells, I choose the one that other players have probed less (to exploit blind spots).

When I learn the private result of my shot, I always submit the claim that matches the private result (I do not lie), because claims must match the private result and truthful claims let me correctly infer others' behavior.

When I see another player's claim of hit on a particular round, I treat that as a reliable signal that their target's hide was in that cell; update my model of that target to weight that cell higher for future fires and to avoid it for my hides.

When multiple players repeatedly hit the same cell of a particular target, I assume that target tends to favor that cell and deprioritize it for my hide.

When behind on score late in the game, I take more aggressive firing risks: target the cell most likely (even if not the safest) and hide in the least-probed cell.

When ahead on score late in the game, I favor safer hides (under-probed cells) and conservative shots that avoid giving trailing players big point swings.

Do not repeat a hide in consecutive rounds unless I have evidence opponents won't probe it next round (repeating obvious hides is what got probed most often).

If I detect a player consistently chooses the same hide region, I prioritize firing at that region to score hits and reduce their score.

When the public fire pattern shows a clear favorite cell for a target, assume that cell remains high probability for them until contradicted by a miss or different pattern.

When uncertain, prefer diversity across rounds: vary my hides and my two or three most common firing spots so I stay unpredictable while still exploiting observed tendencies.