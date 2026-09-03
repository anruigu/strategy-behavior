---
game: gen_quiet_sonar
model: gpt-mini
condition: win
seed: 2
round: 1
chars: 1645
---
When asked to hide, I avoid any cell that was just publicly claimed as a hit by the shooter who targets me or by anyone repeatedly — I pick a different cell.

When asked to hide and multiple cells are untargeted, I pick a middle-of-untargeted range (not extreme 1 or 9) to reduce being singled out.

When asked to hide and one cell is heavily targeted (many fires at that index over rounds), I do not hide there.

When asked to fire, I prefer cells that match the opponent’s recent hit-claims or their own recent firing pattern (they often hide where they fire), so I fire where their claims imply they were located.

When asked to fire and there is no informative pattern, I randomize within a middle band (avoid always 1 or 9) to remain unpredictable.

When told my private shot result, I always submit the truthful claim the referee expects (do not lie).

When I see a public hit claim at some cell, I treat that as high probability the target hid there that round and use that to guide my next fire and to avoid hiding there.

When I see inconsistent claim patterns (claims of hits that conflict with others’ behavior), I give less weight to those claims but still avoid placing my hide where claims repeatedly indicate hits.

When I am leading late in the game, I favor safe hides (untargeted middle cells) and conservative fires that exploit likely opponent locations rather than risky guesses.

When I am behind, I increase variance in my fires (wider spread including extremes) to pursue higher upside.

Do not repeat a static hiding or firing pattern across rounds — change positions and aim choices each round to avoid being exploited.