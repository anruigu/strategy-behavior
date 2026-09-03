---
game: gen_quiet_sonar
model: gpt-mini
condition: neutral
seed: 1
round: 3
chars: 5358
---
When asked to hide, I check the public fires and claims from the last three rounds (at minimum) and avoid any cell that has been targeted repeatedly (2+ times) in that window unless those fires are spread rather than clustered; prefer a cell that has not been fired in the last three rounds.

When asked to hide and many players concentrate on the center (cells 4–6) or a contiguous block (e.g., 5–8), I move to an edge (1–3 or 7–9) that has been fired least recently; I do not hide in the same cell two rounds in a row.

When asked to hide and there is no clear recent clustering, I randomize among the less‑fired cells (prefer uniformly among them) rather than always choosing the same edge or center cell.

When my hiding choice has been targeted repeatedly by others, I break the pattern by moving to the opposite side of the board rather than making a one‑cell incremental shift.

I maintain a short private list of three candidate hides (one recent edge, one opposite edge, one random under‑fired cell) and rotate among them subject to the “no repeat hide” rule.

When asked to fire, I prioritize cells I personally have not yet tried against that target, with a bias toward cells opponents have not recently targeted (they may have avoided them for a reason).

I will not repeat the exact same coordinate more than twice in a match. If my first two attempts at a coordinate were misses, I exclude that coordinate for the rest of the match unless new evidence (an opponent’s confirmed public hit there, or a clear clustering signal) justifies revisiting it.

When choosing a fire cell, I give priority to cells where opponents have publicly claimed hits on the same target (public hits are strong signals). If no such signal exists, I probe under‑fired cells to gather information.

If I score a private hit on my target, I will consider following up nearby only when other players’ patterns or the distribution of recent fires suggest clustering; otherwise I diversify follow‑ups because players often spread hides to edges in this meta.

When opponents’ public claims show consistent success against a particular player (they repeatedly score hits on that player), I infer that player is predictable and avoid hiding where their shots concentrate; conversely, I may adopt that shooter’s successful firing pattern if I need to attack that same predictable player.

When I observe contradictory public patterns (many misses but occasional hits at different locations), I favor information‑gathering shots at under‑fired cells over repeating low‑probability guesses.

When I need information and many untried cells remain, I use a round to probe an under‑fired cell rather than repeating a low‑probability shot that already missed twice; prioritize coverage over repeated probing unless there is a plausible clustering signal.

When deciding between center and edge for hiding or firing, I balance unpredictability and density: if opponents cluster on center I move to an edge; if opponents cluster on edges I consider center. I do not adopt a permanent center/edge bias—I respond to the table pattern.

I always claim exactly the private referee result — claim hit only if privately told hit, claim miss only if told miss. Because claims are constrained, I focus on unpredictability in hiding and systematic probing in firing rather than attempting deception.

I stop hiding in the exact same cell repeatedly, stop firing the same cell more than twice, and stop making only small incremental shifts when targeted — instead make larger relocations when my location appears discovered.

I treat an opponent’s public hit as a reliable signal and consider firing that same cell against the same target in the next round, but only if that cell is consistent with recent clustering or if the opponent has shown repeat hits there.

I learned to be more conservative about repeating my preferred probe (cell 2 in past games): repeated misses on the same coordinate with no contrary public hits mean I should abandon that coordinate for the match.

I learned the value of winning hits (4 points) and their leverage on standings: when a plausible target cell emerges (from public hits or concentrated firing patterns), I will prioritize taking that shot even if it is partially predictable, because confirmed hits swing scores strongly.

When under pressure (negative-ish score or opponents pulling ahead), I shift from safe, predictable hides to deliberately probing untouched pockets to create opportunity for hits rather than passive avoidance.

I keep a running mental frequency map (recent 3–4 rounds) of how many times each cell was fired publicly and which claims were hits; I consult it every hide and fire decision.

When multiple equally under‑fired choices exist, I randomize among them to avoid giving opponents an exploitable pattern.

I do not attempt to misreport claims — the rules forbid it — so I focus my strategic complexity on hide selection and firing sequence.

These rules are the baseline; in live play I will adapt minor parameters (how many rounds of history to consider, when to revisit a twice-missed cell) based on observed opponent behavior, but I will preserve the hard constraints: no more than two repeats of a fired coordinate, no hiding same cell two rounds in a row, truthful claims, and rotating among three candidate hides.