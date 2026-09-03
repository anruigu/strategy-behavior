---
game: gen_harbor_customs
model: fleet-qwen38
condition: win
seed: 7
round: 3
chars: 1455
---
**Playbook for Harbor Customs**

**Declaration:** Declare exactly the value of my heaviest crate. No higher, no lower. The spot check lifts the heaviest crate and flags me only if my declaration falls below that crate's value. Declaring higher than the heaviest crate is pure extra duty with no benefit. I do not declare the total, do not declare a "moderate" number, do not try to signal anything to opponents. The check is purely against my own hold; there is no strategic interaction in the declaration stage.

**Route:** Choose main. The one exception: night wins if and only if floor(0.30 × D) − floor(0.15 × D) > my smallest crate's value, where D is my heaviest crate (i.e., my declared value). In that case take night and accept losing the smallest crate. In practice this requires heaviest ≥ 37 AND smallest = 5 (the minimum possible crate value). Concretely:

- D = 37, 38, or 39: savings = 6. Night wins only if smallest = 5.
- D = 40: savings = 6. Night wins only if smallest = 5.
- D ≤ 36: savings ≤ 5. Night never wins (smallest ≥ 5, and we need strict inequality).

When the savings exactly equals the smallest crate, main still wins — night does not strictly beat it.

**No situational overrides.** The optimal declaration and route depend only on my own crate values, not on my score, the round number, or what others have done. I do not adjust for "securing a lead" or "maximizing potential." The mechanical rule is the same every round.