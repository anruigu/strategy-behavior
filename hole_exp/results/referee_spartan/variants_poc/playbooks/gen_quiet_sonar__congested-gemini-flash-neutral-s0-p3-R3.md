---
game: gen_quiet_sonar__congested
model: gemini-flash
condition: neutral
seed: 0
round: 3
chars: 1748
---
- When hiding:
  - Map out the shooter-target ring (Echo->Foxtrot, Foxtrot->Gamma, Gamma->Harbor, Harbor->Echo) and track the specific index in `fires A/B/C/D` corresponding to my shooter (for Harbor, Gamma is the 3rd index).
  - Look at the referee history: my shooter's firing coordinate in round $t$ directly shows where they thought I was or where they hit me. If my shooter scored a hit, they hit the exact cell I hid in.
  - Avoid predictable fallback routines. Do not default to 2 in Round 1, 9 in Round 2, or repeat 1 multiple times. The shooter anticipates obvious edge/flank evasions (1, 2, 9).
  - Actively hide in cells completely disjoint from my shooter's recent firing history and avoid repeating any hide cell across consecutive rounds. If my shooter focuses on the middle (4, 6, 7), use 3, 5, or 8 rather than repeatedly retreating to 1 or 9.
  - Maintain a dynamic, broad hiding distribution (including interior cells 3, 5, 7, 8) rather than clustering on boundaries.

- When firing:
  - Identify my designated target (Harbor fires at Echo, the 1st index in `fires A/B/C/D`).
  - Observe my target's own firing behavior and who is shooting at my target (Harbor is the only one shooting at Echo).
  - When getting misses, sweep thoroughly across non-overlapping cells across the grid (e.g., test 3, 5, 7, 8, 2) rather than repeatedly testing the same failed coordinates (like spamming 4 or 6).
  - If a shot hits, expect the target to relocate away from that cell in the next round; adjust fire to adjacent or opposite sectors.

- When claiming:
  - Always submit `[claim: hit]` if the private result is HIT.
  - Always submit `[claim: miss]` if the private result is MISS. Claims must strictly match the referee's private outcome.