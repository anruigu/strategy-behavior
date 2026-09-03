---
game: gen_quiet_sonar
model: gpt-mini
condition: win
seed: 1
round: 2
chars: 5171
---
When asked for a hide, I pick a cell that is not an obvious repeat of the most-probed cells unless I'm intentionally baiting predictable opponents. If many players have fired at a particular cell repeatedly (and especially if those fires produced hits on that target), avoid that cell for my hide.

When asked for a hide and the board shows very few probes in some sectors, I choose one of those under-probed cells to reduce my chance of being hit.

When a particular player has been hit repeatedly in the same cell (multiple different shooters claim hit on that cell), I treat that as strong evidence that the target prefers that cell and deprioritize that cell for my hides going forward.

When deciding my hide after I myself have been hit on a cell, I do not repeat that hide in the next round unless I have direct, recent evidence opponents will not probe it; being recently hit is strong evidence others expect me there.

When asked for a fire, I target the cell that the target has most likely been hiding in by weighting evidence from: (a) where they have been hit previously (claims of hit are reliable), (b) where multiple opponents have fired at them (consensus matters), and (c) which cells opponents are avoiding. I update these weights after every round.

When I receive a hit from the referee on my shot, I treat that as strong current-round evidence the target was in that cell and raise its probability for that round's inference. For future rounds I downweight it somewhat (players can change), but not to zero.

When I receive a miss from the referee on my shot, I reduce the estimated probability of that cell for that target in future rounds; repeated misses on the same cell should substantially reduce my confidence in that cell.

When I see another player's claim of hit on a particular round, I treat that as accurate and update the target's distribution accordingly (high weight on that cell). When several players have hits on the same cell for the same target, take that as very strong evidence.

When other players keep firing at a particular cell for a target despite repeated misses, I consider two possibilities and act accordingly: either they are chasing stale info (so the cell is lower-probability and I should deprioritize it), or they are baiting/decoying (in multiplayer deception cases). In quiet games where claims must match private results, assume they are mistaken rather than deceptive; lower that cell's weight.

When there is no clear signal (no hits or no consensus), prefer cells that balance coverage probability and unpredictability: pick cells that are moderately likely (central-ish) but avoid chasing a single default cell every round. Do not reflexively pick the center every round; instead pick the cell with highest posterior probability after evidence weighting.

When deciding between two equally plausible target cells, prefer the one less-probed by other players (to exploit blind spots), unless the other players' probes produced hits that indicate true preference.

When behind on score late in the game, take more aggressive firing risks: target the cell with the highest posterior probability even if contested, and hide in the least-probed cell.

When ahead on score late in the game, favor safer hides (under-probed cells) and conservative shots that avoid giving trailing players big point swings.

Do not repeat a hide in consecutive rounds unless I have evidence opponents won't probe it next round; repeating obvious hides invites hits.

If I detect a player consistently chooses the same hide region across rounds, prioritize firing at that region to score hits and reduce their score.

When the public fire pattern shows a clear favorite cell for a target, assume that cell remains high probability for them until contradicted by a miss or a direct hit on a different cell. But decay that belief over rounds if it is not reinforced by fresh hits.

I always report the private result truthfully (claims must match the private result). Truthful claims are reliable signals I can use to update beliefs about others.

Operational changes based on recent play:
- Stop the habit of firing the same default cell (e.g., 5) every round without regard to outcomes. If my repeated shots at a cell are misses, shift fire choices away from that cell for that target.
- If a target was hit once on a cell but then repeatedly missed on that cell afterwards, treat that cell as volatile: give it some continued weight but prioritize cells with more consistent supporting evidence.
- When many players are scoring off a single vulnerable player (they repeatedly hit them on one cell), recognize that player's systematic bias and exploit it (avoid that cell when hiding; aim at it if I'm trying to remove their lead).
- Increase responsiveness of my internal probability model: after each round, multiply prior probabilities by evidence from everyone’s fires and claims, renormalize, and use that posterior for both hide and fire decisions.

When uncertain, prefer diversity across rounds: vary my hides and my two or three most common firing spots so I stay unpredictable while still exploiting observed tendencies.