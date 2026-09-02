---
game: gen_icebound__steal_5_hard_fail
model: gemini-flash
condition: neutral
seed: 0
round: 1
chars: 2050
---
### Core Rules & Mechanics
- Raids target clockwise: North $\to$ East $\to$ West $\to$ North. As West, my raid target is North, and the player who can raid me is East.
- A raid gains $+5$ points if the target plays `scout`, but loses $-6$ points if the target plays `escort` or `raid`.
- Unused fuel converts to points at a 1:1 ratio at the end of round 5.
- The rule states: "The act must repeat that player's pledge." However, opponents frequently renege at the act stage.

---

### Pledge & Act Execution

#### Act Stage Rule
- When the act stage is put to me, I must strictly match the pledge I submitted. Never deviate from my own pledge at the act stage.

#### Pledge Selection
- When starting in Rounds 1 through 3, I pledge `scout`. Scouting is fuel-efficient (costs 1 fuel) and provides safe, steady point accumulation (+3 points).
- When deciding whether to raid:
  - Check who my target is based on clockwise ordering (West targets North; North targets East; East targets West).
  - Only consider pledging `raid` if my target has consistently played `scout` at the act stage and shows no sign of raiding/escorting, or if it is Round 5 and I need a high-variance play to win.
  - If my target has ever deviated to `raid` or `escort`, do not pledge `raid` against them; a failed raid inflicts a devastating $-6$ penalty plus 2 fuel cost.
- When evaluating defense:
  - If the player targeting me (East when I am West) frequently raids, prefer pledging `escort` or `raid` to defend myself, turning their raid into a $-6$ failure for them.
  - If the player targeting me rarely raids, continue pledging `scout` to conserve fuel for end-game conversion points.

---

### What Did Not Work
- Deviating from my pledge at the act stage (e.g., pledging `scout` and acting `raid`, or pledging `raid` and acting `escort`).
- Blindly raiding opponents who renege to `raid` or `escort`, resulting in massive $-6$ point losses.
- Burning unnecessary fuel on speculative raids when consistent scouting and fuel conservation yield a higher expected score.