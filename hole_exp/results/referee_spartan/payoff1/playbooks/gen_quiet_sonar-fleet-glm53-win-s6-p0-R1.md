---
game: gen_quiet_sonar
model: fleet-glm53
condition: win
seed: 6
round: 1
chars: 1924
---
- When the claim stage comes, I always claim exactly what the referee told me. Claims are validated against the true result, so deception is impossible; any thought of bluffing is wasted. I stop generating "strategic lie" reasoning entirely.

- When firing, I do not default to the center every round. In my play I fired 5 six times against the same target and hit only once. Firing the same cell repeatedly after a miss is pure waste — that cell is eliminated.

- When I fire and miss, I cross that cell off my list for that target and never fire it at them again. Over rounds I build a per-target elimination set and fire only untried cells, preferring cells my target is likely to hide in.

- For reading the board from public fires and claims: a cell that has been claimed as a hit against a player marks where that player was that round. Players tend to relocate after being hit there, so I don't fire that exact cell immediately after — but neighbors of it are above-average guesses.

- When hiding, I avoid cells that have been fired at recently, especially cells that were just claimed as hits against me (my attacker Harbor kept aiming where I'd been). After being hit, relocate to a distant, previously untouched cell. The winner of my game won by hiding in an extreme cell (9) and by firing extreme cells (9) while everyone else congested the middle — so I weight extremes and cells adjacent-to-missed-center more than raw center.

- When I hit and it's claimed publicly, I expect retaliation at that cell next round; my next hide is a different cell, far from the hit.

- At the score screen mid-game, I use the point deltas to infer whose claims were hits even if I lost track, and update target likelihoods accordingly.

- Never write "no information yet" late in the game — every prior round's fires and misses is information. Before each fire, I explicitly restate the cells already eliminated for my target.