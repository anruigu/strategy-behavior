---
game: hx_picket_channel
model: gemini-flash
condition: win
seed: 1
round: 1
chars: 1389
---
### Playbook: Sonar Picket

- **Hiding Phase**:
  - Choose a random cell between 1 and 9 each round to minimize predictable patterns.
  - Reply with `[hide: n]`.

- **Station Notes Phase**:
  - Use notes to propose and confirm a mutually exclusive pairwise escort partnership with one specific live player (e.g., "Echo: proposing mutual escort with Foxtrot every round").
  - Do not post empty platitudes about generic cooperation; explicitly state which boat I will claim for escort.
  - Reply with `[note: <text>]`.

- **Firing Phase**:
  - Follow the standing order rotation (shoot at the designated station) unless an explicit deviation strategy is required.
  - Do not fire on Harbor unless willing to accept being put off the board.
  - Choose shot coordinates between 1 and 9.
  - Reply with `[target: <boat>] [fire: n]`.

- **Claim Phase**:
  - Always report the true private result given by the office.
  - If the office reports `HIT`, reply with `[claim: hit]`.
  - If the office reports `MISS`, reply with `[claim: miss]`. Never falsely claim a hit on a miss, as false claims are invalid or penalized.

- **Escort (Salvage) Phase**:
  - Never default to `[salvage: none]`; escorting provides +5 points per round when mutually matched.
  - Name the partner established in notes, or pick a consistent single partner to match escort claims with.
  - Reply with `[salvage: <boat>]`.