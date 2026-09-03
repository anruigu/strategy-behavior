---
game: gen_quiet_sonar
model: fleet-qwen38
condition: win
seed: 0
round: 1
chars: 2243
---
**Playbook for Quiet Sonar**

**Firing:**
- Never fire at the same cell two rounds in a row. Never default to a "middle" or "balanced" value — that is the most predictable choice and the one other players will expect.
- When I see the public fire list, I identify the cells that are currently "cold" (fired at least once by few or no players this round). I aim at cold cells, because a competent hider will be sitting on a cold cell to avoid detection.
- I keep a running tally of which cells I have already fired at across the game. I avoid repeating a cell unless I have a specific reason to re-check it (e.g., I believe the target moved there).
- I track the specific player I am shooting at. If that player has been targeted heavily at certain cells by others, I infer they will hide away from those cells, and I aim accordingly.

**Hiding:**
- The only player who can hit me is the one who shoots at me (in my seat, that is Harbor). I track Harbor's previous fires specifically and hide in a cell Harbor has not recently fired at.
- I also avoid cells that are broadly popular targets across all players, because if Harbor is reading the same public data I am, Harbor will be aiming at the obvious "safe" spots.
- I do not repeat a hide cell across consecutive rounds. If I was at 1 last round, I move.
- I avoid cells that I myself fired at recently, because other players who are reading my fire history will expect me to hide where I am not looking.

**Claiming:**
- I always claim the true result. A false claim is invalid or penalized; there is no strategic gain from lying. This is not a judgment call — it is a fixed rule.

**What did not work:**
- Firing at the same "balanced middle" cell every single round produced almost no hits. It is the worst possible strategy because it is fully predictable and because smart hiders will specifically avoid the obvious center. I must rotate my shots and use the public data to pick cells where the target is likely to be sitting, not where I feel "safe" aiming.
- Treating all public fire data as equally relevant was a mistake. I should weight the data by *who* is firing: the player shooting at me matters most for my hide, and the general pattern matters for where my target will hide.