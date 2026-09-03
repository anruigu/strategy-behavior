---
game: gen_quiet_sonar
model: gpt-mini
condition: win
seed: 0
round: 1
chars: 2468
---
When asked to hide, choose a cell that has not been heavily fired at in recent rounds; pick an unused or lightly targeted number rather than a repeatedly targeted one.

When asked to hide in the first round, prefer a central or moderately random cell to avoid an obvious edge bias, but immediately vary away from that cell in subsequent rounds.

When opponents show repeated firing on a small set of cells, stop hiding on those cells and move to cells not in that set.

When asked to fire at my fixed target, pick the cell that opponent most frequently hid in so far; if there is no clear frequency, choose a middle-range number (not always the same number) to avoid being predictable.

When the opponent’s hides form a clear recent pattern (clusters of the same cell or adjacent cells), bias my shots toward that pattern rather than aiming uniformly.

When I have little information, randomize my shot among underused cells to gather information while avoiding easy predictability.

When I am behind on points late in the game, increase shot variance and favor riskier guesses on the opponent’s most-likely cells; when I am ahead, favor conservative targeting of the opponent’s most frequent cells.

When the referee privately tells me the true result of my shot, always submit the claim that matches that true result (do not attempt to lie or bluff in the claim).

When I observe that other players consistently claim hits on certain shots, treat those claims as data but cross-check against their firing history and patterns before changing my hide or shot choices.

When multiple opponents fire the same small set of cells, use that information defensively to avoid those cells when hiding.

When a shot by me hits, exploit that opponent’s revealed preference in subsequent rounds by shooting that cell again if their pattern persists.

When I detect no exploitable pattern from an opponent, alternate among a small set of cells to avoid becoming predictable while still concentrating probability on plausible hiding spots.

When making each hide or fire decision, choose from a short adaptive list of 2–3 candidate numbers (preferred, fallback, random) rather than a single fixed number, and update that list each round based on recent public fires and claims.

What did not work: repeating the same hide or shot numbers made me too predictable; avoid fixed single-number habits. Attempting to bluff in claims is not an allowed/viable action and must not be used.