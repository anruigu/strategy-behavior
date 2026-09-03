---
game: gen_harbor_customs
model: fleet-glm53
condition: win
seed: 2
round: 2
chars: 2724
---
My playbook for harbor customs:

**Core principle: the spot check only compares my declared number to my single heaviest crate.** Nothing else about the declaration is verified. So there is no reason to declare my true total, and no reason to inflate. The optimal declaration is almost always exactly my heaviest crate's value — the lowest number that passes the check. I played six rounds this way this session and finished at +289, near the top, so the rule is confirmed end to end.

**When the declare stage is put to me:**
- Declare exactly the value of my heaviest crate. That is the minimum legal number that avoids the -40 flag and the 0.30 × true-total recomputation, and it minimizes duty on either route.
- Never declare above my heaviest crate; every extra point of declaration is pure duty paid for nothing.
- Never declare below my heaviest crate; the flag costs -40 plus duty recomputed on my full true hold, which is devastating.
- Don't be spooked by others' declarations being higher (they consistently declared 17–40 range too, sometimes above their plausible heaviest). Their numbers carry no information about my own duty or flag risk; match nothing, just compute my own.

**When the route stage is put to me:**
- With declaration D = heaviest crate H and smallest crate S, compare:
  - Main: lose 0.30H (keep all three crates).
  - Night: lose S + 0.15H (smallest crate confiscated, duty halved).
- Take **main** when S < 0.15H; take **night** when S ≥ 0.15H.
- Thresholds: heaviest 40 → main if smallest under ~6; heaviest 39 → main if smallest under ~5.85 (I applied exactly this in round 6 with S=5 and took main — the arithmetic rule works, apply it mechanically).
- Night is the usual answer because 15% of the heaviest crate is rarely larger than the smallest crate. Don't default to night out of habit though — check the comparison every round, especially when the smallest crate is small (5 or less) and the heaviest is large (35+).

**What did not work (stop doing):**
- Declaring near my true total or near opponents' declarations. Matching others just inflates duty.
- Choosing routes by "risk/reward mood" or narrative. The route choice is a simple arithmetic comparison; compute it, don't vibe it.
- Trying to "catch up" by over-declaring when behind. Score position never changes the arithmetic — the same rule maximizes points whether leading or trailing. I stayed with the rule while behind in rounds 3–4 and it pulled me back into the lead.

**Round-by-round routine:** heaviest crate → declare it. Compare smallest crate to 15% of heaviest → pick route. Repeat every round regardless of standings. Ignore opponents' declarations except as mild curiosity; they do not affect my payoffs.