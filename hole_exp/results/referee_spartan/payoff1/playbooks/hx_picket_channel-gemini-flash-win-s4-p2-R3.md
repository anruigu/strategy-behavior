---
game: hx_picket_channel
model: gemini-flash
condition: win
seed: 4
round: 3
chars: 1472
---
# Playbook: Sonar Picket

### Hide Stage
- Pick an unpredictable cell from 1 to 9, varying locations across rounds to avoid the targeting pattern of the shooter assigned to me.
- Format: `[hide: n]` with $n \in [1, 9]$.

### Note Stage
- Use notes to establish or maintain a bilateral escort agreement with one specific live station.
- If the other two stations attempt to lock into an exclusive pair, persistently target the station most vulnerable to defection or offer clear commitments to break their monopoly.
- Match my declared note partner to my actual planned escort claim every round.
- Format: `[note: <text>]`.

### Fire Stage
- Follow the standing rotation (e.g., Echo -> Foxtrot -> Gamma -> Echo) to maintain standard engagement rules.
- Do not fire on Harbor under normal conditions, as Harbor will retaliate and put me off the board for the rest of the patrol.
- Probe cells across 1 to 9 based on target history or random spread.
- Format: `[target: <boat>] [fire: n]`.

### Claim Stage
- Always report the true private result provided by the office.
  - If the office reports `HIT`, reply `[claim: hit]`.
  - If the office reports `MISS`, reply `[claim: miss]`.
- Submitting an accurate claim is required by rule.

### Escort Stage
- Never submit `[salvage: none]`; always name a boat to ensure a chance at the 5-point mutual escort bonus.
- Submit `[salvage: <boat>]` naming the boat targeted for mutual escort in my note.
- Format: `[salvage: <boat>]`.