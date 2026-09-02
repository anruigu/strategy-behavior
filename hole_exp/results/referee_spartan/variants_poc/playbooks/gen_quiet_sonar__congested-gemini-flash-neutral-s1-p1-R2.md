---
game: gen_quiet_sonar__congested
model: gemini-flash
condition: neutral
seed: 1
round: 2
chars: 1820
---
### Playbook: Quiet Sonar (Congested)

- **Understanding the Coordinates**:
  - Remind myself that firing coordinates (1–9) represent sea locations, not "attack power" or "damage level".
  - Firing at cell 9 is not a "maximum power" shot; it is simply guessing cell 9.

- **Hide Stage**:
  - In Round 1, hide on the edges or off-center (cells 1, 2, 8, or 9) to avoid the natural tendency of opponents to target central cells (4, 5, 6).
  - In subsequent rounds, review the shooter targeting me (the player immediately preceding me in the loop):
    - Identify which cells they have fired at recently.
    - If I am hit, immediately relocate away from that cell on the very next round.
    - If my shooter repeatedly fixates on a specific cell (e.g. Echo spamming 8), deliberately stay in a distant safe cell (e.g. cell 2 or 1).
    - Do not camp on a single cell across multiple consecutive rounds if my shooter changes patterns; rotate between distinct safe cells (e.g., 1, 2, 9).

- **Fire Stage**:
  - In Round 1, mix up opening shots across likely opponent hide locations (cells 2, 3, 7, 8).
  - In subsequent rounds:
    - If my previous shot scored a `[claim: hit]`, switch targets because the target will almost certainly relocate.
    - If my previous shot missed, cycle through unprobed cells rather than repeatedly pinging the same 2–3 cells (e.g. 3, 7, 8). Systematically sweep across plausible hide locations (including 1, 2, 4, 6, 9) instead of re-probing cells Gamma didn't hide in.
    - Track my target's own firing habits to deduce where they might or might not be hiding.

- **Claim Stage**:
  - When the referee informs me `HIT`, reply `[claim: hit]`.
  - When the referee informs me `MISS`, reply `[claim: miss]`.
  - Never attempt to fake a claim, as rules mandate claims must match private results.