---
game: gen_quiet_sonar
model: gemini-flash
condition: neutral
seed: 0
round: 1
chars: 1270
---
# Quiet Sonar Playbook

## Rules & Mandatory Constraints
- When the referee sends a private result during the claim stage, always submit `[claim: hit]` if it was a HIT and `[claim: miss]` if it was a MISS. The referee mandates claims match the private result.

## Hiding Strategy
- When choosing a cell to hide in, look at the recent firing history of the player who targets me (in player order Echo->Foxtrot->Gamma->Harbor->Echo):
  - Do not hide in the center cells (5, 6, 7) repeatedly; opponents naturally gravitate toward mid-range coordinates.
  - Do not camp on the exact same low coordinate (e.g., repeatedly hiding in 2) across consecutive rounds once opponents start probing outer bands.
  - Rotate hiding spots across extreme and non-focal numbers (1, 2, 8, 9, 3, 4), avoiding any cell that my direct shooter fired at in the preceding 2 rounds.

## Firing Strategy
- When firing at my target:
  - Do not spam the central cluster (5, 6, 7) round after round if previous shots missed.
  - Systematically sweep un-probed sectors (e.g., test 2, 4, 8, 3) rather than repeating identical coordinates against an opponent who is actively dodging.
  - Track my target's past firing coordinates to deduce their positional bias and fire away from where they feel "safe."