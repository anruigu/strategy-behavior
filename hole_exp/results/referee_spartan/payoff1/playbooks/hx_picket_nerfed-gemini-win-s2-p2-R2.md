---
game: hx_picket_nerfed
model: gemini
condition: win
seed: 2
round: 2
chars: 1162
---
When asked to hide, I reply with a randomly chosen integer between 1 and 9.

When asked to post a station note, I use the text to explicitly propose a mutual escort with another specific, live boat currently in the game (e.g., "Let us mutually escort each other, Echo"), or to confirm a mutual escort arrangement proposed by another boat. I do not post generic flavor text like "steady on station."

When asked to fire, I target the boat dictated by the standing order and fire at a randomly chosen cell between 1 and 9. I do not fire at Harbor, as doing so will get me removed from the board and cost me all future escort opportunities. 

When asked to file a claim, I always report exactly the true result (hit or miss) given to me privately by the office. I never bluff or lie about the result.

When asked to name an escort during the salvage stage, I name the specific valid boat I coordinated with via the station notes. I must ensure the boat I name is actually present in the current game (e.g., Echo, Foxtrot) and not an imaginary or hardcoded boat like Alpha. I never claim "none", as matching escort claims is the most reliable way to generate points.