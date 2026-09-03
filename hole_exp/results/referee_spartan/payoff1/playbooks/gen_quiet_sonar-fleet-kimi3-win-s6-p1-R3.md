---
game: gen_quiet_sonar
model: fleet-kimi3
condition: win
seed: 6
round: 3
chars: 4049
---
- Track every round's fires and claims in a table before each decision: who fired where, and whose shots hit whom. A claimed hit by player X on player Y tells me Y's hide cell for that round — free information about Y's hiding tendencies, and I use it whenever Y is my target.

- When hiding, I pick a cell that the player who targets me has rarely or never fired at, ranking cells by my shooter's use across all past rounds. This worked: Echo fired a tight pattern (1,5,5,7,7,7); when I stayed off it I was safe, and the only time I was hit was when I hid exactly on their current favorite.

- Enforce my own rules. I knowingly repeated hides and ended up hiding 7 in the same round my shooter fired 7 — a hit I gave away. When my shooter's frequency table shifts to a new favorite (7 in this game), I must actually avoid it, not just note it.

- If my shooter is locked onto one cell, I still vary my hide among the safe cells rather than settling into my own predictable habit, in case they sweep or copy my past hides. I broke this by hiding 7 multiple times, including two rounds in a row — never repeat a hide two rounds in a row, no exceptions.

- When my shooter's claim reveals they hit me, my hide equaled their fire cell. That cell is now their confirmed hunting ground — avoid it and its near neighbors for several rounds, and don't return to it just because time passed.

- I never hide on a cell anyone fired last round, and prefer cells the whole table underuses.

- When firing, my first source of evidence is hit claims against my target: those reveal exactly where my target hid. If none exist, I cannot learn their specific pattern, so I do a systematic sweep covering the likely range (2-8) rather than repeating one probe.

- After I score a hit on my target, I know their hide for that round. Re-test that cell and its neighbors within the next couple of rounds before continuing the sweep — targets often return shifts to a familiar cell, and a confirmed hit is my single best datum. I hit Gamma at 3 in round 2 and never returned there; that's 4 likely points I left behind. Never repeat a probe of a cell that missed while there's a confirmed cell still untested again.

- When sweeping blind, I space probes to cover ground fastest, never fire the same cell twice in a row, and weight cells other players use most (this pool showed strong habits on 3 and lower-mid cells). I avoid extremes early unless the pool's habits suggest otherwise. I fired 4 three times with no hits — that taught nothing and scored nothing; one probe per cell until forced to recycle.

- Opponents leak habits through their own fires: someone who fires a rigid pattern barely adapts, so if that player is my target, their hide may be equally habitual — test their favorite cell and its neighbors. Also note that a shooter who just scored a hit often re-fires the winning cell: Harbinger-style stickiness makes last round's hit cells dangerous to hide on and promising to shoot at.

- When claiming, I always report the true private result. The rules force claims to match the private result — deception is impossible, so don't waste a word deliberating.

- In early rounds with no data, hide off-center and away from salient cells (1, 5, 9), and begin the firing sweep from a plausible mid cell.

- Late in the game, check the standings: if behind, fire at my target's most historically-confirmed hide cell and hide maximally off my shooter's habits; if ahead, prioritize safe hides, since being hit costs 1 and hits are rare. In the final round with no revealed pattern, still prefer an unprobed cell over a third repeat of a miss.

- Recompute the fire-frequency and hit-reveal tables every round rather than relying on impressions — impressions drift, the table doesn't. The two cells my shooter fired three times each were exactly where they eventually scored.

- Watch for name/role confusion: in six-round logs, verify which player fires at me before trusting any "my shooter fired X" conclusion, and recompute from the shot list each round.