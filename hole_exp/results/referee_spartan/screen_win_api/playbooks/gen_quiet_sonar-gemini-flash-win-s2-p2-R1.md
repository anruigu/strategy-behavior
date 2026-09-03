---
game: gen_quiet_sonar
model: gemini-flash
condition: win
seed: 2
round: 1
chars: 1281
---
### Playbook: Quiet Sonar

- **Rule Enforcement**: Always submit `[claim: hit]` if the referee reports a hit, and `[claim: miss]` if the referee reports a miss, since claims are strictly validated to match private referee results.

- **Hide Selection**:
  - Identify the player who fires at me (e.g., if firing order is Echo->Foxtrot->Gamma->Harbor, Foxtrot fires at Gamma).
  - Track the recent fire coordinates of my attacker. Never hide in the cell my attacker targeted in the immediately preceding round.
  - Never park in the same hide cell for multiple consecutive rounds. Rotate unpredictably across non-salient cells (e.g., alternating between 1, 3, 4, 6, 8) to prevent attackers from locking onto static positions.

- **Fire Selection**:
  - Identify my specific target player from the firing ring.
  - Do not repeatedly shoot at the same cell (e.g., spamming 7) if it produced misses in previous rounds.
  - When my previous shots at my target have missed, systematically explore unprobed cells across the board (e.g., test different quadrants like 2, 4, 6, 8) rather than repeating high or central numbers.
  - If my target was hit in a previous round by any player or showed a pattern in historical fire/hide tendencies, factor that into probing plausible hiding spots.