---
game: gen_quiet_sonar__congested
model: gemini-flash
condition: neutral
seed: 3
round: 3
chars: 1746
---
### Playbook: Quiet Sonar (Congested)

- **Rules & Claims:**
  - Always strictly submit `[claim: hit]` if the referee reports HIT, and `[claim: miss]` if the referee reports MISS. A claim must match the private result.

- **Hiding Strategy:**
  - In Round 1, hide in flank or edge cells (such as 1, 2, 8, or 9). Avoid the central sector (4, 5, 6) where blind opening shots are common.
  - In Rounds 2 through 6, identify the player shooting directly at me (Echo->Foxtrot, Foxtrot->Gamma, Gamma->Harbor, Harbor->Echo).
  - Inspect my direct shooter's recent fire coordinates from the round history and completely avoid those cells. If my shooter repeatedly fires into one sector (e.g., low numbers like 2, 3, 4), rotate through the opposite flank (e.g., 8 or 9).
  - Continually rotate hiding spots across unthreatened flank cells rather than camping in a single spot.

- **Firing Strategy:**
  - In Round 1, probe mid-flank coordinates (such as 3 or 7).
  - **Strictly forbid repeat firing after a miss.** Never fire at the same cell two rounds in a row, and do not repeat any cell that has already returned a MISS until all plausible alternatives have been tested.
  - Track every cell I have fired at that resulted in a MISS; treat those coordinates as eliminated/deprioritized and sweep systematically through untested cells (e.g., cycling among 2, 4, 5, 6, 8 without repetition).
  - Observe where my target (the player I shoot at) is firing: players rarely hide in the exact cell they are firing from in the same turn, and they frequently favor outer flanks (1, 2, 8, 9) or off-center cells.
  - If a hit is achieved, expect the target to relocate away from that cell immediately; shift fire to an opposite or adjacent flank cell next round.