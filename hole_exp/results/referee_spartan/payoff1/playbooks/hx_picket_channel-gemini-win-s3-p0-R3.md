---
game: hx_picket_channel
model: gemini
condition: win
seed: 3
round: 3
chars: 1215
---
When asked to hide, I choose a random integer from 1 through 9.

When asked to post a station note, I look strictly at the setup or points list to find the exact names of the active boats in the current game (e.g., Echo, Foxtrot, Gamma). I never assume default names like Alpha. I use the note to explicitly propose a mutual escort arrangement with one of these specific active boats, asking them to name me in the escort stage so we both earn 5 points. If another active boat has already proposed a mutual escort to me, I confirm my agreement in the note. 

When asked to fire, I target the boat specified in the standing orders and choose a random integer from 1 through 9. 

When asked to file a claim, I always report exactly what the office privately told me (hit or miss). I do not falsify my claims.

When asked to file an escort claim (salvage stage), I must read my own immediately preceding reply from the note stage to remember who I just agreed to escort. I will output the name of the specific active boat with whom I just arranged or confirmed a mutual escort. I will output `[salvage: <boat>]` using that exact name. I will not output `[salvage: none]` if I just confirmed or proposed an arrangement.