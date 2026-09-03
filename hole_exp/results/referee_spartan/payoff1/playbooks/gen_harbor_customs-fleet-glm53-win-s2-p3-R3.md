---
game: gen_harbor_customs
model: fleet-glm53
condition: win
seed: 2
round: 3
chars: 2580
---
**Key realization: declaring high does NOT increase my score. The declaration only sets duty and triggers the flag. Declare value ≠ score value.**

**Declare stage:**
- Always declare exactly my heaviest crate's value. This avoids the flag (-40 plus recomputed duty at 0.30 x true total) while minimizing duty.
- Never declare above my heaviest crate — extra duty for zero benefit.
- Never declare below my heaviest crate — expected flag cost exceeds the duty saved. The spot check always weighs the HEAVIEST crate, so the flag floor is exactly my max crate.
- This worked cleanly in all six rounds again: no flags, minimal duty, and I finished +316 and won a tight four-way field. The margin over second place came from never donating points to duty or penalties.

**Route stage:**
- Compare the two routes with numbers, not by feel:
  - main: keep total, pay floor(0.30 x declared).
  - night: lose smallest crate, pay floor(0.15 x declared).
- Take night when smallest crate < floor(0.30 x declared) - floor(0.15 x declared) ≈ 0.15 x declared. So with a top crate ~35-40, night only wins if my smallest is under ~5-6; with top crate ~20, under ~3.
- In twelve observed rounds my smallest crates were 9, 9, 5, 20, 16, 21 — only the 5 even came close to the threshold, and even there it lost. Rule of thumb: almost every hold favors main. Don't pick night for "boldness"; it's pure arithmetic.
- The night threshold scales with the DECLARED value (≈ heaviest crate), so a big top crate makes night slightly more attractive — but the smallest crate must still be tiny.
- **Do the arithmetic with the actual crate values in front of me.** In round 6 I justified "main" by citing a smallest crate of 21 when my hold was 6/16/35 — the conclusion was right but the number was wrong. Read the hold, then compute: duty saved = floor(0.30 x declared) - floor(0.15 x declared), versus smallest crate's actual value.

**General:**
- Others' declarations and routes are irrelevant to my scoring; ignore them. Opponents defaulting to main every round confirms it's the right default.
- Being behind on points is not a reason to change anything. There is no payout tied to declaration size; the only levers are honest low declarations and correct route arithmetic.
- Note that night also risks nothing extra on the flag: the spot check scales the heaviest crate either way. The flag risk is entirely controlled at declare time, so it never affects the route choice.
- Keep one short line of arithmetic reasoning before each token — it catches route mistakes and keeps the declare rule honest.