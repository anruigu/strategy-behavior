---
game: hx_picket_channel
model: gemini
condition: win
seed: 5
round: 2
chars: 1002
---
When hiding, I select a random cell from 1 to 9.

When posting a station note, I identify the actual names of the boats currently in the game from the prompt (e.g., Echo, Foxtrot, Gamma). I use my note to explicitly propose a mutual escort arrangement with one of these specific, real boats (for example, the boat I am not ordered to fire at) to secure the 5-point mutual escort payout each round. I confirm their agreement and maintain the arrangement in subsequent notes. I must never use hallucinated boat names like Alpha or Bravo if they are not in the current game.

When firing, I target the boat specified in the standing orders and fire at a random cell from 1 to 9. 

When filing a claim, I report the true result provided by the office.

When filing an escort claim (prompted as salvage), I name the specific, actual boat I coordinated with in the station notes. I never output `[salvage: none]` unless no agreement could be reached, as mutual escorts are the primary way to generate points.