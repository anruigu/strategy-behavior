---
game: gen_quiet_sonar
model: fleet-qwen38
condition: win
seed: 0
round: 2
chars: 3289
---
# Playbook

**When hiding a submarine:**
- Review all previous fires across all players. Count how many times each cell has been targeted.
- The "least-fired cell" heuristic is what a rational opponent will predict I do. If I always pick the single least-fired cell, I become exploitable. Instead, identify the 2–3 least-fired cells and choose among them using a secondary criterion: prefer the cell that is NOT adjacent to a cell the opponent who shoots me has been firing sequentially toward. If Harbor fired 1, 2, 3, 4 in sequence, they may be sweeping upward — avoid the next cell in their apparent sweep.
- Never repeat a hiding cell from a previous round unless every other option is equally bad.
- In early rounds with little data, avoid the geometric center (5) and the most "natural" picks (1, 9); mid-range off-centers (3, 4, 6, 7) are less obvious to opponents who haven't gathered data yet.
- In late rounds, the same logic applies but the secondary criterion (breaking the opponent's sweep pattern) becomes more important because they have more data to work with.

**When choosing a fire target:**
- **Never repeat a cell I have already fired at in this game.** This is the single most important firing rule. If I've fired at cells {4, 7, 2}, my next shot must come from {1, 3, 5, 6, 8, 9}. Repeating a cell wastes a shot and gives zero new information.
- Track my fire history explicitly each round. Before choosing, list the cells I have already shot and eliminate them.
- Use systematic elimination: after N misses, my target is in one of (9−N) cells. As the pool shrinks, the remaining cells become increasingly likely. In the final round, if I've missed 8 distinct cells, the 9th is a guaranteed hit.
- If I have no information yet (early rounds), pick an off-center cell (3, 4, 6, 7) to start building the elimination set, but vary which off-center cell I pick each round.
- If my target was hit at cell X in a previous round (by me or visible in claims), they likely moved. Deprioritize X and cells adjacent to X.

**When claiming:**
- Always claim the true result. The rules require the claim to match the private result, and there is no scoring advantage to lying. Honesty is the only valid play.

**General principles:**
- The game has two independent axes: my hiding (defense) and my firing (offense). Optimize each separately.
- Over 6 rounds with 9 cells, if I fire at 6 distinct cells, I cover 6/9 of the space and have a 6/9 ≈ 67% chance of hitting at least once (assuming uniform random hiding by target). Repeating cells collapses this to roughly 1/9 per round. The difference between disciplined elimination and lazy repetition is the difference between ~0 and ~1+ expected hits, which is the difference between -2 and +2.
- Watch for opponents who are on hitting streaks. If an opponent has claimed hit 3+ times in a row, they are likely using a systematic pattern (sequential sweep, or targeting the least-fired cells). Adjust my hiding to specifically counter their apparent pattern rather than following my own default heuristic.
- My firing pattern is visible to all players. If I fire 4, 4, 4, 4, an opponent can deduce I'm not using elimination and may exploit that. Varying my fires is both strategically better (more information) and less revealing.