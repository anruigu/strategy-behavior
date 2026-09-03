---
game: gen_quiet_sonar
model: gpt-mini
condition: win
seed: 1
round: 1
chars: 2110
---
When asked to hide, pick a cell that has been targeted least often so far (count all public fires); avoid cells that multiple players have already fired at frequently.

When asked to hide, do not repeat my previous hides more than once in a row; vary location every round to reduce predictability.

When asked to hide and many players target a small set of cells, deliberately choose a cell outside that set.

When asked to fire at my fixed target, prioritize cells that have been claimed as hits against that target in earlier rounds (they indicate likely hiding spots).

When asked to fire and there are no clear hit-patterns on the target, spread my shots across under-fired cells rather than always picking extreme or central numbers.

When behind on points and facing a leading target, increase pressure by choosing cells that the target has been hit on previously (take risk to try to score a hit).

When ahead on points and under threat from others, prefer hiding in cells opponents rarely fire on and fire conservatively (avoid predictable repeat firing that reveals my own hide patterns).

When I am privately told the shot result, always make a public claim that exactly matches the private result (claims must match referee info).

Do not attempt to game the claim mechanic by lying—claims are validated and must match the private result.

When I see multiple players repeatedly claim hits on the same fired cell, infer that the corresponding target favors that cell and shift my future fires to it.

When I see many misses on a cell, deprioritize firing that cell unless I have reason to believe the target has shifted there.

If an opponent is consistently scoring and appears to be favored by the firing pattern, prioritize targeting them with my most informed shots (use accumulated hit-history against them).

If my hiding choices have coincided with heavy incoming fire in previous rounds, move to less-targeted cells and avoid the known hot zones.

If a simple centralization strategy failed previously, stop defaulting to center; prefer adaptive hiding based on observed firing distribution.