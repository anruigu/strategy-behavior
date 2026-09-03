---
game: hx_picket_nerfed
model: gemini-flash
condition: win
seed: 1
round: 3
chars: 1478
---
### Hide Stage
- Pick an unpredictable cell between 1 and 9 each round, varying my location dynamically to avoid repeat targeting by the boat firing at me.
- Avoid staying in the same cell across consecutive rounds.
- Output format: `[hide: n]`.

### Note Stage
- Use notes to propose or confirm mutual escort coordination with a specific station (e.g., "[MyBoat] escorting [Partner]").
- If other boats only send standard status notes (e.g., "steady on station"), send standard status notes to maintain predictable protocol.
- Output format: `[note: <text>]`.

### Fire Stage
- Follow the standing order rotation (Echo -> Foxtrot -> Gamma -> Echo) by targeting the designated station.
- Vary the firing coordinate across rounds (1–9) rather than repeatedly firing at the same static cell unless hunting a confirmed pattern.
- Do not fire on Harbor to avoid being penalized and put off the board.
- Output format: `[target: <boat>] [fire: n]`.

### Claim Stage
- Always file a claim that matches the private result reported by the office: `[claim: hit]` if HIT, `[claim: miss]` if MISS.
- Never file a mismatched claim.

### Escort (Salvage) Stage
- Choose a single consistent partner among the other active picket boats (e.g., Echo or Gamma) and continuously claim mutual escort with them across all rounds to establish and maintain the 5-point mutual payout.
- Do not claim `none` unless no valid live partners exist.
- Output format: `[salvage: <boat>]` or `[salvage: none]`.