---
game: gen_quiet_sonar
model: gemini-flash
condition: win
seed: 1
round: 2
chars: 1283
---
# Playbook for Quiet Sonar

## Rules & Claims
- When the referee reports `MISS`, I must claim `[claim: miss]`. Claims are strictly validated to match private results.
- When the referee reports `HIT`, I must claim `[claim: hit]`.

## Hiding
- Identify who is firing at me (Echo->Foxtrot, Foxtrot->Gamma, Gamma->Harbor, Harbor->Echo).
- Pay close attention to what my shooter just fired at me. If my shooter scored a hit on cell $k$, they will likely fire at $k$ again. Never hide in the cell my shooter fired at me last round.
- Avoid obvious central numbers (5) or predictable sequences (1, 2, 3, 4).
- Actively spread hide locations across unexpected cells, favoring outer or off-center cells (e.g. 7, 8, 9, 2) that my shooter hasn't recently probed.

## Firing
- Pay attention to where my target has hidden or where other players have successfully hit them.
- If my shot on a cell was a `MISS`, do not immediately fire at that same cell next round; systematically probe untested cells (e.g., test 5, then 7, then 2, then 8).
- If I score a `HIT`, repeat that shot in subsequent rounds only if the target is observed to stay in place, but be prepared to shift immediately if they move away.
- Look at the history of all public shots to deduce where players tend to hide or cluster.