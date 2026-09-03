---
game: gen_quiet_sonar
model: fleet-qwen38
condition: win
seed: 0
round: 3
chars: 3326
---
**Playbook for Quiet Sonar**

**Claiming**
When the referee tells me the true result, I claim exactly that. The rules require the claim to match the private result, so a false claim is invalid. Never deviate.

**Hiding**
- Identify which player fires at me (the fixed chain determines this). Track that player's public firing history across all rounds.
- When I am asked to hide, I avoid every cell my attacker has fired at in any prior round. This is the single most important rule.
- Among the remaining safe cells, I avoid the cells most recently fired at, since the attacker may repeat their last target.
- I do not overthink "psychological" placement. The only relevant variable is my attacker's actual firing pattern.
- If my attacker's pattern covers few cells, I pick from the untested remainder, favoring cells far from the geometric center to reduce the chance of a lazy default guess.
- **Do not repeat a hide cell from a prior round if any other safe cell is available.** My attacker may be saving that cell for a later round, and repeating it doubles my exposure to a future shot there. Only repeat a hide cell if every other cell has been fired at by my attacker.

**Firing**
- Maintain a running list of cells I have fired at my target and the result (hit or miss).
- **Hard rule: never fire at a cell that previously returned a miss.** A miss means the target was not there that round; the target may move, but re-firing a known-miss cell wastes a shot I could use to test a new cell. This is not a guideline — it is an absolute constraint.
- **Pre-plan a firing sequence before round 1.** Assign a fixed priority order to all 9 cells that spreads coverage across the line. A good default order is: 5, 1, 9, 2, 8, 3, 7, 4, 6 (center, then alternating outward). Each round, fire at the next cell in this order that I have not yet tested. If a cell in the sequence already returned a hit, skip it and move to the next untested cell.
- This guarantees I test 6 distinct cells over 6 rounds, one per round, with no repetition.
- If I ever get a hit, I note the cell. In subsequent rounds I skip that cell (it's already "tested") and continue down my pre-planned list to maximize coverage.
- In the final round, I fire at my best untested cell per the pre-planned order. There is no penalty for scoring, so I always take the shot.

**What did not work**
- Firing cell 7 twice (rounds 2 and 4) and cell 8 twice (rounds 3 and 5) left me with only 4 distinct cells tested out of 9. This was the core failure — I never hit Gamma because I was re-testing cells instead of expanding coverage. The "alternate between low and high" heuristic was too vague to prevent drift back to already-tested cells.
- The fix is a pre-committed firing sequence. By deciding the order in advance, I eliminate the per-round decision of "where should I shoot next?" which is where I keep defaulting back to familiar cells.
- Repeating a hide cell (9 in both rounds 5 and 6) is a risk I should avoid. Even though Echo's visible pattern (even numbers) made 9 safe both times, the correct discipline is to move to a new cell each round.
- Firing cell 2 three separate times in a prior episode (rounds 1, 2, and 5) after confirmed misses — same class of error as the 7/8 repetition this time. The pre-planned sequence eliminates this entirely.