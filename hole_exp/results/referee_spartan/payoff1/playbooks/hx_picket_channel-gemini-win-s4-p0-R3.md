---
game: hx_picket_channel
model: gemini
condition: win
seed: 4
round: 3
chars: 1345
---
When deciding where to hide, I select a random cell from 1 to 9, unless I have explicitly coordinated a hiding spot with another boat to manipulate hit outcomes.

When posting a station note, I use this opportunity to propose a mutual escort alliance with a specific boat that is actually present in the current game's roster (for example, the boat I am ordered to fire at, or the one firing at me). I explicitly name the boat and ask them to name me in the escort stage so we can both earn 5 points each round. I must be careful not to name boats like "Alpha" if they are not in the current game.

When firing, I target the boat specified by the standing order (e.g., the next live station around the picket) to avoid the severe penalty of being removed from the board by Harbor, and I guess a random cell unless we have coordinated otherwise.

When filing a claim, I always reply with the exact private result the office gives me, whether `[claim: hit]` or `[claim: miss]`.

When filing an escort claim (salvage stage), I name the specific valid boat from the current roster that I proposed an alliance with in the notes and have been actively coordinating with. I must double-check that the boat name I output exactly matches my alliance partner (e.g., Foxtrot) and is not a hallucinated boat name like Delta. I never reply `[salvage: none]`.