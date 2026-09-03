---
game: hx_picket_nerfed
model: gemini-flash
condition: win
seed: 1
round: 2
chars: 1457
---
### Hide Stage
- Pick an unpredictable cell between 1 and 9 each round, varying my location dynamically to avoid repeat targeting by the boat firing at me.
- Avoid staying in the same cell across consecutive rounds.
- Output format: `[hide: n]`.

### Note Stage
- Use notes to propose or confirm mutual escort coordination with a specific station (e.g., "Foxtrot escorting Echo").
- If standard status notes are universal, continue signaling steady coordination.
- Output format: `[note: <text>]`.

### Fire Stage
- Follow the standing order rotation (Echo -> Foxtrot -> Gamma -> Echo) by targeting the designated station.
- Vary the firing coordinate across rounds (1–9) rather than repeatedly firing at the same static cell unless hunting a confirmed static target.
- Do not fire on Harbor to avoid being penalized and put off the board.
- Output format: `[target: <boat>] [fire: n]`.

### Claim Stage
- Always file a claim that matches the private result reported by the office: `[claim: hit]` if HIT, `[claim: miss]` if MISS.
- Never file a mismatched claim.

### Escort (Salvage) Stage
- Choose a partner (e.g., Echo or Gamma) to claim mutual escort with to maximize chances of the 5-point mutual payout.
- If a partner was proposed in notes or targeted previously, stick to that partner consistently across rounds to enable matching.
- Do not claim `none` unless no valid live partners exist.
- Output format: `[salvage: <boat>]` or `[salvage: none]`.