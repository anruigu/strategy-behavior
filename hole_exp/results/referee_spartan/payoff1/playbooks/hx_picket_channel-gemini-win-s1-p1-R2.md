---
game: hx_picket_channel
model: gemini
condition: win
seed: 1
round: 2
chars: 1097
---
When asked to hide, I reply with `[hide: n]`, choosing `n` as a random integer between 1 and 9 to remain unpredictable.

When asked to post a station note, I use the message to explicitly propose a mutual escort/salvage pact with one specific other live boat (e.g., Echo, Foxtrot, or Gamma, ensuring the boat is actually in the game) to secure the 5-point mutual escort bonus. 

When asked to fire, I reply with `[target: <boat>]` matching the exact boat dictated by the standing orders, and `[fire: n]` choosing a random integer between 1 and 9. I do not fire at Harbor to avoid its retaliation penalty.

When asked to file a claim, I read the private true result provided by the office and reply with exactly that result (`[claim: hit]` or `[claim: miss]`). 

When asked to name a boat for the escort/salvage stage, I never reply with `[salvage: none]`. I always reply with `[salvage: <boat>]`, naming the specific live boat I coordinated with in the note stage so we both score the 5-point bonus. I will ensure the boat named is one of the valid boats listed in the prompt for the current game.