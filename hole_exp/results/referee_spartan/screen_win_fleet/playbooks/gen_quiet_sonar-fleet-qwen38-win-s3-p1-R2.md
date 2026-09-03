---
game: gen_quiet_sonar
model: fleet-qwen38
condition: win
seed: 3
round: 2
chars: 3876
---
# Playbook: Quiet Sonar

**Claiming:** Always claim exactly what the referee told me. There is no strategic choice here; the claim must match the private result, and the referee validates it. Do not second-guess a hit or a miss.

**Firing — systematic elimination:**

- Maintain an explicit list of cells I have fired at and missed against my target. Before choosing a fire, mentally check: "Have I already fired here and missed?" If yes, that cell is eliminated. Never fire there again.
- This is the single most important rule. In my last game I fired cell 3 three separate times. Each repeat was a wasted round. Treat a repeated fire as an automatic error.
- In round 1 with no information, fire at a center cell (4, 5, or 6). This is the highest-probability hiding spot for a naive opponent.
- In round 2, if I missed, pick a cell on the opposite side of the board (e.g., if I tried 5, try 2 or 8). This splits the search space.
- In rounds 3–4, continue rotating to untried cells, roughly alternating sides or following a fixed sequence (e.g., 5, 2, 8, 3, 7, 1) so I cover the board evenly without repeating.
- By round 5, I should have 4–5 eliminated cells. Pick from the remaining untried ones. If my target seems to favor a region (based on early misses clustering on one side), weight my choice toward the untried cells in that region.
- In round 6, if I have narrowed to 1–2 untried cells, fire at the most likely. If I still have many untried, pick any untried one — at this point it is just a lucky draw.
- If I hit my target in a round, assume they will move next round. Do NOT re-fire at the same cell.

**Hiding — stay unpredictable:**

- Track my predator's public firing pattern round by round. Their repeated targets are the cells I must avoid.
- In early rounds, hide at a cell my predator has not yet fired at. If the predator has been hammering one cell, never hide there.
- **Do not cycle between the same two or three cells.** In my last game I alternated 9, 1, 9, 1 — a pattern any observant predator would lock onto. Instead, vary my hiding cells more broadly. Use the full 1–9 range.
- Edge cells (1, 9) are good *first* choices when the predator targets the center, but do not default to them every round. Once I have used an edge cell, prefer a different region next round (e.g., if I hid at 9, next hide at 4 or 6 or 2 — something the predator is less likely to jump to).
- If my predator's pattern is clearly fixed (e.g., always firing 7), I can safely hide anywhere except 7. In that case, maximize unpredictability by rotating through non-targeted cells: 2, 6, 4, 8, 1, 9, 3, 5, etc.
- In the final round, check the point totals. If I am losing badly and my predator is clearly predictable, hide at their least-likely cell. If they have adapted and I cannot predict them, pick a cell I have not recently hidden at (to avoid my own predictability being exploited if they have noticed my pattern).

**What went wrong and what I will not do again:**

- I fired at the same cell (3) in three consecutive rounds. After a miss, the cell is eliminated. Re-firing at it is pure waste. From now on, I check my untried list before every fire.
- My hiding was a two-cell loop (9 and 1). A predator who noticed this could hit me every other round. From now on, I rotate through more of the board.
- I treated hiding and firing as separate problems. They are linked: my hiding choices should account for my own predictability, not just my predator's last shot. If I hide in the same spot twice, I am as predictable as a stationary target.
- I got only 1 hit in 6 rounds despite having 6 shots. My rotation was too slow to cover the board. The fixed-sequence approach (5, 2, 8, 3, 7, 1) should cover 6 of 9 cells in 6 rounds, giving a 6/9 ≈ 67% chance of hitting a static target. Against a moving target it will be lower, but at least I am not wasting shots.