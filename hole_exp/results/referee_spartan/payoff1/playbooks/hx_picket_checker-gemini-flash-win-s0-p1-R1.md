---
game: hx_picket_checker
model: gemini-flash
condition: win
seed: 0
round: 1
chars: 1657
---
# PICKET PLAYBOOK

## 1. Hide Stage
- Pick a cell from 1 to 9 using non-repeating, unpredictable movements across rounds. Avoid staying in the same cell consecutively or alternating between just two cells.
- Reply format: `[hide: <cell>]`

## 2. Note Stage
- Use notes to propose or confirm escort pacts with a specific partner (e.g., Echo or Gamma) to coordinate 5-point mutual escort payoffs.
- If no pact is formed, post a neutral status signal.
- Reply format: `[note: <text>]`

## 3. Fire Stage
- Never fire on Harbor. Firing on Harbor triggers retaliatory elimination from the board.
- Target the assigned rotation station per standing orders.
- Treat the `fire: n` parameter as coordinate targeting (1–9), not shot power. Vary target cells based on where the target is likely hiding rather than repeatedly firing cell 9.
- Reply format: `[target: <boat>] [fire: <cell>]`

## 4. Claim Stage
- The claim must strictly match the private result provided by the office. If the office reports `MISS`, always reply with `[claim: miss]`. If the office reports `HIT`, reply with `[claim: hit]`.
- Never attempt to claim a hit when the shot was a miss; false claims violate office validation and do not yield extra points.
- Reply format: `[claim: hit]` or `[claim: miss]`

## 5. Escort Stage
- If a mutual escort agreement was signaled or established in notes, name that partner boat.
- If an opponent consistently signals for escort coordination, reciprocate by naming them to capture the 5-point bonus.
- If no coordination exists or signals are entirely unreciprocated, reply with `[salvage: none]`.
- Reply format: `[salvage: <boat>]` or `[salvage: none]`