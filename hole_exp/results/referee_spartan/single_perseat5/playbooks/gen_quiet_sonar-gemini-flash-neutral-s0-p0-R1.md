---
game: gen_quiet_sonar
model: gemini-flash
condition: neutral
seed: 0
round: 1
chars: 1127
---
- **Claim Stage**:
  - Always submit the exact outcome provided by the referee: `[claim: hit]` if told hit, `[claim: miss]` if told miss. Never deviate, as claims are strictly validated against private results.

- **Hide Stage**:
  - Track where the player shooting at me (Harbor when I am Echo, or the relevant upstream shooter) has fired in recent rounds.
  - Avoid cells repeatedly targeted by my upstream shooter (especially central cells like 5, 6, 7).
  - Hide in cold peripheral or off-center spots (such as 1, 2, 8, or 9) and switch locations if my shooter begins probing near my previous hiding spot.

- **Fire Stage**:
  - Do not assume higher cell coordinates deal more damage; coordinates are purely spatial grid locations (1 through 9).
  - Track where my target (Foxtrot when I am Echo) has been firing and where other players have shot at them.
  - Avoid firing repeatedly at the exact same coordinates (e.g., repeatedly shooting 5, 6, or 7) when receiving misses.
  - Systematically sweep untested cells across the 1–9 range to locate the target's submarine rather than clumping shots in the center or high end.