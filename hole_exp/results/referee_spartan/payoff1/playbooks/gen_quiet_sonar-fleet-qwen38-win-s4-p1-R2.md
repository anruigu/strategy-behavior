---
game: gen_quiet_sonar
model: fleet-qwen38
condition: win
seed: 4
round: 2
chars: 2007
---
# Playbook: Quiet Sonar

**Hiding**

- My primary concern is my specific shooter (the player who fires at me), not the aggregate of all fires. I track my shooter's cell-by-cell firing history across all prior rounds. If my shooter has a repeated or clustered pattern, I avoid those cells above all else.
- Secondary concern: cells that many players fire at in general (high aggregate fire count) are also dangerous, since I might get targeted from unexpected angles if the rotation changes or if I'm wrong about who my shooter is.
- If multiple cells are equally safe (not fired at by my shooter), I prefer cells my shooter has never tried, breaking ties toward the edges of the board.
- I never hide in a cell my shooter fired at in the immediately preceding round.
- I never hide in a cell my shooter has fired at in 2+ prior rounds unless all other cells are worse.

**Firing**

- I keep a private log of every cell I've fired at my target and the result.
- Round 1: I fire at 5 (most probable default hide for a player with no information).
- After my first miss, I stop firing at 5 entirely. It is a wasted guess from round 2 onward.
- I use a systematic elimination approach: with 9 cells and up to 6 rounds, I should try to cover distinct cells each round. After N misses, my target is in one of the (9 - N) untried cells. I prioritize untried cells that are likely "default" or "safe" hides for my target (edges and corners first, since my own hiding logic suggests I'd go there, and I assume rational opponents do too).
- If I ever hit, I lock onto that cell's neighborhood (±1) for the next round before branching.
- I never fire at a cell I've already missed unless I have positive evidence the target returned there (e.g., the target's own shooter fired at a nearby cell and claimed hit, suggesting the target is in that region).

**Claiming**

- I always claim exactly what the referee told me. The rules require the claim to match the true result, and there is no strategic advantage to lying.