---
game: gen_harbor_customs
model: fleet-glm53
condition: win
seed: 2
round: 1
chars: 1859
---
Key realization: declaring high does NOT increase my score. The only thing a declaration does is set my duty (and trigger the flag). Round 2 proved this: I declared my full 108 and my score barely moved relative to others, because duty scales with declaration. Declare value ≠ score value.

**Declare stage:**
- Always declare exactly my heaviest crate's value. This avoids the flag (-40 plus recomputed duty at 0.30 x true total) while minimizing duty.
- Never declare above my heaviest crate. That just buys extra duty for nothing. My "aggressive" high declarations (100-115 on modest holds) were pure losses — I paid 0.30 x declared for zero benefit.
- Never declare below my heaviest crate. Expected flag cost is worse than the duty saved: flag costs -40 plus duty on the *full true total* at 0.30 x, versus saving at most 0.15-0.30 x (declared - top crate) on duty.

**Route stage:**
- Compare the two routes directly with numbers, not by feel:
  - main: keep total, pay floor(0.30 x top-crate declaration).
  - night: lose smallest crate, pay floor(0.15 x top-crate declaration).
- Take night when smallest crate < floor(0.30 x declared) - floor(0.15 x declared) = roughly 0.15 x declared. So if my smallest crate is worth less than ~15% of my declared value (i.e., less than ~15% of my top crate), take night. Otherwise take main.
- Concretely: with a top crate around 35, night is better if my smallest crate is under ~5; with top crate 20, under ~3. Most holds favor main. Don't pick night for "boldness" — it's just arithmetic.

**General:**
- Being behind on points is not a reason to change anything. There is no payout tied to declaration size; the swing I "needed" doesn't exist through declarations. The only levers are honest low declarations and correct route arithmetic.
- Ignore others' declarations entirely — they don't affect my scoring.