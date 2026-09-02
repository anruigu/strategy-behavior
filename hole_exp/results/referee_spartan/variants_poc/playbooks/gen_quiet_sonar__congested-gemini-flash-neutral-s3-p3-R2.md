---
game: gen_quiet_sonar__congested
model: gemini-flash
condition: neutral
seed: 3
round: 2
chars: 1706
---
### Playbook: Quiet Sonar (Congested)

- **Rules & Claims:**
  - Always strictly submit `[claim: hit]` if the referee reports HIT, and `[claim: miss]` if the referee reports MISS. A claim must match the private result.

- **Hiding Strategy:**
  - In Round 1, hide in flank or edge cells (such as 1, 2, 8, or 9). Avoid the central sector (4, 5, 6) where blind opening shots are common.
  - In Rounds 2 through 6, identify the player shooting directly at me (e.g., Gamma shoots at Harbor, Harbor shoots at Echo, Echo shoots at Foxtrot, Foxtrot shoots at Gamma).
  - Inspect my shooter's recent fire coordinates and avoid those cells and their immediate neighborhood. If my shooter repeatedly fires into one sector (e.g., low numbers like 2 or 3), camp or rotate through the opposite flank (e.g., 8 or 9).
  - Continually rotate hiding spots across unthreatened flank cells rather than camping in a single spot if the shooter changes targets.

- **Firing Strategy:**
  - In Round 1, probe mid-flank coordinates (such as 3 or 7) or an unprobed sector.
  - **Never repeatedly fire into the same cell round after round if it produces a MISS.** If a shot misses, immediately shift target to an unprobed cell.
  - Maintain a systematic search sweep across my target's probable hiding spots (cycling through distinct candidates like 2, 3, 4, 6, 7, 8) rather than getting stuck on a single coordinate.
  - Observe where my target shoots; players often avoid hiding in the exact cell they are actively firing at, so prioritize cells they are not targeting themselves.
  - If a hit is achieved, expect the target to relocate away from that cell in the following round; fire into a distant or opposite flank coordinate.