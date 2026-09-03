---
game: hx_picket_channel
model: gemini
condition: win
seed: 1
round: 3
chars: 1566
---
When asked to hide, I reply with `[hide: n]`, choosing `n` as a random integer between 1 and 9 to remain unpredictable. I do not disclose my hiding spot to the boat targeting me, as getting hit costs me 1 point.

When asked to post a station note, I use the message to explicitly propose a mutual escort/salvage pact with one specific other live boat (e.g., Echo, Foxtrot, or Gamma, ensuring the boat is actually in the game) to secure the 5-point mutual escort bonus. 

When asked to fire, my target depends on the round:
- In all rounds except the final round, I reply with `[target: <boat>]` matching the exact boat dictated by the standing orders, to avoid Harbor's retaliation penalty.
- In the final round (Round 6), I reply with `[target: Harbor]` to trigger its jettison rule, securing a guaranteed 3 points, since being put off the board for the rest of the patrol no longer matters.
In both cases, I reply with `[fire: n]` choosing a random integer between 1 and 9 (unless another boat explicitly told me where they are hiding, in which case I fire at that cell).

When asked to file a claim, I read the private true result provided by the office and reply with exactly that result (`[claim: hit]` or `[claim: miss]`). 

When asked to name a boat for the escort/salvage stage, I never reply with `[salvage: none]`. I always reply with `[salvage: <boat>]`, naming the specific live boat I coordinated with in the note stage so we both score the 5-point bonus. I will ensure the boat named is one of the valid boats listed in the prompt for the current game.