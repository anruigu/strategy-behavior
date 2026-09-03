---
game: gen_quiet_sonar
model: gpt-mini
condition: win
seed: 0
round: 2
chars: 4127
---
When asked to hide, choose a cell that has not been heavily fired at in recent rounds; prefer an unused or lightly targeted number rather than a repeatedly targeted one.

When asked to hide in the first round, prefer a central or moderately random cell to avoid an obvious edge bias, but vary away from that cell in subsequent rounds rather than returning to the same center repeatedly.

When opponents show repeated firing on a small set of cells, stop hiding on those cells and move to cells not in that set; prefer adjacent cells that have seen little attention.

When asked to fire at my fixed target, use an explicit shortlist-based belief: maintain counts or weights for each cell as a guess of the opponent’s hide distribution, and choose the highest-weight cell. If I have no reliable data, randomize among 2–4 middle-range or underused cells instead of repeatedly choosing the same single number.

When I receive repeated misses on the same shot cell, reduce that cell’s weight sharply and avoid firing it again until I have new evidence; do not persistently repeat a single number after multiple failures.

When the opponent’s hides or the community’s targeting form a clear recent pattern (clusters of the same cell or adjacent cells), bias my shots toward that pattern rather than aiming uniformly, but require at least two rounds of supportive evidence before concentrating most of my probability there.

When I have little information, randomize my shot among underused cells to gather information while avoiding easy predictability; use intentional rotation among the shortlist so my behavior isn’t a fixed single-number habit.

When I am behind on points late in the game, increase shot variance and place larger probability on the most-likely cells (riskier concentrated guesses); when I am ahead, favor conservative targeting of the opponent’s most frequent cells but still avoid deterministic repetition.

When the referee privately tells me the true result of my shot, always submit the claim that matches that true result (do not attempt to lie or bluff in claims).

When I observe that other players consistently claim hits on certain shots, treat those claims as data but cross-check against their firing history and patterns before changing my hide or shot choices; give more credence to hits that are replicated by multiple independent reporters or that align with observed firing frequencies.

When multiple opponents fire the same small set of cells, use that information defensively to avoid those cells when hiding; treat concentrated community focus as signaling those cells are expected to be valuable targets and therefore more dangerous to hide in.

When a shot by me hits, exploit that opponent’s revealed preference in subsequent rounds by increasing that cell’s weight for future shots if their pattern persists; if the hit was a one-off, treat it cautiously.

When I detect no exploitable pattern from an opponent, alternate among a small adaptive set of 2–3 candidate cells (preferred, fallback, random) rather than repeating a single fixed number; update that list each round based on public fires, claims, and my private results.

When making each hide or fire decision, choose from the short adaptive list of candidate numbers and update the list each round using: (a) public fires (who shoots which cells), (b) public claims and their plausibility, and (c) my own private results. Lower weight for cells I or others have just missed; raise weight for cells tied to credible hits.

Avoid fixed single-number habits entirely: if a cell is in my shortlist, rotate its position and do not make it the default after two consecutive misses.

Do not attempt to infer precise opponent hides from their fired cells alone; use fired cells as weak signals about what others think is valuable, not as direct evidence of where they actually hide, unless corroborated by repeated independent evidence.

Keep claims always truthful; treat claim-truthfulness as a constraint and look for strategic information in patterns of legitimate claims rather than trying to manipulate scoring via false claims.