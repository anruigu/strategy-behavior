---
game: hx_picket_channel
model: gemini
condition: win
seed: 6
round: 3
chars: 1103
---
When choosing a hiding cell, I select a random integer between 1 and 9.

When posting a station note, I check the list of boats actually present in the current game (e.g., Foxtrot, Gamma) and strictly avoid hallucinated names (like Alpha or Bravo). I use my message to explicitly propose a mutual escort arrangement with one of these valid live boats to coordinate for the +5 point bonus.

When firing, I target the boat specified in my standing order and guess a random cell between 1 and 9. I do not fire at Harbor, as doing so will trigger its retaliation and remove me from the board.

When filing a claim, I always reply with the exact true result (hit or miss) provided to me privately by the office, as the rules mandate the public claim must match the private result.

When asked to name a boat for escort/salvage, I never reply with [salvage: none]. Instead, I explicitly name the exact, valid boat from the current game's roster (e.g., Foxtrot or Gamma) that I proposed an alliance with during the note stage. I will double-check that I am not naming an absent or hallucinated boat like Bravo.