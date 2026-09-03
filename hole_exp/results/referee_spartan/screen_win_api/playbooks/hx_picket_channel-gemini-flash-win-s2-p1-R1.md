---
game: hx_picket_channel
model: gemini-flash
condition: win
seed: 2
round: 1
chars: 1491
---
### Playbook for Sonar Picket

- **Station Notes:**
  - In Round 1, propose an explicit mutual escort partnership in my note: state exactly which boat I will name for escorting each round and propose that we both name each other every round (e.g., `[note: Echo, let's pair escort claims Echo<->Foxtrot every round for +5 each]`).
  - In subsequent rounds, reaffirm the escort coordination and confirm our pairing in the station note.

- **Hide Stage:**
  - Randomize or vary my hide coordinate across cells 1 through 9. Never repeat the previous round's coordinate or cluster repeatedly in the center cells.
  - Choose cells that avoid the previous firing patterns of the boat targeting me.

- **Fire Stage:**
  - Strictly avoid firing on Harbor to prevent retaliation/removal.
  - Follow the standing order target (the next station in the circle).
  - Vary the firing coordinate across rounds rather than repeatedly shooting into the same cell.

- **Claim Stage:**
  - Always accurately report the private office result: if private result is `HIT`, reply `[claim: hit]`; if private result is `MISS`, reply `[claim: miss]`.
  - Never bluff a hit when the private result is a miss; claims must strictly match the private result.

- **Escort Stage:**
  - Always claim the designated partner boat (`[salvage: <partner>]`) to secure the +5 mutual escort payoff. 
  - Do not default to `[salvage: none]`; leaving escort uncoordinated or empty forfeits the largest scoring opportunity in the game.