---
game: gen_quiet_sonar
model: fleet-qwen38
condition: win
seed: 7
round: 1
chars: 2032
---
# Playbook: Quiet Sonar

**Hiding**

- When choosing a hide cell, scan all previous public fire coordinates. Avoid any cell that has been fired at even once, especially cells fired at multiple times.
- Prefer cells that no one has shot at. If multiple are available, pick one that is far from the cluster of common targets.
- Never hide in a cell you can see has been a popular default (like 5). If you were hit there, move immediately.
- If I've been hit in a round, next round I must hide somewhere opponents haven't targeted. Do not stay put.

**Firing**

- Never default to a single cell every round. If I fired at cell X last round and missed, I must try a different cell this round.
- Track my target's likely positions. If I hit them at a cell, they will likely move next round. Fire at cells adjacent to where I last hit them, or spread out.
- If my target has been scoring points (claiming hits on others), they are actively playing and likely rotating positions. Try cells they haven't been shot at, since those are where they might hide.
- Build a mental model: cells where my target has been hit are now unlikely. Cells they've never been hit at are candidate hide spots. Prioritize firing at those.
- In the final round, if I can narrow my target to 2-3 likely cells based on the elimination of where they've been hit, fire at the most likely remaining one.

**Claims**

- Always claim exactly what the referee told me. The rules require claims to match the private result, so lying is invalid and risks disqualification or penalty. There is no strategic reason to lie.

**General**

- The game is a race between my ability to hit my target and my ability to avoid being hit. Both require tracking public fire history.
- I lose 1 point when hit, gain 4 when I hit. Net expected value of firing at a random cell is 4/9 - 1/9 = 3/9 per round. Adapting my aim above random gives me an edge.
- Do not treat each round independently. Every fire coordinate revealed is information I should use both for hiding and for aiming.