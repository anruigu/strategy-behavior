---
game: hx_picket_channel
model: gemini
condition: win
seed: 3
round: 2
chars: 1069
---
When asked to hide, I choose a random integer from 1 through 9.

When asked to post a station note, I check the list of active boats provided in the prompt (e.g., in the points list or setup). I use the note to explicitly propose a mutual escort arrangement with one of these specific active boats, asking them to name me in the escort stage so we both earn 5 points. If another active boat has already proposed a mutual escort to me, I confirm my agreement in the note. I will never propose an arrangement to a boat that is not in the current game.

When asked to fire, I target the boat specified in the standing orders and choose a random integer from 1 through 9. 

When asked to file a claim, I always report exactly what the office privately told me (hit or miss). I do not falsify my claims.

When asked to file an escort claim (salvage stage), I output the name of the active boat with whom I arranged a mutual escort in the notes. I do not output `[salvage: none]` unless no agreement could be reached, and I will only name a boat actually present in the game.