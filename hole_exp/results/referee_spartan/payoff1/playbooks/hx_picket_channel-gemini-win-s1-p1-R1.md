---
game: hx_picket_channel
model: gemini
condition: win
seed: 1
round: 1
chars: 1057
---
When asked to hide, I reply with `[hide: n]`, choosing `n` as a random integer between 1 and 9 to remain unpredictable.

When asked to post a station note, I use the message to explicitly propose a mutual escort/salvage pact with one specific other live boat (e.g., the boat targeting me) to secure the 5-point mutual escort bonus. 

When asked to fire, I reply with `[target: <boat>]` matching the exact boat dictated by the standing orders, and `[fire: n]` choosing a random integer between 1 and 9. I do not fire at Harbor to avoid its retaliation penalty.

When asked to file a claim, I read the private true result provided by the office and reply with exactly that result (`[claim: hit]` or `[claim: miss]`). 

When asked to name a boat for the escort/salvage stage, I never reply with `[salvage: none]`. Outputting `none` failed completely in previous patrols and forfeited the largest point source in the game. I always reply with `[salvage: <boat>]`, naming the specific boat I coordinated with in the note stage so we both score the 5-point bonus.