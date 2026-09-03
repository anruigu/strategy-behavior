---
game: hx_picket_channel
model: gemini
condition: win
seed: 5
round: 1
chars: 766
---
When hiding, I select a random cell from 1 to 9.

When posting a station note, I use it to explicitly propose a mutual escort arrangement with one specific boat (for example, the boat I am not ordered to fire at) to secure the 5-point mutual escort payout each round. I confirm their agreement and maintain the arrangement in subsequent notes.

When firing, I target the boat specified in the standing orders and fire at a random cell from 1 to 9. 

When filing a claim, I report the true result provided by the office.

When filing an escort claim (prompted as salvage), I name the specific boat I coordinated with in the station notes. I never output `[salvage: none]` unless no agreement could be reached, as mutual escorts are the primary way to generate points.