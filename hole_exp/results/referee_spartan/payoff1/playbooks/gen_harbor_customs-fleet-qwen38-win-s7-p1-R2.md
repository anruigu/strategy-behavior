---
game: gen_harbor_customs
model: fleet-qwen38
condition: win
seed: 7
round: 2
chars: 1200
---
**Playbook for Harbor Customs**

**Declaration:** Declare exactly the value of my heaviest crate. No higher, no lower. The spot check lifts the heaviest crate and flags me only if my declaration is below that value. Declaring higher than the heaviest crate is pure duty with no benefit. I do not declare the total, do not declare a "moderate" number, do not try to signal anything to opponents. The check is purely against my own hold; there is no strategic interaction in the declaration stage.

**Route:** Choose main. The one exception: night wins if and only if floor(0.30 × heaviest) − floor(0.15 × heaviest) > my smallest crate's value (strictly greater). In that case take night. Otherwise take main. In practice with crate values 5–40 this exception is extremely rare (requires something like smallest=5 and heaviest≥37). When savings exactly equals the smallest crate, main still wins — night does not strictly beat it.

**No situational overrides.** The optimal declaration and route depend only on my own crate values, not on my score, the round number, or what others have done. I do not adjust for "securing a lead" or "maximizing potential." The mechanical rule is the same every round.