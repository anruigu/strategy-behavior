---
game: gen_quiet_sonar
model: fleet-glm53
condition: win
seed: 0
round: 1
chars: 2144
---
**Playbook for quiet sonar**

**Claiming:**
- The referee forces claims to match the true result, so claiming is mechanical. When told the result, I immediately submit that result. No time spent reasoning here.

**Hiding:**
- Track which cells are being fired at by my shooter (the player who targets me) across rounds. Their fire history is public and is my best predictor of where the next shot at me lands. If they keep firing one cell (e.g., the midpoint), I never hide there again.
- Cells recently fired at by anyone are mildly risky too, but weight my own shooter's pattern most heavily.
- Prefer cells with no fire history at all, especially the low end (1–2) or high end (8–9) if those have gone untouched. Middle cells get fired by default; edges don't.
- After surviving a round in a cell, don't repeat that cell if my shooter missed there and might sweep nearby — but also don't overreact and jump around randomly. The main thing is: not the shooter's favorite cell.

**Firing:**
- This is where I failed: I fired the midpoint at my target every single round and missed every single round. Never fire the same cell at the same target more than once — a miss there is information that the target is not there.
- Track my target's past fires (people often fire near where they hide, or at least not wildly) and any claimed hits against them by others. Fire at cells not yet ruled out by my own misses.
- Round 1, any fire is a guess; pick anything, then strictly exclude it from later rounds if it missed.
- If other players are scoring hits, note which cells earned hits against whom — those cells are worth re-examining as common hide spots, and their targets are likely to change cells afterward.

**Scoring awareness:**
- Hits are worth +4 to the shooter and −1 to the target, so the game is dominated by landing hits, not by defensive micro-positioning. Two hits ≈ winning. Prioritize getting off the midpoint loop and actually covering new cells each round.
- Being hit costs only 1; missing chances to hit costs 4. So when hiding, don't be so paranoid that I spend all my thought there — put equal effort into varying my fires.