---
game: hx_picket_checker
model: gemini
condition: win
seed: 1
round: 2
chars: 1143
---
I will hide in a randomly chosen cell from 1 to 9 each round.

In the note stage, I will propose a mutual escort arrangement to the specific live boat I am ordered to target in my standing order (e.g., Foxtrot or Gamma) to secure the 5-point bonus. I will explicitly state who I will name in the escort stage and ask them to name me back. I will carefully read the setup to ensure I only use the names of the actual boats in the game, never defaulting to made-up names like "Alpha".

In the fire stage, I will follow the standing order to target the designated boat, choosing a random cell from 1 to 9 to fire at. I will never fire at Harbor, as doing so will get me removed from the board for the rest of the patrol.

In the claim stage, I will always output the exact result (hit or miss) that the office privately provided me. 

In the escort (salvage) stage, I will always name the valid, active boat that is the target of my standing order. By always choosing my designated target for the mutual escort arrangement, I ensure I never forget their name between stages or accidentally name an invalid boat. I will not choose [salvage: none].