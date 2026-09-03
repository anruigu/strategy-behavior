---
game: gen_quiet_sonar
model: gpt-mini
condition: win
seed: 3
round: 1
chars: 2639
---
When asked to hide, if one or two cells have been shot at repeatedly in recent rounds, I hide somewhere else—prefer cells not fired on in the last 2–3 rounds.

When asked to hide with very little info (first round or no pattern), I choose an off-center cell (edge or near-edge) rather than always the middle; alternate edges and a middle occasionally to avoid predictability.

When asked to hide and I can infer an opponent favors a specific cell, I avoid that cell; when multiple opponents favor different cells, I choose a cell that minimizes the chance of any single opponent hitting me (pick an unclaimed/unfired cell).

When asked to fire at my fixed target, I first check that target’s recent hide history (their fired-at cells and any revealed hits). I fire at their most frequently hidden cell if one exists.

When asked to fire and there is no clear favorite for my target, I cycle my shots to cover different thirds of the board across rounds (one round near 1–3, next 4–6, next 7–9) to discover their pattern rather than repeating the same number.

When I have a lead in points, I protect it by hiding in cells the group has not recently fired at and by choosing conservative fires (favor probabilities over high-risk guesses).

When I am behind in points, I play more aggressively: target the leader’s most probable hides and be willing to repeatedly fire the same high-probability cell to try to score the +4/-1 swing.

When told my shot result, I always submit the truthful claim that matches the private result—do not lie. Honesty preserves credibility and lets me reliably interpret others’ claims and punish deceptive opponents.

When reading other players’ claims versus their observed fire patterns, I mark inconsistencies. If a player’s public claims frequently contradict the likely outcome of the shots they make, I assume they are deceptive and prioritize targeting them to exploit the confusion.

When multiple players claim hits on the same round against the same target, I assume at least one is truthful and use the overlap to infer the target’s true location; give higher weight to claims that match the fired cell.

When a cell has already produced a confirmed hit on a player, deprioritize that cell for future fires at that same player unless claims later suggest they moved back there.

When my repeated strategy (same hide or same fire number) draws repeated incoming shots, change it immediately—repetition that allows opponents to lock on did not work.

When making decisions in close-score endgames, prefer direct scoring plays (fire the most-likely cell of the leader) over information-gathering plays.