---
game: gen_quiet_sonar
model: fleet-qwen38
condition: win
seed: 4
round: 1
chars: 2600
---
# Playbook: Quiet Sonar

**Hiding**

- When I choose where to hide, I scan the full history of public fires across all players and all prior rounds, count how often each cell was targeted, and pick the cell with the fewest shots fired at it. The most-fired cell is the most dangerous to occupy, not the safest.
- If multiple cells share the minimum fire count, I pick the one farthest from the center of the board, since center cells tend to be convergence points for lazy players.
- I never repeat a hide cell if it was fired at in the immediately preceding round.

**Firing**

- I keep a private log of every cell I've fired at my target and whether I hit or missed. I never fire at a cell that I've already fired at and missed, unless I have a specific reason to think the target returned there (e.g., they hit a cell near it in a later round, suggesting they cluster in a region).
- In the first round I fire at 5 (the most probable default hide). In every subsequent round I fire at a cell I haven't yet tried, prioritizing cells adjacent to any cell where I previously hit (the target may drift locally) and cells in the same half of the board where I last hit.
- If I have hit my target in a prior round, I weight my next fire toward that cell's neighborhood (±1) before branching to untried cells elsewhere.
- I stop firing at the most common "safe" center cell after my first miss there; it becomes a wasted guess every round I repeat it.

**Claiming**

- The rules force me to claim the true result. I always claim exactly what the referee told me. There is no strategic choice here.

**Cross-round tracking**

- Each round I update two tables: (1) a count of shots fired at each cell by every player (for my hide decisions), and (2) my own hit/miss log against my target (for my fire decisions). I never make a decision without consulting both tables first.
- If a round's public fire data reveals that my target is being heavily targeted by their own shooter's predecessor, I note which cells are "hot" for them and avoid hiding there.

**What did not work last time**

- I hid at 5, the single most-fired cell in the game, on two separate occasions. That directly caused me to be hit. I must invert my logic: the most-fired cell is the worst place to hide.
- I fired at 5 in five out of six rounds. After my first miss at 5 I had no reason to keep returning to it, yet I did. Diversification after a miss is mandatory.
- My "balance risk" reasoning was vague and produced a degenerate strategy. Every fire must be justified by either an untried cell or a proximity-to-prior-hit argument.