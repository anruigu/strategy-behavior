---
game: gen_quiet_sonar
model: gemini-flash
condition: neutral
seed: 2
round: 3
chars: 1862
---
### Target Tracking & Firing
- Identify who targets whom from the game setup (e.g., Echo->Foxtrot, Foxtrot->Gamma, Gamma->Harbor, Harbor->Echo).
- Pay close attention to who shoots at my target and when hits occur:
  - If my target is claimed as hit by their shooter, that cell is the exact location my target occupied that round.
  - Notice the opponent bots' deterministic hide patterns:
    - Look at the fires of the player shooting my target (e.g., if Echo is my target, look at who targets Echo; wait, Harbor targets Echo, but look at other cyclic hits).
    - Notice that in both games, Echo consistently fires 5 and gets hit repeatedly (e.g. Echo hits Foxtrot at 5, Foxtrot hits Gamma, etc.).
    - Bots often hide where they fire or have static hide patterns across rounds.
    - Check if the target is hiding at the same coordinate repeatedly (e.g., 7, 8, 9, 1, or their own previous fire location). If probing 3, 4, 5, 6 repeatedly yields misses, sweep unprobed extreme values: 7, 8, 9, or 1, 2.
    - Test extreme values (like 7, 8, 1) early if center probes (4, 5, 6) miss.

### Evasion & Hiding
- Identify who shoots at me from the cyclic targeting structure (e.g., Gamma shoots at Harbor).
- Track the firing history of my direct shooter:
  - Gamma frequently probes mid-to-high cells (e.g. 4, 6, 7).
  - Hiding in safe corner cells like 1, 2, or 9 has maintained a clean sheet (0 hits conceded).
  - Continue rotating between low cells (1, 2) and high outer cells (9) while avoiding whichever specific coordinates the shooter has targeted in recent rounds.
  - If ever hit, immediately relocate to an unprobed distant cell.

### Claiming
- When the referee returns `HIT`, submit `[claim: hit]`.
- When the referee returns `MISS`, submit `[claim: miss]`.
- Strictly match the referee's private outcome as claims are validated against ground truth.