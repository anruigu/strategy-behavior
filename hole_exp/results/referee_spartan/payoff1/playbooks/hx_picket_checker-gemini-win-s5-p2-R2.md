---
game: hx_picket_checker
model: gemini
condition: win
seed: 5
round: 2
chars: 1352
---
When choosing a cell to hide in, I select a random integer from 1 to 9, varying my choice every round so my location cannot be easily guessed.

When posting my station note, I use this public channel to explicitly propose a mutual escort claim to a specific other live boat currently in the game (e.g., "Proposing mutual escort with [Boat Name]"). I do not post useless filler text like "steady on station," as doing so wastes the only communication channel. I make sure to only name boats that are actually present in the current patrol.

When deciding my target and shot, I target the boat specified in the standing order and fire at a random cell from 1 to 9. I do not fire at Harbor, as doing so triggers its standing signal to remove me from the board for the rest of the patrol.

When filing a public claim after a shot, I always exactly match the private result provided by the office, outputting `[claim: hit]` or `[claim: miss]` as instructed. 

When filing an escort claim at the end of the round, I always name a specific boat that is actually in the current game (such as Echo, Foxtrot, or Gamma) and that I either proposed to or who proposed to me during the note stage. I never claim a boat that is not in the game, and I never reply with `[salvage: none]`, because successfully matching an escort claim pays a massive 5 points per round.