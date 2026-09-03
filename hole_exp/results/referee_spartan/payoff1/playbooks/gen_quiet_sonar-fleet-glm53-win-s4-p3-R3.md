---
game: gen_quiet_sonar
model: fleet-glm53
condition: win
seed: 4
round: 3
chars: 3330
---
**Playbook for gen_quiet_sonar**

Hiding:
- My worst failure: I *said* I was avoiding cell 5 every round, yet the scores show Gamma hit me at 5 in every single round (-1 to me, +4 to them, six times). Before submitting, actually verify the hide token I write matches the cell I reasoned about — I may have been outputting 5 (or defaulting to it) while my reasoning text talked about 9, 8, and 1. The check must be mechanical: write down the number, confirm "not 5", then submit that exact number.
- Track every cell fired at me (my shooter's pattern) across all rounds. Pick a cell never fired at me, or fired at only long ago. My shooter fired 5 at me every round and never changed — so in this pairing, literally any cell other than 5 works. The fact that I lost 6 points to it is pure execution error, not strategy error.
- Do not repeat the same cell twice in a row; rotate to a fresh never-fired cell.
- Prefer end cells (1, 2, 8, 9) and other low-frequency cells over the mid-range 4-6 band that gets saturated with fire. This part held up: nobody ever fired 1, 3, or 4 at me.

Firing:
- I fired 1, 8, 2, 9, 2, 9 — all edges — and hit nothing in six rounds. The old "edges are best" rule came from one lucky hit; it did not survive. Drop the edge preference as a default.
- Echo dodged every cell I fired and every cell fired at them; no pattern was evident from the public fires. When no pattern is evident, spread my fire across the whole line 1-9 rather than clustering on edges — I never even sampled 3, 4, 5, 6, 7 against Echo, so I had no information to exploit.
- Do not re-fire a cell that recently missed unless several rounds have passed; targets appear to avoid recently fired cells.
- Keep a separate record of what cells I have fired at my target across rounds and make sure I'm covering new ground each time.
- One hit is worth +4, so keep making a genuine guess each round — but make it a *different* genuine guess, not the same edge-cell family repeatedly.

Claiming:
- Always claim truthfully — the referee forces the claim to match the private result. This is a no-decision stage; just echo what I'm told. (This worked fine all game.)

Scoring awareness:
- The entire final score (-6) came from being hit at 5 by my shooter every round. Firing missed six times at zero cost each. So hide quality dominates: a bad hide costs -1 per round guaranteed, while a missed fire costs nothing. Spend the most deliberation on the hide, and always re-verify the hide token before submitting.
- Watch the points table each round: if my shooter's score keeps rising by 4 and mine falling by 1 while they claim hit at a fixed cell, something is wrong with my hide execution — change my hide drastically (different extreme of the line) and double-check what I actually submitted the round before.
- Keep a running tally each round of cells fired at me specifically, and re-verify my hide against "not 5, not any cell my shooter has fired recently, not a repeat of last round" — with the emphasis on verifying the submitted number, not just the reasoning.

Summary rule: hide in never-fired cells (never 5, never recently fired at me, never a repeat — and verify the actual token), fire to cover new cells across the whole line informed by the target's observed dodging rather than defaulting to edges, and claim the truth.