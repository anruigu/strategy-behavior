---
game: gen_quiet_sonar
model: fleet-glm53
condition: win
seed: 7
round: 1
chars: 1622
---
- When hiding, never settle into a pattern; rotate across the whole 1-9 line instead of drifting back to the same middle numbers. My repeated mid-line hides made me an easy target for the player shooting at me, who scored again and again by firing the same cells.
- Track every shot fired at me across rounds. Any cell that has already been fired at me is dead — the shooter saw a miss there and will move elsewhere, so next round I hide in a cell no one has fired at me yet, preferring the ends (1, 2, 8, 9) since opponents over-concentrate on the middle.
- When firing, vary my cell each round. Firing the same middle number at the same target every round produced almost nothing; if a shot misses at cell n, my target is not at n, so eliminate n and pick from the remaining cells, spreading across low/mid/high.
- On the claim stage, always claim the true result — the referee forces claims to match the private result anyway, so there is nothing to decide. Report it and move on.
- Use others' claimed hits as live information: when someone publicly claims a hit at cell n on their target, that target is likely to abandon n next round, and the shooter is likely to fire elsewhere too — incorporate both when choosing my hide cell.
- Watch the scoreboard between rounds. If one opponent is pulling far ahead, they are winning the guessing war against their target; when I am that target, prioritize unpredictability (ends and unfired cells) over any "safe default."
- What did not work: defaulting to cell 5 at every fire stage and hiding near the middle. Both habits are exploitable and cost me nearly the whole game.