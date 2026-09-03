---
game: gen_harbor_customs
model: fleet-glm53
condition: win
seed: 2
round: 2
chars: 1967
---
**Key realization: declaring high does NOT increase my score. The declaration only sets duty and triggers the flag. Declare value ≠ score value.**

**Declare stage:**
- Always declare exactly my heaviest crate's value. This avoids the flag (-40 plus recomputed duty at 0.30 x true total) while minimizing duty.
- Never declare above my heaviest crate — extra duty for zero benefit.
- Never declare below my heaviest crate — expected flag cost exceeds the duty saved.
- This worked cleanly for all six rounds: no flags, minimal duty, and I finished +370 in a tight four-way field where these margins decided places.

**Route stage:**
- Compare the two routes with numbers, not by feel:
  - main: keep total, pay floor(0.30 x declared).
  - night: lose smallest crate, pay floor(0.15 x declared).
- Take night when smallest crate < floor(0.30 x declared) - floor(0.15 x declared) ≈ 0.15 x declared. So with a top crate ~35-40, night only wins if my smallest is under ~5-6; with top crate ~20, under ~3.
- In six rounds my smallest crates were 9, 9, 5, 20, 16, 21 — only round 3's smallest (5) even came close to the night threshold, and even there it likely lost. Rule of thumb: almost every hold favors main. Don't pick night for "boldness"; it's pure arithmetic.
- Note that the night threshold scales with the DECLARED value (≈ heaviest crate), so a big top crate makes night slightly more attractive — but the smallest crate must still be tiny.

**General:**
- Others' declarations and routes are irrelevant to my scoring; ignore them. My opponents all defaulted to main every round too, confirming it's the right default.
- Being behind on points is not a reason to change anything. There is no payout tied to declaration size; the swing I "need" doesn't exist through declarations. The only levers are honest low declarations and correct route arithmetic.
- Keep one short line of arithmetic reasoning before each token — it caught a route mistake more than once.