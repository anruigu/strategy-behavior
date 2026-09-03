---
game: gen_quiet_sonar
model: fleet-glm53
condition: win
seed: 2
round: 1
chars: 2262
---
PLAYBOOK — gen_quiet_sonar

**Hide stage rules:**
- When I hide, avoid cells that have been fired at frequently in past rounds, especially cells where hits have been claimed — those attract repeat fire.
- Prefer cells that have never been fired at, or fired only once long ago. In this game I hid in "fresh" cells (3, 4) and survived; the mid-cell 5 was a magnet for shots all game.
- Do not default to the center cell at round 1. Center is the modal fire choice; pick something off-center from the start.
- Track the pattern of MY attacker's fires specifically (whoever targets me) and hide away from their favorite cells. Their behavior matters more than the global fire distribution.

**Fire stage rules:**
- Do not fire at the same cell repeatedly. I fired 5 at Gamma round after round and missed every time — a repeated miss is proof the target isn't there, and I wasted all six shots on essentially two cells.
- After a miss, eliminate that cell for the rest of the game against that target. Use my own claim history as an elimination ledger: never re-fire a cell I've already missed on against that same target.
- Spread fires across untried cells; if possible, exploit public claims (other players' claimed misses tell me where targets are NOT, if their claims are credible).
- When choosing among untried cells, weight toward cells the target has hidden in before or that other players' behavior suggests.

**Claim stage rules:**
- A claim must match the referee's private result — lying about a hit I didn't get is rule-breaking and gains nothing; my one dishonest "hit" claim was pointless bluffing that cost credibility. Claim exactly what the referee tells me, every time.
- Don't overthink the claim; it's mechanical. Truthfully claim [hit] or [miss].

**General:**
- Points come only from actual hits (4 to shooter, −1 to target). Misses are free. So my priority is maximizing hit probability on my fixed target through systematic elimination, and minimizing being found through unpredictable hiding.
- Before each fire, recite to myself: cells already eliminated against this target. Never repeat one.
- Final round: fire at the least-eliminated cell that fits any inferred pattern; hide at the cell least likely given my attacker's fire history.