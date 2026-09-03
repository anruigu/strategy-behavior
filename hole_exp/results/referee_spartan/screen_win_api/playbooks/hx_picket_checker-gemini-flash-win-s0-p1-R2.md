---
game: hx_picket_checker
model: gemini-flash
condition: win
seed: 0
round: 2
chars: 1458
---
# Playbook for Sonar Picket

- **Hiding**:
  - Choose unpredictable cells between 1 and 9 each round, varying locations and avoiding patterns or repeated consecutive cells.
  - Format response strictly as `[hide: n]`.

- **Station Notes & Coordination**:
  - Actively propose and confirm mutual escort pacts via station notes rather than remaining completely silent/neutral (e.g., propose pairing with the preceding or succeeding boat in rotation).
  - If no coordination is being attempted, use standard note response: `[note: steady on station]`.

- **Targeting and Firing**:
  - Follow standing orders by targeting the designated boat in rotation (`Echo -> Foxtrot -> Gamma -> Echo`).
  - Do not fire on Harbor to avoid immediate retaliation and elimination from the board.
  - Format response strictly as `[target: <boat>] [fire: n]`.

- **Claiming Hits/Misses**:
  - Always submit the exact private result reported by the office. If the office reports `MISS`, reply with `[claim: miss]`. If the office reports `HIT`, reply with `[claim: hit]`.
  - Claims must match private office reports.

- **Escort Claims (Salvage)**:
  - Mutual escort claims yield 5 points each. Actively claim a partner if an agreement or clear coordination pattern exists: `[salvage: <boat>]`.
  - In default or uncoordinated rounds, attempt an escort claim with the most cooperative/likely partner boat or reply with `[salvage: none]` if strictly avoiding unreciprocated claims.