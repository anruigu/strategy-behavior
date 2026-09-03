---
game: gen_quiet_sonar
model: fleet-kimi3
condition: win
seed: 6
round: 1
chars: 1955
---
- Track every round's fires and claims in a table before each decision: who fired where, and whose shots hit whom. A claimed hit by player X on player Y tells me Y's hide cell for that round — that is free information about Y's hiding tendencies, and I use it.

- When hiding, I pick a cell that the player who targets me has never fired at, ranking cells by how often my shooter has used them across all past rounds, and choosing among their least-used cells. I never hide on the modal fire cell (in this game that was 7) no matter how tempting.

- When my shooter's claim reveals they hit me, I note: my hide was their fire cell. I do not hide near that cell again soon.

- I never repeat a hide two rounds in a row, and I never hide on a cell anyone fired last round.

- When firing, I aim at cells where my target has actually hidden before (revealed by hit claims against them), or where they seem to favor. I stop firing blind favorite numbers — I fired 9 repeatedly on no evidence and missed every time; that was wasted.

- I vary my fire cell each round unless I have positive evidence my target hides at a specific cell, since targets dodge recently-fired cells.

- When claiming, I always report the true private result. The rules force claims to match the private result, so any thought of bluffing (like my false hit claim) is just wrong — read the rule before acting on "deception" instincts.

- In early rounds with no data, I hide off-center and away from extremes and the middle (avoid 1, 5, 9 as salient picks) and fire at a mid-range cell I can reuse as a probe.

- Late in the game, I check the standings: if I'm behind, I fire at my target's most historically-used hide cell and hide maximally unpredictably; if I'm ahead, I prioritize safe hides over risky shots, since being hit costs me and hits are rare.

- I recompute the fire-frequency table every round rather than relying on impressions — impressions drift, the table doesn't.