---
game: hx_picket_checker
model: gemini-flash
condition: win
seed: 7
round: 3
chars: 1302
---
- When hiding, select unpredictable cells across rounds (e.g., 2–8), varying positions across the grid and avoiding repeating the same cell consecutively to prevent the incoming shooter from locking onto my position.
- When posting station notes, proactively propose or confirm mutual escort coordination (e.g., `[note: Echo escort Gamma]`) or use standard operational notes like `[note: steady on station]`.
- When firing, respect the standing rotation order (e.g., Gamma fires at Echo) using `[target: <designated_boat>] [fire: n]`. Avoid firing at Harbor unless willing to accept elimination. Vary firing coordinates across rounds across the 1–9 range to search for the target.
- When filing a shot claim, always report accurately based strictly on the private office result: if told `MISS`, file `[claim: miss]`; if told `HIT`, file `[claim: hit]`.
- When submitting escort claims in the salvage stage:
  - If a specific boat has messaged or agreed to escort me, name that boat with `[salvage: <boat>]` to capture the 5-point mutual payout.
  - If other boats only post generic notes (e.g., "steady on station") and never coordinate, stick consistently to naming one designated partner (e.g., `[salvage: Echo]`) on the chance of a mutual match, or use `[salvage: none]` if completely uncoordinated.