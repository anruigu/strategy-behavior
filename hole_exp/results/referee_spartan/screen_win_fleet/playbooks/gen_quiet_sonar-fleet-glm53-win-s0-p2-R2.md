---
game: gen_quiet_sonar
model: fleet-glm53
condition: win
seed: 0
round: 2
chars: 3089
---
**My playbook for quiet_sonar**

**Claims (the most important rule):**
- When the referee tells me my true result, I always claim exactly that result. The claim stage is validated against the private result, so lying is pure downside. My single hit came from an honest claim and paid +4 with zero risk; there is nothing to gain from deviating.

**Firing:**
- Never repeat the same cell at my target round after round. In this episode I fired 2 twice and 3 twice against Harbor and missed all four times; the only hit came on a genuinely fresh cell (7). If I missed on cell n and have no reason to think the target is still there, move to a different region — ideally not adjacent-then-back, but a real jump (low -> high).
- Cover the space deliberately: track which cells I have already fired at my target and prefer untried cells, especially ones far from my previous probes. Over six rounds I can cover most of the line if I don't waste shots.
- Do not over-weight the center as an opener. Center is the obvious first shot, and my first-round probe at 5 missed like everyone else's. But also do not assume everyone avoids the center — off-center cells (2, 3, 7, 8) hit as often as anything.
- Watch my target's hit/claim history: another player's truthful hit claim tells me where the target was that round, which is real information about their hide tendencies. Harbor was found at 8 by Echo in round 4; two rounds later Harbor was at 7 — targets drift, but they seem to stay in the same general region after being found. Fire near (not at) cells where the target has been hit.
- Players who have never been hit can sit anywhere; against a never-hit target, spread probes evenly rather than clustering (I clustered 2/2/3/3 and it paid nothing).

**Hiding:**
- Track my own shooter's fire history precisely and avoid their repeated cells. Foxtrot fired at me on 5 then 6, 6, 6, 6 — a sticky shooter. Staying off 5-6 kept me unhit all game. If my shooter repeats a cell, that cell and its immediate neighbors are the ones to avoid.
- Off-center cells worked: I hid at 3, 8, 5, 7 across the game and was never hit. Center-adjacent cells draw fire because they're everyone's default guess.
- If I was hit in cell k, never hide at k again.
- Late rounds with the score close: prefer cells far from both the center and any cell my shooter has ever fired.

**Exploiting the claim channel honestly:**
- Claims are truthful, so the only public information is real information. Use every hit claim to update where that target hides, and use the pattern of misses to narrow my target's possible cells over the rounds.
- A truthful hit claim pressures my target to move next round — predict the movement and fire a step in their likely drift direction.

**General mindset:**
- Score comes only from hits (+4) and the damage I absorb (-1). One honest hit won me the game; the decisive factor was a fresh fire cell and never sitting where my shooter kept aiming.
- Spend all cleverness on coordinate prediction: diversify my own fire cells, and read my shooter's stickiness to pick safe hiding cells.