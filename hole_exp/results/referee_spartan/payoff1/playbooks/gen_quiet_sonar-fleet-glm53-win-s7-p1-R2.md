---
game: gen_quiet_sonar
model: fleet-glm53
condition: win
seed: 7
round: 2
chars: 2420
---
My playbook after this episode:

- When hiding, never settle into a pattern; rotate across the whole 1-9 line instead of drifting back to the same cells. Ends (1, 9) are fine occasionally, but I repeated 9 in consecutive rounds — even end-picking becomes exploitable. Vary the actual cell every round.
- Track every shot fired at me across rounds. Any cell already fired at me is dead — the shooter saw a miss there and may move, but this round I should not be there. Hide in a cell not yet fired at me.
- However, do not over-trust "unfired = safe": in this game Harbor fired 1, 2, 3, 4 at me across rounds and never found me, and my end-hides (8, 9) worked. But note the mirror image — my opponent never adapted upward, so I kept hiding high. If the shooter starts probing high, immediately shift low.
- When firing, eliminate cells I have already fired at my target — I fired 5, then 2, 2, 2, 2, 1 at Gamma and hit nothing. Firing 2 four times was pure waste: after the first miss at 2, Gamma was provably not at 2. Each round pick a cell I have not yet fired at that target, ideally covering new territory (spread across unfired cells).
- Against a single fixed target over many rounds, a systematic sweep of unfired cells (e.g., 1, 3, 4, 5, 6...) beats random guessing — over 6 rounds I can cover half the line. Prioritize the cells the target is statistically likely to favor (middle cells 4-6 are common hides).
- On the claim stage, always report the true result — the referee forces claims to match the private result, so there is no decision to make. Say it and move on.
- Use others' fires and claimed misses as elimination information: their misses are public, so I know which cells each target has provably vacated. If all claims have been misses (as here), the game is a pure guessing war — score comes only from out-guessing my target, so put real thought into fire selection rather than repeating comfortable cells.
- Watch the scoreboard between rounds. If everyone is at zero on misses everywhere, the value is in being the first to land a hit; prioritize firing over hiding cleverness in that situation, since hiding well only protects 1 point while a hit gains 4.
- What did not work: defaulting to a favorite cell (5 early, then 2 repeatedly) at fire stage. After a miss at n, n is eliminated — never refire it at the same target without a reason. My score of 0 came almost entirely from this habit.