---
game: gen_quiet_sonar
model: gpt-mini
condition: neutral
seed: 1
round: 1
chars: 2762
---
When asked to hide, look at the public list of all fires from the last three rounds and pick a cell that has been fired at least twice recently by other players only if those fired cells are not clustered; otherwise pick a cell that has not been fired in the last three rounds.

When asked to hide and many players concentrate on the center (cells 4–6) or a contiguous block (e.g., 5–8), move to an edge (1–3 or 7–9) that has been fired at least least recently; do not hide repeatedly in the same cell two rounds in a row.

When asked to hide and there is no clear recent clustering, randomize among the less-fired cells (prefer uniformly among them) rather than always choosing the exact center.

When my target fires pattern shows repeated misses on some cells, stop firing the same cells against them; diversify to probe untouched cells.

When choosing a fire cell, do not repeat the exact same firing coordinate more than twice in the same match; if the first two attempts at a coordinate were misses, exclude that coordinate for the rest of the match unless new information suggests otherwise.

When choosing a fire cell, prioritize cells that I personally have not yet tried against that target, with a slight bias toward cells that opponents have NOT recently targeted (they likely avoided them for a reason).

When I have at least one confirmed hit on the target (my private result), continue firing adjacent cells in the next round only if the rules or prior patterns suggest clustering; otherwise spread shots to avoid wasting follow-ups on unlikely adjacent positions.

When submitting a claim, always match the private referee result exactly — claim hit only if I was privately told hit, claim miss only if told miss.

When I observe opponents’ public claims and scores, adjust hide choice defensively if someone is repeatedly scoring hits against me or players on my flank: assume they target predictable spots and move away from those spots.

When I notice my hiding choices are being targeted frequently, break the pattern immediately by moving to an opposite side of the board; do not try to out-guess by small incremental moves.

When the board shows many untried cells and I need information, use one round to probe a less-fired cell rather than repeating an expensive low-probability shot.

Do not rely on being able to bluff via claims (claims must match private results), so focus on unpredictability in hiding and systematic probing in firing rather than on deception.

What did not work and therefore I avoid: hiding repeatedly in the exact same central cell (made me predictable), firing the same mid-range cell every round against the same target (wasted shots), and failing to move to less-targeted edges when the center became crowded.