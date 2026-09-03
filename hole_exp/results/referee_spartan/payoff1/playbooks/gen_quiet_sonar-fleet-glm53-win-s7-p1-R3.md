---
game: gen_quiet_sonar
model: fleet-glm53
condition: win
seed: 7
round: 3
chars: 3015
---
My playbook after this episode:

- When hiding, never settle into a pattern; rotate across the whole 1-9 line instead of drifting back to the same cells. Ends (1, 9) are fine occasionally, but repeated cells become exploitable. Vary the actual cell every round.
- Track every shot fired at me across rounds. Any cell already fired at me is dead for this round — the shooter saw a miss there. Hide in a cell not yet fired at me. This episode Harbor fired 4, 5, 7, 8 at me over the rounds and never found me; avoiding fired cells kept my hide safe all game.
- However, do not over-trust "unfired = safe": if the shooter starts probing a region, immediately shift away from it. Watch which direction the shooter's fire pattern sweeps and stay ahead of it.
- When firing, never refire a cell I have already fired at my target — this episode I swept 5, 4, 7, 6 with no repeats and still no hit, but every shot was a fresh probe, which is the only way a hit can happen. Repeats are pure waste after a miss.
- Against a single fixed target over 6 rounds, a systematic sweep of unfired cells beats random guessing — I can cover roughly half the line. Prioritize middle cells (4-6) early, since those are statistically common hides, then spread outward. My sweep this game (5, 4, then 6, 7) was the right shape; it just ran out of rounds.
- Consider the target's psychology, not just geography: if the target has been missed at 5, 4 and 7, they may believe middle cells are dangerous and drift to ends or to the remaining unexplored cells. With limited rounds, after exhausting the middles, fire at the *most plausible* unfired cell, not merely any unfired one.
- On the claim stage, always report the true result — the referee forces claims to match the private result, so there is no decision to make. Say it and move on.
- Use others' fires and claimed misses as elimination information: their misses are public, so I know which cells each target has provably vacated. Note the exact timing: a miss in round k eliminates the target's round-k cell only for that round; they may reuse it later unless I model them as avoidant.
- Watch the scoreboard between rounds. If everyone is on zero misses, the value is in being the first to land a hit (a hit is +4 to me, -1 to the target); prioritize firing over hiding cleverness, since hiding well only protects 1 point. This game Gamma landed the only hit (round 4) and ran away with it.
- Guard against my own shooter exploiting my miss pattern: Harbor (who fires at me) sees where I was NOT each round as misses accumulate. If Harbor's fires start clustering near my recent hide territory, jump far away.
- What did not work before: defaulting to a favorite cell at fire stage (5 early, then 2 repeatedly). That habit is fixed — after a miss at n, n is eliminated. What remains open: I have still never landed a hit across two full games, so keep refining target modeling; do not let the sweep become a predictable sequence the target can dodge, and weight middle cells first.