---
game: gen_quiet_sonar
model: fleet-qwen38
condition: win
seed: 5
round: 3
chars: 3394
---
# Playbook: Quiet Sonar

## Claiming

- When the referee tells me the true result, I always claim that exact result. No exceptions. A false claim is a rule violation that costs more than the 4 points I'd gain.

## Firing

- I maintain a running list of cells I have already fired at. Each round I pick from the cells I have NOT yet fired at. With 6 rounds and 9 cells, I should always have at least 3 untried options.
- I do not fire the same cell twice unless all other cells have been exhausted. Repeating a fire is a waste of a shot because my target will have learned to avoid it.
- Within the untried set, I prefer cells that are less "obvious" to a rational hider: avoid 5, then 3 and 7, then 4 and 6, then 2 and 8, then 1 and 9. But this is a tiebreaker only — the hard constraint is "untried."
- If I hit my target at cell X in round N, I do NOT fire X in round N+1. They will have moved.
- I track the full public fire and claim history. If my target is being hit by their own hunter at cell Y, that tells me where they hid, not where they will hide next. I use this to confirm my target's tendencies (e.g., do they return to the same region?).

## Hiding

- I maintain a running list of cells my hunter (the player who fires at me) has fired at, from the public history. Each round I hide in a cell they have NOT yet fired at. This is my primary rule.
- With 6 rounds and 9 cells, even if my hunter fires 6 distinct cells, there are 3 cells I can safely hide in. I should almost always be able to avoid being hit.
- If my hunter repeats a cell (e.g., fires 5 three times), that is exploitable: any cell other than 5 is safe that round. I hide in the cell least likely to be their next new target.
- When choosing among safe cells (untried by my hunter), I prefer cells that are also unlikely to be "guessed" by a pattern-seeking hunter. If they've fired 5, 5, 7, their next new cell might be 6 or 8 (adjacent exploration) or 3 (mirror). I avoid those.
- I do NOT hide in a cell where I was hit the previous round, even if it's "safe" by the untried rule, because my hunter may be probing around their hit location.
- In round 1, before I have any fire history, I hide in an extreme cell (1, 2, 8, or 9) because first-round fires cluster on 5 and its neighbors.

## Tracking and Awareness

- Every round, before hiding, I write down: (a) which cells my hunter has fired, (b) which of those I was hit on, (c) which cells remain safe.
- Every round, before firing, I write down: (a) which cells I have fired, (b) which remain untried, (c) whether my target showed any pattern in where they hid (from their hunter's hits).
- I watch cross-player patterns to infer "personalities": a player who hides center every round is predictable; a player who jumps around is harder. I adjust my firing sequence accordingly (e.g., if my target seems random, I just work through untried cells in a fixed order; if they seem to prefer edges, I prioritize center fires).

## Score Awareness

- If I am ahead in points, I can afford to be conservative: hide safely, fire methodically.
- If I am behind (as I often am in this game because the shot cycle makes some players structurally disadvantaged), I still play the same optimal strategy. There is no "desperate" play that helps; the only thing that helps is hitting more and getting hit less, which is exactly what the untried-cell strategy maximizes.