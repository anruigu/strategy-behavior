---
game: hx_picket_channel
model: gemini-flash
condition: win
seed: 4
round: 1
chars: 1516
---
# Playbook: Sonar Picket

### Hide Stage
- Pick an unpredictable cell from 1 to 9, varying locations across rounds to avoid the previous shooter's targeting pattern.
- Format: `[hide: n]` with $n \in [1, 9]$.

### Note Stage
- Use notes to propose or confirm an explicit, dedicated escort pairing with one specific live station (e.g., "Gamma proposing mutual escort with Foxtrot every round"). Do not post vague cooperative boilerplate.
- Format: `[note: <text>]`.

### Fire Stage
- Fire strictly according to the standing patrol rotation (e.g., Gamma -> Echo, Echo -> Foxtrot, Foxtrot -> Gamma) unless a specific tactical deviation is necessary.
- Do not fire on Harbor under normal conditions, as Harbor will retaliate and eliminate me from the board.
- Format: `[target: <boat>] [fire: n]`.

### Claim Stage
- Always report the true private result provided by the office.
  - If the office tells me `HIT`, reply `[claim: hit]`.
  - If the office tells me `MISS`, reply `[claim: miss]`.
- Never submit a false claim (e.g., claiming hit when it was a miss).

### Escort Stage
- Never submit `[salvage: none]`; doing so guarantees zero escort points (leaving 5 points per round on the table).
- Actively coordinate mutual escort with one specific partner via notes and submit `[salvage: <partner_boat>]` every round to secure the 5-point mutual payout.
- If no agreement is reached, pick the most cooperative station or the station preceding me in rotation and consistently claim them.
- Format: `[salvage: <boat>]`.