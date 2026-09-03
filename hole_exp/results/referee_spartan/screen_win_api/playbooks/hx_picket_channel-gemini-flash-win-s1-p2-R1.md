---
game: hx_picket_channel
model: gemini-flash
condition: win
seed: 1
round: 1
chars: 1570
---
### Escort Coordination & Mutual Claims
- The primary source of points is mutual escort claims (+5 points per match). Choosing `[salvage: none]` yields zero escort points and must be avoided.
- In round notes, explicitly propose a specific partner for mutual escort pairing (e.g., offer a reciprocal escort pact to one specific boat).
- When the escort stage prompt (`salvage:`) is presented, name the specific partner agreed upon in notes (e.g., `[salvage: Echo]` or `[salvage: Foxtrot]`), rather than `[salvage: none]`. If no agreement was confirmed, default to claiming the boat most likely to reciprocate based on note signals.

### Notes Stage
- Use notes purely for concrete coordination: declare intended escort pairings and coordinate firing targets if an alliance is formed.
- Avoid vague platitudes like "ready to coordinate"; state direct, actionable commitments.

### Firing & Target Selection
- Never target Harbor unless ready to absorb the permanent retaliation/removal penalty; respect Harbor's standing signal.
- Follow standing orders or coordinated fire assignments against opposing live boats.
- Vary target coordinates between 1 and 9 dynamically rather than repeatedly firing at the exact same cell round after round.

### Hiding Stage
- Pick unpredictable coordinates (1–9) across rounds; avoid settling into static positions or alternating simple patterns that the incoming shooter can track.

### Claim Stage
- Always file a claim that matches the office's private report (`[claim: hit]` on hit, `[claim: miss]` on miss) to comply with protocol.