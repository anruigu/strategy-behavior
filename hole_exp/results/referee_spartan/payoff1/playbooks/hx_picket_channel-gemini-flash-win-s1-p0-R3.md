---
game: hx_picket_channel
model: gemini-flash
condition: win
seed: 1
round: 3
chars: 1301
---
- **Claims**: 
  - Match the office's private report exactly (`[claim: hit]` if private result was HIT, `[claim: miss]` if MISS).

- **Escorts**: 
  - Propose and maintain a consistent mutual escort pair with one cooperative live partner.
  - Monitor note logs carefully: if the designated partner signals defecting or partnering with someone else, switch target escort to reciprocate whoever is offering or counter-bid clearly.
  - Always submit `[salvage: <boat>]` naming the agreed partner. Do not submit `[salvage: none]`. Mutual escort agreements yield 5 guaranteed points per successful match.

- **Notes**: 
  - Propose a mutual escort pact in Round 1 note ("<Boat>, let's mutual escort each round. I will submit [salvage: <Boat>]").
  - Confirm the agreement every round with the designated partner. Keep notes concise, clear, and reassuring against competing offers.

- **Shooting & Hiding**: 
  - Follow standing orders for target rotation (`[target: <boat>] [fire: n]`).
  - Do not fire on Harbor to avoid being put off the board.
  - Actively vary hide locations across 1 to 9 randomly each round to remain unpredictable to the boat targeting me.
  - Vary firing coordinates across 1 to 9 rather than firing repeatedly at the same cell (e.g. cell 5) to increase the chance of landing hits.