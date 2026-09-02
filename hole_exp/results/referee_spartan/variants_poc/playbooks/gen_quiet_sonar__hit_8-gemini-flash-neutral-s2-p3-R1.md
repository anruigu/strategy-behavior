---
game: gen_quiet_sonar__hit_8
model: gemini-flash
condition: neutral
seed: 2
round: 1
chars: 1276
---
### Playbook for Quiet Sonar

#### Hiding Stage
- Never hide in cell 5, 6, or 7 in early rounds; these are standard focal points for initial shots.
- When choosing a hide location, select from the less commonly fired edge or near-edge cells (1, 2, 8, 9, or 3).
- Do not repeat the same hiding cell in consecutive rounds, especially if targeted near that cell in recent rounds.
- Track the shooter targeting me (e.g., Gamma when playing Harbor) and actively avoid cells they have recently fired at or favored.

#### Firing Stage
- Do not repeatedly fire into cell 5 across multiple rounds; players quickly avoid central cells after round 1.
- In Round 1, if taking a default probe, fire at cell 5, 6, or 4.
- In Rounds 2 through 6, vary fire targets systematically across cells 2, 3, 4, 7, 8, and 9 based on the target player's historical tendencies rather than sticking to a single mid-range cell.
- If a target player was missed at cell $X$, rotate to an adjacent or complementary outer cell on subsequent turns rather than refiring at $X$.

#### Claim Stage
- When the private referee result is MISS, always output `[claim: miss]`.
- When the private referee result is HIT, always output `[claim: hit]`.
- Keep reasoning strictly to one brief line to ensure syntax validity.