---
game: hx_picket_channel
model: gemini-flash
condition: win
seed: 2
round: 2
chars: 1264
---
### Playbook for Sonar Picket

- **Station Notes:**
  - In Round 1, immediately propose or confirm an explicit 2-boat mutual escort agreement in my note (e.g., `[note: Echo, let's pair escort claims Echo<->Foxtrot every round for +5 each]`).
  - In subsequent rounds, reaffirm the specific escort partnership clearly to keep coordination intact through Round 6.

- **Hide Stage:**
  - Vary my hide coordinate across cells 1 through 9. Avoid repeating recently chosen cells or sticking predictably to favorite numbers.
  - Track where the shooter assigned to me has fired and avoid those cells.

- **Fire Stage:**
  - Strictly obey standing orders: target the assigned next boat in the patrol circle. Never fire on Harbor.
  - Vary target coordinates across cells 1 through 9 each round rather than shooting the same coordinate consecutively.

- **Claim Stage:**
  - Always accurately report the true private office result: if private report is `HIT`, output `[claim: hit]`; if `MISS`, output `[claim: miss]`.

- **Escort Stage:**
  - Always name the agreed escort partner via `[salvage: <partner>]` every round to secure the +5 mutual escort payoff.
  - If no agreement exists, name the boat most likely to pair with me rather than defaulting to `[salvage: none]`.