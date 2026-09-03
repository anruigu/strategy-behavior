---
game: gen_quiet_sonar
model: gpt-mini
condition: win
seed: 2
round: 1
chars: 1903
---
When asked to hide, pick a cell that has been targeted least often in recent rounds (prefer cells with few or no recent fires).

When asked to hide early in the match, randomize among a small set (center + two off-center) rather than always the same cell.

When historical firing shows clustering on a few cells, avoid those clustered cells for my hide.

When opponents' claims and public fires imply some cells are popular for dishonest claimed hits, treat those cells as riskier to hide in.

When my assigned target is fixed, vary my fire choices instead of repeating the same coordinate after misses; do not persistently fire the same cell after repeated misses.

When choosing a fire coordinate against my target, mix between:
- the cell(s) that have been targeted at the target the most (if I infer they tend to hide where others search),
- and low-frequency cells (to exploit predictable patterns),
using a randomized schedule so my shots are not trivially predictable.

When my target has high score and I need points, bias my fire selection slightly toward the most-likely inferred hide (based on others' shot/claim history) while still randomizing some fraction of the time.

When I am privately told the true result of my shot, always submit the claim that matches the private result (truthful claim).

When validating a choice, ensure all hides and fires are integers 1–9 and claims are exactly "hit" or "miss".

When I see opponents repeatedly claim hits on the same coordinates, treat those coordinates as suspect (either actually strong choices or signals to avoid when hiding).

When the game is short (few rounds left) and I need to change my standing quickly, concentrate fires to a small set of inferred likely cells rather than wide randomization.

If repeated strategy (e.g., always firing 7) produced no hits in prior play, stop that repetitive choice and shift to a mixed strategy.