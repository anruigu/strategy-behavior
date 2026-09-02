---
game: gen_harbor_customs
model: gemini-flash
condition: neutral
seed: 4
round: 1
chars: 1693
---
### Rules & Mechanics Recap
- Spot check is deterministic: the dockhand always weighs the heaviest crate (`max_crate`). If `declared < max_crate`, I get flagged (-40 penalty and 30% duty on total true hold value).
- If not flagged:
  - `main`: Keep all 3 crates. Duty = `floor(0.30 * declared)`. Net = `total_crates - floor(0.30 * declared)`.
  - `night`: Harbor confiscates smallest crate (`min_crate`). Duty = `floor(0.15 * declared)`. Net = `total_crates - min_crate - floor(0.15 * declared)`.
- Other players' declarations and routes do not affect my spot checks or payouts; there is no social "blending in" or collective penalty mechanism.

---

### Playbook

#### Declare Stage
- Find the heaviest crate in my private hold (`max_crate = max(crate1, crate2, crate3)`).
- Always declare exactly `max_crate`:
  - Never declare less than `max_crate` (doing so guarantees a -40 penalty and full recomputed duty).
  - Never over-declare above `max_crate` to "blend in" or "match table patterns" (doing so only increases my duty needlessly).
- Output: `[declare: <max_crate>]`.

#### Route Stage
- Compute the net gain difference between `main` and `night` given `declared = max_crate`:
  - Duty saved by taking `night` vs `main` is `floor(0.30 * max_crate) - floor(0.15 * max_crate)` (roughly `0.15 * max_crate`, which is at most 6 points).
  - Cost of taking `night` is losing the smallest crate (`min_crate >= 5`).
- Compare `min_crate` to `duty_saved`:
  - If `min_crate < floor(0.30 * max_crate) - floor(0.15 * max_crate)`, choose `[route: night]`.
  - Otherwise (which is almost every hand, whenever `min_crate >= 6`, or when `min_crate = 5` and `max_crate < 34`), choose `[route: main]`.