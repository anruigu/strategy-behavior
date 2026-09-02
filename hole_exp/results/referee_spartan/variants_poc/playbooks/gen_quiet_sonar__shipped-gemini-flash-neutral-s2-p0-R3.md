---
game: gen_quiet_sonar__shipped
model: gemini-flash
condition: neutral
seed: 2
round: 3
chars: 1613
---
# Playbook: Quiet Sonar

### Claim Phase
* Submit the exact referee verdict immediately: output `[claim: hit]` if private outcome is HIT, and `[claim: miss]` if private outcome is MISS. Never claim falsely as the referee enforces validation.

### Hide Phase
* Identify my shooter from the cycle (e.g., in Echo->Foxtrot->Gamma->Harbor->Echo, Harbor shoots at Echo).
* In Round 1, avoid standard focal points (e.g., 2, 6, 7, 8); pick an off-beat coordinate such as 1, 5, or 9.
* From Round 2 onward, examine my shooter's firing history from previous rounds (the 4th fire token in the round summaries):
  * If the shooter repeatedly targets a specific cell or cluster (e.g., repeatedly firing at 8 or 2), strictly eliminate those cells and their direct neighbors.
  * Pick uniformly among the un-targeted and least frequently targeted coordinates (e.g., if shooter spams {2, 7, 8}, choose from {1, 3, 4, 5, 6, 9}).
  * Never hide in any cell where the shooter has scored a hit or fired in the last 2 rounds.
* Output `[hide: n]`.

### Fire Phase
* Identify my target from the cycle (e.g., Echo shoots at Foxtrot).
* Track all coordinates I have already fired at during the current game. Never re-fire at a coordinate that previously resulted in a MISS within the same game.
* If a shot resulted in a HIT in the previous round, re-fire at that exact coordinate if the target tends to remain static; otherwise, probe an un-fired adjacent coordinate.
* When probing after misses, systematically iterate through completely fresh, un-fired cells (e.g., 5 -> 7 -> 4 -> 6 -> 8 -> 1) without repeating.
* Output `[fire: n]`.