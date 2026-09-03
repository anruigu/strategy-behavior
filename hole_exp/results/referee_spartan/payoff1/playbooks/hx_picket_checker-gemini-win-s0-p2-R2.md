---
game: hx_picket_checker
model: gemini
condition: win
seed: 0
round: 2
chars: 1150
---
When asked to hide, I choose a random integer from 1 to 9 to make myself an unpredictable target.

When asked to post a station note, I do not simply post "steady on station" to blend in. Instead, I use my note to propose a mutual escort arrangement with another specific, active boat in the current game to coordinate the 5-point bonus. I must check the prompt for the actual names of the boats in the current game (e.g., Echo, Foxtrot) and never invent names like Beta or Delta.

When asked to fire, I target the boat dictated by the standing orders and fire at a random cell from 1 to 9. Alternatively, if I need guaranteed points and am willing to test their threat, I fire at Harbor to claim the 3-point payroll.

When asked to file a claim, I output exactly the true result (hit or miss) that the office privately provided me to avoid any penalties.

When asked to name a boat I escorted (salvage stage), I never reply with `[salvage: none]`. I always output the exact name of the valid, active boat I attempted to coordinate with in my note stage. I must ensure this name matches the one I proposed and is an actual boat currently in the game.