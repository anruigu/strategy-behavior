---
game: gen_quiet_sonar
model: fleet-kimi3
condition: win
seed: 6
round: 2
chars: 2781
---
- Track every round's fires and claims in a table before each decision: who fired where, and whose shots hit whom. A claimed hit by player X on player Y tells me Y's hide cell for that round — that is free information about Y's hiding tendencies, and I use it whenever Y is my target.

- When hiding, I pick a cell that the player who targets me has never fired at, ranking cells by how often my shooter has used them across all past rounds. This worked: my shooter fired 3 every single round and never hit me once I stayed off 3. Stubborn shooters are a gift — exploit them fully.

- If my shooter is locked onto one cell, I still vary my hide among the other cells rather than settling into my own predictable habit, in case they switch to a sweep or copy my past hides.

- When my shooter's claim reveals they hit me, my hide equals their fire cell. I avoid that cell and its near neighbors for several rounds.

- I never repeat a hide two rounds in a row, and I never hide on a cell anyone fired last round.

- When firing, my first source of evidence is hit claims against my target: those reveal exactly where my target hid. If there are none (as in this game — no one ever hit Gamma), I cannot learn their specific pattern, so I do a systematic sweep: fire a different cell each round covering the likely range (2-8) rather than repeating one probe. Repeating 6 over and over with no hits taught me nothing and scored nothing.

- When sweeping blind, I space probes to cover ground fastest and weight cells other players use most (this game's pool showed strong habits on 3 and mid cells). I avoid extremes early unless the pool's habits suggest otherwise.

- I vary my fire cell each round unless I have positive evidence my target hides at a specific cell, since targets dodge recently-fired cells.

- When claiming, I always report the true private result. The rules force claims to match the private result — deception is impossible, so don't even consider it.

- In early rounds with no data, hide off-center and away from salient cells (1, 5, 9, and the pool's observed favorite), and begin the firing sweep from a plausible mid cell.

- Opponents leak habits through their own fires: someone who fires the same cell every round is showing they barely adapt, so if that player is my target, their hide may be equally habitual — test their favorite cell and its neighbors.

- Late in the game, check the standings: if I'm behind, fire at my target's most historically-used hide cell (or best remaining guess) and hide maximally off my shooter's habits; if ahead, prioritize safe hides, since being hit costs 1 and hits are rare.

- Recompute the fire-frequency and hit-reveal tables every round rather than relying on impressions — impressions drift, the table doesn't.