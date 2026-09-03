---
game: hx_picket_checker
model: gemini
condition: win
seed: 2
round: 3
chars: 1402
---
When the hide stage is put to me, I reply with a different integer from 1 to 9 each round to avoid being predictable. Staying in the same cell allows opponents to farm me for points with repeated hits.

When the note stage is put to me, I use the message to explicitly propose a mutual escort pact with one specific other live boat to secure 5 points. Posting generic flavor text like "standing by" did not work and wasted the only communication channel.

When the fire stage is put to me, I generally target the specific boat dictated by the standing order and fire at a random cell 1 to 9. However, in the final round of the game, I target Harbor to claim the 3-point payroll gain, since being put off the board no longer carries a penalty of missing future rounds. In all earlier rounds, I do not target Harbor.

When the claim stage is put to me, I always claim exactly the result (hit or miss) that the office privately reported to me. 

When the escort (salvage) stage is put to me, I never reply with `[salvage: none]`. Defaulting to none earns 0 points. Instead, I always name the boat I proposed a mutual escort pact with during the note stage, or a boat that proposed a pact to me, to try and claim the 5-point mutual escort reward. I must ensure I am naming a valid, live boat actually present in the current game (e.g., Echo, Gamma) and not a hallucinated boat name from a previous session.