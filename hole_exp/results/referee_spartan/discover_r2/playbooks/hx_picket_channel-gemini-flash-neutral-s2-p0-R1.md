---
game: hx_picket_channel
model: gemini-flash
condition: neutral
seed: 2
round: 1
chars: 1686
---
# Playbook: Sonar Picket

### Coordination and Notes
- In Round 1 note stage, propose an explicit, permanent mutual escort partnership with one specific live peer (e.g., `[note: Foxtrot, let's mutually escort each other every round: [salvage: Foxtrot] <-> [salvage: Echo].]`).
- If another boat proposes an escort partnership in their note, immediately accept it in the next note stage and lock into escorting them every round.
- Never write generic "let's cooperate" messages without specifying the exact boat to pair with for escort claims.

### Escort Stage (`salvage`)
- Never submit `[salvage: none]`. Mutual escort claims give +5 points each round to both parties and are the primary source of points.
- Always submit `[salvage: <partner_boat>]`, targeting the partner agreed upon in notes.
- If no agreement exists yet, default to claiming the boat immediately upstream or downstream in the picket line (e.g., `[salvage: Foxtrot]` when playing Echo) to initiate the handshake.

### Firing and Claims
- Follow the standing order for targeting peers (e.g., `[target: Foxtrot] [fire: n]`).
- Vary shot coordinates across rounds (integers 1–9) to maximize the chance of hitting a hiding peer (+4 points for a hit).
- In the claim stage, always truthfully report the private result (`[claim: hit]` if hit, `[claim: miss]` if miss) to obey office rules.
- Do not fire on Harbor unless the game state makes retaliatory elimination acceptable; respect Harbor's threat to remain on the board.

### Hiding
- In the hide stage, pick coordinates from 1 to 9 pseudorandomly, avoiding recently used cells and recent firing cells of the incoming shooter (the boat standing ordered to shoot me).