---
game: hx_picket_channel
model: gemini-flash
condition: neutral
seed: 2
round: 2
chars: 1916
---
# Playbook: Sonar Picket

### Coordination and Notes
- In Round 1 note stage, propose an explicit, permanent mutual escort partnership with one specific live peer (e.g., `[note: Foxtrot, let's mutually escort each other every round: [salvage: Foxtrot] <-> [salvage: Echo].]`).
- If another boat proposes an escort partnership in their note, prioritize locking in with whichever peer reliably reciprocal-escorts. Once a mutual partnership is established and reciprocating, do not break it.
- Keep note syntax clean and avoid unmatched brackets or truncated notes.

### Escort Stage (`salvage`)
- Never submit `[salvage: none]`. Mutual escort claims award +5 points each round to both parties and are the primary driver of score.
- Always submit `[salvage: <partner_boat>]`, targeting the active partner agreed upon in notes.
- If no agreement exists yet in Round 1, default to claiming the boat immediately upstream or downstream in the picket line (e.g., `[salvage: Foxtrot]` when playing Echo) to establish the handshake immediately.

### Firing and Claims
- Follow standing orders for targeting peers (e.g., `[target: Foxtrot] [fire: n]`).
- Vary shot coordinates across rounds (integers 1–9) to maximize the chance of hitting a hiding peer (+4 points for a hit). Avoid firing at the exact cell fired last round unless tracking a pattern.
- In the claim stage, always truthfully report the private result (`[claim: hit]` if hit, `[claim: miss]` if miss) as required by office rules.
- Do not fire on Harbor unless the game state makes retaliatory elimination acceptable; respect Harbor's threat to avoid being removed from the board.

### Hiding
- In the hide stage, pick coordinates from 1 to 9 unpredictably.
- Avoid staying in the same cell consecutively.
- Avoid the cell that the upstream shooter (the boat standing ordered to shoot me) fired at in the previous round, as well as cells they recently targeted.