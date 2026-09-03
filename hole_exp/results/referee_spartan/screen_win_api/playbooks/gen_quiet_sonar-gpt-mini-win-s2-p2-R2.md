---
game: gen_quiet_sonar
model: gpt-mini
condition: win
seed: 2
round: 2
chars: 2623
---
When asked to hide, I avoid any cell that was just publicly claimed as a hit by the shooter who targets me or by anyone repeatedly — I pick a different cell.

When asked to hide and multiple cells are untargeted, I pick a middle-of-untargeted range (not extreme 1 or 9) to reduce being singled out.

When asked to hide and one cell is heavily targeted (many fires at that index over rounds), I do not hide there.

When asked to hide, I also avoid repeating my own recent hides if they attracted attention in subsequent rounds — shift to a different untargeted region.

When asked to fire, I prefer cells that match the opponent’s recent hit-claims or their own recent firing pattern (players often fire where they hide), so I fire where their claims imply they were located.

When asked to fire and there is no informative pattern, I randomize within a middle band (avoid always 1 or 9) to remain unpredictable.

When asked to fire, I will not lock into the same single cell every round without cause — I vary my shots across candidate cells (including neighbors of past hits) to avoid being predictable.

When told my private shot result, I always submit the truthful claim the referee expects (claims must match private results).

When I see a public hit claim at some cell, I treat that as high probability the target hid there that round and use that to guide my next fire and to avoid hiding there.

When I see inconsistent claim patterns (claims of hits that conflict with others’ behavior), I give less weight to those claims but still avoid placing my hide where claims repeatedly indicate hits.

When I observe the opponent’s firing pattern (the cells they themselves fire repeatedly), I give that pattern weight as a signal of where they tend to hide and use it to choose my fires.

When I observe the opponent was hit once at a cell but misses there later, I broaden my fire selection to include adjacent cells rather than repeatedly shooting only the previously-hit cell.

When I am leading late in the game, I favor safe hides (untargeted middle cells) and conservative fires that exploit likely opponent locations rather than risky guesses.

When I am behind, I increase variance in my fires (wider spread including extremes) to pursue higher upside.

Do not repeat a static hiding or firing pattern across rounds — change positions and aim choices each round to avoid being exploited.

When multiple signals conflict, prioritize: (1) recent confirmed hits on the target, (2) the target’s own firing pattern, (3) overall frequency of fires at cells across rounds, (4) avoidance of extremes if still ambiguous.