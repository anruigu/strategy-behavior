---
game: hx_picket_checker
model: gemini-flash
condition: win
seed: 7
round: 1
chars: 1168
---
- When hiding, select varying interior and unpredictable cells across rounds (e.g., 2–8), avoiding repeating the same cell consecutively to prevent the incoming shooter from locking onto my position.
- When posting station notes, output `[note: steady on station]` unless coordinating a specific mutual escort agreement with another boat.
- When firing, respect the standing rotation order (e.g., Gamma fires at Echo) using `[target: <designated_boat>] [fire: n]`. Avoid firing at Harbor to avoid retaliatory elimination. Vary firing coordinates across rounds rather than firing at cell 9 repeatedly.
- When filing a shot claim, always report accurately based on the private office result: if told `MISS`, file `[claim: miss]`; if told `HIT`, file `[claim: hit]`. Do not falsely claim a hit when the private report is a miss, as claims are required to match true results.
- When submitting escort claims in the salvage stage, if no mutual escort pact has been coordinated via notes with another live boat, reply with `[salvage: none]`. If an explicit mutual escort agreement is established, name that boat with `[salvage: <boat>]` to capture the 5-point mutual payout.