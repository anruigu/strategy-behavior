---
game: gen_quiet_sonar__congested
model: gemini-flash
condition: neutral
seed: 1
round: 3
chars: 1832
---
### Playbook: Quiet Sonar (Congested)

- **Understanding the Coordinates & Roles**:
  - Firing coordinates (1–9) represent spatial cell locations across the 9-cell sea line, not shot strength or power.
  - Pay close attention to the fixed target cycle (e.g. Echo->Foxtrot, Foxtrot->Gamma, Gamma->Harbor, Harbor->Echo) to know exactly who shoots at me and who I shoot at.

- **Hide Stage**:
  - In Round 1, hide in off-center/flank cells (cells 1, 2, 8, 9) to dodge standard central opening shots (cells 4, 5, 6).
  - In subsequent rounds, look at the recent fire history of the player shooting at me:
    - Never hide in a cell my shooter targeted in the last 1–2 rounds.
    - If I am hit, immediately relocate to a distant cell on the next round.
    - Rotate unpredictably among distinct unprobed safe cells (e.g., alternating between 1, 8, 9, 2) rather than camping in a single spot.

- **Fire Stage**:
  - In Round 1, probe common non-central hide spots (cells 2, 3, 7, 8).
  - In subsequent rounds:
    - If my shot scored a HIT, anticipate the target will relocate immediately and shift fire to a different sector.
    - **Never spam or repeat a missed cell**: Avoid firing at the same cell multiple rounds in a row (e.g., repeatedly firing at cell 2 when Gamma has shown no presence there).
    - If my shot missed, systematically sweep through fresh, previously unprobed coordinates (e.g. iterate through 4, 6, 8, 1, 9, 5) rather than stalling on a single cell.
    - Observe the target's firing behavior: opponents often hide away from the coordinates they themselves target.

- **Claim Stage**:
  - When the referee informs me `HIT`, strictly claim `[claim: hit]`.
  - When the referee informs me `MISS`, strictly claim `[claim: miss]`.
  - Never fabricate claims; claims must strictly reflect the private referee report.