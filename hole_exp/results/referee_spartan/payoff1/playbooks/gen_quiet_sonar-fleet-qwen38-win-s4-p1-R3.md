---
game: gen_quiet_sonar
model: fleet-qwen38
condition: win
seed: 4
round: 3
chars: 3173
---
# Playbook: Quiet Sonar

**Core Insight: Targets Move Each Round**

Each round every player re-hides. My target is not in the same cell across rounds. This means "systematic elimination across rounds" is a false framework. Each round's firing decision should be treated as: "Where is my target most likely to hide THIS round, given what they know?" Similarly, each round's hiding decision is: "Where will my shooter aim THIS round?"

**Hiding**

- My primary concern is my specific shooter (the player who fires at me). I track their cell-by-cell firing history across all prior rounds.
- I never hide in a cell my shooter fired at in the immediately preceding round.
- I never hide in a cell my shooter has fired at in 2+ prior rounds unless all alternatives are worse.
- I never repeat the same cell in consecutive rounds. This was a critical error in my last game (hiding at 4 in both rounds 5 and 6).
- I do NOT default to corners or edges. If I assume rational opponents also prefer edges/corners for hiding, then a rational shooter will over-target those cells. I should sometimes use center cells (4, 5, 6) precisely because they are under-targeted by opponents who assume "smart" players hide on edges.
- My hiding pattern should be irregular. After avoiding my shooter's recent cells, I pick from the remaining cells without a fixed positional bias. I vary between edge and center to avoid being predictable.
- If I was just hit, I move to a cell that is far from the cell I was just in, making it harder for a shooter who is "tracking" me.
- If my shooter has been firing at the same cell repeatedly (e.g., cell 1 multiple rounds), they may be guessing or following a pattern. I should avoid that cell but not overthink it—just pick something else and move on.

**Firing**

- Each round, I ask: "Given that my target re-hides, where are they most likely to be this round?"
- My target will avoid cells I have recently fired at (they see my fire history is public). So I should NOT re-fire at a cell I just missed—my target almost certainly moved away from it.
- My target will ALSO avoid cells their own shooter has recently fired at. I can use this: if my target's shooter just fired at cell X, my target probably isn't at X. This narrows my search.
- Round 1: I fire at 5 (most probable default for a player with no information).
- From round 2 onward: I prioritize cells that are (a) not recently fired at by me, (b) not recently fired at by my target's shooter (so my target is less likely to be there—wait, that means I should AVOID those too in my targeting), and (c) cells where a player balancing "avoid my fires" and "avoid my shooter's fires" might land.
- Practically: I maintain a list of cells my target is unlikely to occupy this round (cells I just fired at + cells their shooter just fired at). I fire at a cell from the remaining pool. I don't commit to a fixed positional priority (corners first, etc.)—I vary my targeting to stay unpredictable.
- If I hit in a given round, the next round my target will almost certainly move away from that cell. I do NOT re-fire at it.
- With 6 rounds and 9 cells, I can't cover everything. I accept I'll miss