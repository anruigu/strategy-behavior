---
game: gen_quiet_sonar__congested
model: gemini-flash
condition: neutral
seed: 1
round: 1
chars: 1714
---
### Playbook: Quiet Sonar (Congested)

- **Understanding the Coordinates**:
  - Remind myself that firing coordinates (1–9) represent sea locations, not "attack power" or "damage level".
  - Firing at cell 9 is not a "maximum power" shot; it is simply guessing cell 9.

- **Hide Stage**:
  - In Round 1, hide on the edges or off-center (cells 1, 2, 8, or 9) to avoid the natural tendency of opponents to target central cells (4, 5, 6).
  - In subsequent rounds, review the shooter targeting me (the player immediately preceding me in the loop):
    - Identify which cells they have fired at recently.
    - Avoid cells they frequently target.
    - If my shooter is stuck targeting central clusters (4–7), keep hiding in quiet peripheral cells (e.g., 2, 3, 8).
    - If I was hit in the previous round, immediately move away from that cell.

- **Fire Stage**:
  - In Round 1, avoid blindly firing at cell 5 every game; mix up opening shots across likely opponent hide locations (cells 2, 3, 7, 8).
  - In subsequent rounds:
    - If my previous shot scored a `[claim: hit]`, remember my target will likely relocate; do not fire at the exact same cell unless exploiting double-bluffs.
    - If my previous shot missed, eliminate that cell from my target pool for the next round and probe unsearched or off-center cells.
    - Observe my target's firing habits to infer their likely psychological hiding patterns (e.g., if they repeatedly target 5–7, they may hide outside that range).

- **Claim Stage**:
  - When the referee informs me `HIT`, reply `[claim: hit]`.
  - When the referee informs me `MISS`, reply `[claim: miss]`.
  - Never attempt to fake a claim, as rules mandate claims must match private results.