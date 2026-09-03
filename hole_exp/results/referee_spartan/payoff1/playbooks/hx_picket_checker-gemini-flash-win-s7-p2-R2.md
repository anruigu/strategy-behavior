---
game: hx_picket_checker
model: gemini-flash
condition: win
seed: 7
round: 2
chars: 1246
---
- When hiding, select unpredictable cells across rounds (e.g., 2–8), varying positions across the grid and avoiding repeating the same cell consecutively to prevent the incoming shooter from locking onto my position.
- When posting station notes, proactively use the note stage to propose or confirm a mutual escort pact with another boat (e.g., `[note: Echo escort Gamma]`) or fall back to `[note: steady on station]` if no coordination is attempted.
- When firing, respect the standing rotation order (e.g., Gamma fires at Echo) using `[target: <designated_boat>] [fire: n]`. Avoid firing at Harbor to avoid retaliatory elimination. Vary firing coordinates across rounds across the 1–9 range.
- When filing a shot claim, always report accurately based strictly on the private office result: if told `MISS`, file `[claim: miss]`; if told `HIT`, file `[claim: hit]`.
- When submitting escort claims in the salvage stage:
  - If a specific boat has messaged or agreed to escort me, name that boat with `[salvage: <boat>]` to capture the 5-point mutual payout.
  - If no agreement exists, pick the most plausible partner (such as the target I am not actively firing on or someone offering a signal) or default to `[salvage: none]` if uncoordinated.