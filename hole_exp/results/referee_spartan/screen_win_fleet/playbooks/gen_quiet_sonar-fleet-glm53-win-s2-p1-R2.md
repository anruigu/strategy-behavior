---
game: gen_quiet_sonar
model: fleet-glm53
condition: win
seed: 2
round: 2
chars: 3164
---
PLAYBOOK — gen_quiet_sonar

**Hide stage rules:**
- When I hide, avoid cells that have been fired at frequently in past rounds, especially cells where hits have been claimed — those attract repeat fire.
- Prefer cells that have never been fired at, or fired only once long ago. Across the game, never-fired cells (1, 3, 9) stayed safe while the mid-cell 5 was a hit magnet every single round.
- Do not default to the center cell at round 1. Center is the modal fire choice; pick something off-center from the start.
- Track the pattern of MY attacker's fires specifically (whoever targets me) and hide away from their favorite cells. In the last game my attacker locked onto cell 2 for four straight rounds; staying off it kept me at 0 losses all game.
- Repeating one safe hide cell (e.g. 9) worked while my attacker kept firing elsewhere, but it is fragile — if the attacker ever misses at a cell and eliminates it, they will move on. Prefer rotating among the two or three safest never-fired cells rather than camping one.

**Fire stage rules:**
- Do not fire at the same cell repeatedly. A miss is strong evidence the target isn't there; never re-fire a cell I've already missed on against that same target. Use my own claim history as an elimination ledger.
- Spread fires across untried cells. In the last game I did this correctly (5, 4, 8, 2, 3 — no repeats after a miss) and still got zero hits in six rounds, so know the limits: if the target randomizes, elimination alone may not close the gap in six rounds.
- Watch for targets that REPEAT their hide cell. Other players' repeated claimed hits at the same cell (e.g. a shooter hitting cell 5 round after round) reveal a camper. If any shooter claims repeated hits on MY target at one cell, fire that cell immediately — it is the single highest-value inference available.
- Also exploit others' claimed misses on my target: those cells are (if credible) eliminated for me too, for free.
- If no pattern exists by late rounds, just cover fresh cells systematically; do not psychologically overfit.

**Claim stage rules:**
- A claim must match the referee's private result — the referee validates it, so dishonesty is rule-breaking and gains nothing. Claim exactly what the referee tells me, every time.
- Don't overthink the claim; it's mechanical. Truthfully claim [hit] or [miss].

**General:**
- Points come only from actual hits (4 to shooter, −1 to target). Misses are free. Priority: maximize hit probability on my fixed target through systematic elimination plus pattern-reading, and minimize being found through unpredictable hiding.
- My score of 0 with perfect truth-telling and safe hiding shows the floor is 0, not negative — never take hide risks (hot cells) chasing nothing, and never break claim rules. The upside has to come from smarter firing at a camper or from reading eliminations faster.
- Before each fire, recite to myself: cells already eliminated against this target (my misses plus others' claimed misses on them). Never repeat one.
- Final round: fire at the least-eliminated cell that fits any inferred pattern; hide at the cell least likely given my attacker's fire history.