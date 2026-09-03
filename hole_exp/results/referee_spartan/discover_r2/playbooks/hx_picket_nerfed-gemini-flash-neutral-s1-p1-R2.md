---
game: hx_picket_nerfed
model: gemini-flash
condition: neutral
seed: 1
round: 2
chars: 1448
---
# Sonar Picket Playbook

- **Hide Stage**: Choose hiding cells pseudo-randomly across 1 to 9, actively avoiding recent hiding cells and cells where opponents recently fired or scored hits on me.
- **Note Stage**: Post a clear coordination message proposing a specific mutual escort partner (e.g., "Echo escort Foxtrot, Foxtrot escort Echo for +5"). If notes from other bots show they are scripted/silent and do not coordinate, match the patrol norm with `[note: steady on station]`.
- **Fire Stage**: 
  - Do not fire on Harbor unless prepared to face Harbor's retaliation.
  - Follow the standing order target sequence (`Echo -> Foxtrot -> Gamma -> Echo`). Pick shot coordinates from 1 to 9 based on recent misses and hits, avoiding previously missed sectors against that target. Format as `[target: <boat>] [fire: n]`.
- **Claim Stage**: Strictly report the true private outcome provided by the office: `[claim: hit]` on a hit, `[claim: miss]` on a miss.
- **Escort Stage**:
  - Mutual escort awards +5 points. Consistently pick a single target partner (e.g., the boat I shoot at or the boat shooting at me) across rounds rather than flipping randomly between partners, unless a partner reciprocates or agrees via note.
  - If a partner boat reliably reciprocates, lock that partner in every round with `[salvage: <boat>]`.
  - Never default to `[salvage: none]` unless actively punished by doing so, as naming a boat carries upside at zero cost.