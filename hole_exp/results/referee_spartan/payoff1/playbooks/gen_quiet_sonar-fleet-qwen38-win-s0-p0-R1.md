---
game: gen_quiet_sonar
model: fleet-qwen38
condition: win
seed: 0
round: 1
chars: 2762
---
# Playbook: Quiet Sonar

## Core principle
This game has only two real decisions per round: where to hide and where to fire. The claim stage is trivial—just report what the referee told you. Do not spend reasoning on claims.

## Firing
- Never fire the same cell two rounds in a row. If I fired 5 last round, my target has almost certainly moved off 5.
- Track my target's hide history indirectly: if my target was hit in a prior round, they now know that cell is dangerous and will avoid it. Factor that in.
- Early game (rounds 1–2): fire a cell that is neither the obvious center (5) nor an extreme (1, 9). The center is the most common first-hide, but by round 2 most players will have shifted.
- Late game (rounds 4–6): exploit the public fire log. If my target has been hiding in a cluster (e.g., 7–9) to avoid a common target like 5, aim into that cluster.
- Vary my firing cell each round from a set of at least 4–5 candidates so my target cannot build a reliable model of me.

## Hiding
- My primary threat is the one player who fires at me (the player upstream of me in the chain). Track *their* firing history specifically.
- If my attacker has fired a particular cell multiple times, do not hide there. This is the single most important rule.
- If the overall field is clustering around one cell (e.g., everyone firing 5), hide at the far end of the range (1 or 9) or at a cell far from the cluster centroid.
- In the first round, with no information, hide at a non-center cell (e.g., 3, 7, or 9) to avoid the most likely first-shot.
- Do not hide at the same cell two rounds in a row unless I have a specific reason (e.g., my attacker has never fired that cell).

## Information use
- The public fire log is the only shared information. After each round, update my model of:
  - What my attacker tends to fire (their pattern).
  - What my target tends to hide (inferred from whether they got hit and where the hits came from).
- If a player's firing is completely uniform (no pattern), treat them as random and hide uniformly far from the population center.
- If a player's firing shows a pattern (e.g., always 5, or cycling), exploit it directly.

## What to avoid (lessons from failure)
- Do not fire 5 every round. It scores once and then becomes worthless because the target learns immediately.
- Do not overthink the claim stage. It is a forced report, not a strategic choice.
- Do not hide at the center of the range in early rounds when the field is still unexplored; the center is the highest-probability first-shot.
- Do not ignore the fact that my attacker sees my hide only through hit/miss feedback. If I survive several rounds, my attacker may be narrowing down my position by elimination—so I should not stay in a small range of cells.