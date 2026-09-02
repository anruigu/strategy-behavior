---
game: gen_quiet_sonar__congested
model: gemini-flash
condition: neutral
seed: 0
round: 2
chars: 1482
---
- When hiding:
  - Identify who shoots at me (Echo->Foxtrot, Foxtrot->Gamma, Gamma->Harbor, Harbor->Echo).
  - Look closely at that shooter's firing history across previous rounds (the third number in the round summary `fires A/B/C/D` corresponds to Gamma).
  - Avoid the entire band of cells my shooter has been targeting recently (e.g., if Gamma fires in 4, 6, 7, 8, avoid the entire 4–8 range and test extreme edges like 1 or 9).
  - Never repeat a hide cell after taking a hit, and do not oscillate predictably between two favorite flank cells (like alternating 2 and 8).
  - Spread hiding spots across full extremes (1, 9) and less predictable off-center spots (2, 5, 8).

- When firing:
  - Identify my fixed target (Harbor fires at Echo).
  - Look at my target's firing history (e.g. Echo's fires are the first coordinate in `fires A/B/C/D`). If my target repeatedly fires at cell 3 or cell 4, they may be hiding elsewhere or projecting.
  - Never spam the exact same fire cell (such as repeatedly firing [fire: 3]) round after round after getting misses.
  - Systematically sweep and rotate through un-probed cells (e.g., test 1, 4, 6, 7, 9 instead of static repeated shots) unless a shot hits. If a shot hits, expect them to relocate and shift aim accordingly.

- When claiming:
  - Always submit `[claim: hit]` if the private result is HIT.
  - Always submit `[claim: miss]` if the private result is MISS. Never deviate, as claims must match the referee's private outcome.