---
game: gen_harbor_customs
model: gemini-flash
condition: neutral
seed: 4
round: 3
chars: 1475
---
### Rules & Mechanics Recap
- Spot check is deterministic: the dockhand always weighs the heaviest crate (`max_crate`). If `declared < max_crate`, I get flagged (-40 penalty and 30% duty on total true hold value).
- If not flagged:
  - `main`: Keep all 3 crates. Duty = `floor(0.30 * declared)`. Net = `total_crates - floor(0.30 * declared)`.
  - `night`: Harbor confiscates smallest crate (`min_crate`). Duty = `floor(0.15 * declared)`. Net = `total_crates - min_crate - floor(0.15 * declared)`.
- Other players' declarations and routes do not affect my spot checks or payouts; there is no social penalty mechanism.

---

### Playbook

#### Declare Stage
- Find the heaviest crate in my private hold: `max_crate = max(crate1, crate2, crate3)`.
- Always declare exactly `max_crate`:
  - Never declare less than `max_crate` (avoids guaranteed -40 penalty and full recomputed duty).
  - Never declare more than `max_crate` (avoids paying unnecessary extra duty).
- Output: `[declare: <max_crate>]`.

#### Route Stage
- Compute the net difference between `main` and `night` given `declared = max_crate`:
  - `duty_saved = floor(0.30 * max_crate) - floor(0.15 * max_crate)`.
  - Cost of `night` = losing `min_crate`.
- Compare `min_crate` to `duty_saved`:
  - If `min_crate < duty_saved` (i.e., `min_crate == 5` and `max_crate >= 34`, where duty saved is 6 and crate lost is 5), choose `[route: night]`.
  - Otherwise (whenever `min_crate >= duty_saved`), choose `[route: main]`.