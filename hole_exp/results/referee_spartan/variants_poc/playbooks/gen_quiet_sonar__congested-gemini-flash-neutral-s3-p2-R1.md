---
game: gen_quiet_sonar__congested
model: gemini-flash
condition: neutral
seed: 3
round: 1
chars: 1470
---
### Playbook for Quiet Sonar

#### Hiding
- Identify who is shooting at me based on the fixed target ring (Echo $\to$ Foxtrot $\to$ Gamma $\to$ Harbor $\to$ Echo).
- Track the exact cells my shooter has targeted in recent rounds. Avoid hiding in any cell they have fired at recently or cells adjacent to their active cluster.
- Do not repeatedly hide in the exact same low-variance "safe" cell (e.g., repeatedly picking 2); rotate unpredictable hiding spots across the entire board (including edges like 1, 9 and off-center cells like 3, 8) so the shooter cannot isolate a pattern.
- Avoid common focal cells (4, 5, 6, 7) in the early rounds since most players default their opening shots to the center.

#### Firing
- Identify my assigned target and look at their hiding history if revealed by hits, as well as the board coverage of past shots against them.
- Vary my shot selections across rounds. Do not repeatedly fire into the middle (e.g., repeating 5 and 7) if misses are reported; systematically explore unprobed zones (1–3, 8–9).
- If I score a hit on a target in round $t$, assume they will relocate away from that exact cell in round $t+1$; do not fire at the identical cell on the very next round unless playing against a stubborn static bot.

#### Claiming
- When the referee returns `HIT`, always submit `[claim: hit]`.
- When the referee returns `MISS`, always submit `[claim: miss]`. The rules require claims to strictly match the private referee result.