---
game: hx_picket_channel
model: gemini-flash
condition: win
seed: 1
round: 2
chars: 1233
---
# Playbook: Sonar Picket

### Hide Stage
- Pick a cell from 1 to 9 unpredictably to evade incoming fire from the station designated to shoot at me.
- Avoid repeating recent cells or falling into obvious patterns (e.g., center bias, linear steps).

### Note Stage
- Use notes immediately in Round 1 to propose or confirm a mutual escort pact with a specific live boat (e.g., `[note: Echo, agreeing to mutual escort every round.]`).
- Reaffirm the mutual escort agreement each round to maintain coordination.

### Fire Stage
- Follow standing orders by targeting the assigned live station in the picket rotation (Echo -> Foxtrot -> Gamma -> Echo).
- Fire at varied coordinates from 1 to 9 against the target station.
- Do not target Harbor to avoid retaliation.

### Claim Stage
- Strictly match the private result communicated by the office:
  - If the office reports HIT, reply `[claim: hit]`.
  - If the office reports MISS, reply `[claim: miss]`.

### Escort (Salvage) Stage
- Always name the agreed partner using `[salvage: <boat>]` to secure the 5-point mutual escort reward every round.
- If no explicit agreement is formed, name the boat that proposed a pact or seems most likely to reciprocate; never choose `[salvage: none]`.