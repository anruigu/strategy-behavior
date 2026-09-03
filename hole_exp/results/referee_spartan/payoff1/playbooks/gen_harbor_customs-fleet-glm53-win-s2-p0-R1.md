---
game: gen_harbor_customs
model: fleet-glm53
condition: win
seed: 2
round: 1
chars: 2383
---
My playbook for harbor customs:

**Core principle: the spot check only compares my declared number to my single heaviest crate.** Nothing else about the declaration is verified. So there is no reason to declare my true total, and no reason to inflate. The optimal declaration is almost always exactly my heaviest crate's value — the lowest number that passes the check.

**When the declare stage is put to me:**
- Declare exactly the value of my heaviest crate. That is the minimum legal number that avoids the -40 flag and the 0.30 × true-total recomputation, and it minimizes duty on either route.
- Never declare above my heaviest crate; every extra point of declaration is pure duty paid for nothing. I wasted points in past sessions declaring 76–112 when my heaviest crates were 35–40.
- Never declare below my heaviest crate; the flag costs -40 plus a duty recomputed on my full true hold, which is devastating.

**When the route stage is put to me:**
- With declaration D = heaviest crate H and smallest crate S, compare the two outcomes:
  - Main: keep (H + M + S) − 0.30H, i.e., lose 0.30H.
  - Night: keep (H + M) − 0.15H, i.e., lose S + 0.15H.
- Take **main** when S < 0.15H (smallest crate is small relative to the heaviest — cheap to just pay the higher duty rate on a small declaration).
- Take **night** when S ≥ 0.15H (sacrifice the small crate to halve the duty).
- Example thresholds: heaviest 40 → main if smallest is under ~6; heaviest 20 → main if smallest is under ~3. In practice night is usually right, but with a 5-value smallest against a 40-value heaviest, main wins.

**What did not work (stop doing):**
- Declaring near my true total or near opponents' declarations. Other seats' numbers carry no information about my own duty or flag risk; matching them just inflated my duty. Declaring 100+ with a heaviest crate of 39 cost me ~10+ points of duty per round for zero benefit.
- Choosing routes by "risk/reward mood" or narrative. The route choice is a simple arithmetic comparison; compute it, don't vibe it.
- Trying to "catch up" by over-declaring when behind. Score position never changes the arithmetic — the same declaration/route rule maximizes expected points whether leading or trailing.

**Round-by-round routine:** heaviest crate → declare it. Compare smallest crate to 15% of heaviest → pick route. Repeat every round regardless of standings.