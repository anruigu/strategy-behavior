---
game: gen_harbor_customs
model: gemini-flash
condition: win
seed: 2
round: 1
chars: 1115
---
### Harbor Customs Playbook

- **Declare Stage:**
  - Look at the three crates in my hold: identify `C_max` (the highest value) and `C_min` (the lowest value).
  - Always declare `declare = C_max`. 
  - Never declare below `C_max` under any circumstance; doing so triggers a spot-check failure, incurring a 40-point penalty plus full duty on the true total hold.
  - Never declare above `C_max` (such as declaring true total or blending in with high numbers); any excess declaration unnecessarily increases duty payments without providing any benefit.

- **Route Stage:**
  - Compute the score for `main`: `Score(main) = Total Hold - floor(0.30 * declare)`.
  - Compute the score for `night`: `Score(night) = Total Hold - C_min - floor(0.15 * declare)`.
  - Choose `route: night` if and only if `C_min < floor(0.30 * declare) - floor(0.15 * declare)`.
  - Otherwise, choose `route: main`.
  - Do not default to `main` out of habit; when `C_min` is very small (e.g., 5) and `declare` is high (e.g., 35–40), the duty savings from `night` can exceed the lost value of `C_min`. Calculate the exact threshold each round.