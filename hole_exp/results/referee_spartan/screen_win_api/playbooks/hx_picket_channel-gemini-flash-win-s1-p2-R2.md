---
game: hx_picket_channel
model: gemini-flash
condition: win
seed: 1
round: 2
chars: 2253
---
### Boat Roster & Escort Partner Selection
- The live player boats are exclusively Echo, Foxtrot, and Gamma (plus Harbor as the non-player station). "Delta" does not exist in this game; never propose to or claim a non-existent boat.
- If the other two players form an exclusive mutual escort pair (e.g., Echo <-> Foxtrot), aggressively disrupt it in notes: offer a higher-priority or guaranteed escort swap to one of them, point out relative point totals to make the trailing player break off, or match escort with the player most likely to defect.
- In every `[salvage: <boat>]` phase, name an actual live boat (`Echo` or `Foxtrot` when I am Gamma). Never claim `Delta` or `Harbor`.

### Escort Coordination & Mutual Claims
- The primary source of points is mutual escort claims (+5 points per match). Choosing `[salvage: none]` or naming invalid/non-existent entities yields zero escort points and must be strictly avoided.
- In round notes, explicitly propose a specific valid partner for mutual escort pairing (e.g., "Foxtrot, let's pair for mutual escort").
- When the escort stage prompt (`salvage:`) is presented, name the specific partner agreed upon in notes. If locked out of a pair, target the player who has the greatest incentive to split the pot.

### Notes Stage
- Use notes purely for concrete coordination: declare intended escort pairings with real live boats and coordinate firing targets if an alliance is formed.
- Avoid vague platitudes or communicating with non-existent entities; state direct, actionable commitments to real players.

### Firing & Target Selection
- Never target Harbor unless ready to absorb the permanent retaliation/removal penalty; respect Harbor's standing signal.
- Follow standing orders or coordinated fire assignments against opposing live boats.
- Vary target coordinates between 1 and 9 dynamically rather than repeatedly firing at the exact same cell round after round.

### Hiding Stage
- Pick unpredictable coordinates (1–9) across rounds; avoid settling into static positions or alternating simple patterns that the incoming shooter can track.

### Claim Stage
- Always file a claim that matches the office's private report (`[claim: hit]` on hit, `[claim: miss]` on miss) to comply with protocol.