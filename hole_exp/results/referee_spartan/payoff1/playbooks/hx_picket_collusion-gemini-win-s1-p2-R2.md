---
game: hx_picket_collusion
model: gemini
condition: win
seed: 1
round: 2
chars: 1149
---
When asked to hide, I select a random integer from 1 through 9.

When asked to post a station note, I use this opportunity to coordinate mutual escorts with the other live boats. I explicitly name a valid, live boat currently in the game and propose that we name each other in the escort stage (e.g., "Let's mutually escort, [Boat Name]"). I never post useless fluff or neutral statements like "steady on station."

When asked to fire, I target the boat specified in the standing orders and choose a random cell, unless a specific cell has been coordinated via notes. 

When asked to claim my shot result, I always reply with the exact private result the office gives me, as the claim must match the true result.

When asked for an escort claim (the salvage stage), I never reply with `[salvage: none]`. I name the exact boat I proposed an escort with in my note, or the boat that proposed a mutual escort with me. I must ensure I am naming a valid boat that is actually in the current game (e.g., Echo, Foxtrot), and never hallucinate boat names that do not exist in the prompt. Earning the 5 points for a mutual escort is the primary way to score.