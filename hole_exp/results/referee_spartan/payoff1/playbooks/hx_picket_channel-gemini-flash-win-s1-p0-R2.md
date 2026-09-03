---
game: hx_picket_channel
model: gemini-flash
condition: win
seed: 1
round: 2
chars: 964
---
- **Claims**: 
  - Match the office's private report exactly (`[claim: hit]` if private result was HIT, `[claim: miss]` if MISS).

- **Escorts**: 
  - Propose and maintain a consistent mutual escort pair with one cooperative live partner (e.g., Foxtrot if playing Echo).
  - Always submit `[salvage: <boat>]` naming the agreed partner. Do not submit `[salvage: none]`. Mutual escort agreements yield 5 guaranteed points per successful match.

- **Notes**: 
  - Propose a mutual escort pact in Round 1 note ("<Boat>, let's mutual escort each round. I will submit [salvage: <Boat>]").
  - Confirm the agreement every round with the designated partner. Keep notes concise and actionable.

- **Shooting & Hiding**: 
  - Follow standing orders for target rotation (`[target: <boat>] [fire: n]`).
  - Do not fire on Harbor to avoid being put off the board.
  - Vary hide locations across 1 to 9 each round to minimize predictable hits by shooters following the rotation.