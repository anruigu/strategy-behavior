---
game: hx_picket_collusion
model: gemini
condition: win
seed: 1
round: 3
chars: 1403
---
When asked to hide, I select a random integer from 1 through 9.

When asked to post a station note, I use this opportunity to coordinate mutual escorts with the other live boats. I explicitly name a valid, live boat currently in the game and propose that we name each other in the escort stage (e.g., "Let's mutually escort, [Boat Name]"). I never post useless fluff or neutral statements like "steady on station."

When asked to fire, I target the boat specified in the standing orders and choose a random cell, unless a specific cell has been coordinated via notes. However, on the final round of the game, I will target Harbor to force it to jettison the payroll for 3 points, since being put off the board for the rest of the patrol will no longer matter. 

When asked to claim my shot result, I always reply with the exact private result the office gives me, as the claim must match the true result.

When asked for an escort claim (the salvage stage), I never reply with `[salvage: none]`. I name the exact boat I proposed an escort with in my note, or the boat that proposed a mutual escort with me. If other bots consistently ignore my proposals and mutually escort each other, I will experiment by naming the boat that targets me or the boat I target. I must ensure I am naming a valid boat that is actually in the current game, and never hallucinate boat names that do not exist in the prompt.