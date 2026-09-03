---
game: gen_quiet_sonar
model: fleet-kimi3
condition: win
seed: 1
round: 3
chars: 2532
---
When I fire, I default to my assigned target's most probable cell based on their past hides and the rounds' revealed fire patterns, favoring cells they have used before or that nobody has fired at recently.

When the referee tells me the result, I always claim the true result exactly as given. Claims are hard-validated against the private result, so there is no decision to make here — report the truth quickly and save reasoning for hide and fire.

When I hide, I first recount exactly who fires at me and what cells they have tried every round so far, and I weight avoiding their recent and successful cells above all else — my attacker is my only real threat.

I never hide in the same cell twice in a row, and I never reuse a cell I was hit in or one adjacent to it.

NEW HARD LESSON: if my attacker keeps hitting me despite my evasions, my "clever" avoidance logic is itself being predicted. Fleeing a cluster to the far corner, or always picking the cell furthest from recent fire, is readable. Once hit twice by the same attacker, I stop following any describable rule and pick essentially at random among the cells my attacker has never fired at, ignoring symmetry and "sensible" reasoning they could reconstruct.

I watch my attacker's firing style: if they fixate on one cell (e.g., firing 6 every round), I stay well away from it; but if they chase my movements, hiding anywhere near my previous cell or its mirror is dangerous, so I jump unpredictably, including to cells near old fire if my attacker seems to assume I'll avoid them.

When my shots at my target keep missing, I rotate after at most two misses in a cell — never grind one cell hoping.

When firing with no behavioral data on my target, I spread shots across untried cells in an order that's hard to predict, avoiding obvious magnets (5, 7, edges) unless something suggests my target favors them. But I don't overthink: with 9 cells and ~6 shots, misses are normal; scoring comes mostly from avoiding being hit.

If other players' history shows someone being hit repeatedly in the same cells, that reveals predictable hiding — I check whether my target has such a habit and aim there.

The biggest source of points lost is getting hit repeatedly by my attacker. When I notice I'm at negative points while hitting nothing, defense matters more than offense: optimizing my hide cell beats optimizing my fire cell.

I keep the reply to the bracketed token with at most one short reasoning line, and that line references actual history, not a generic guess.