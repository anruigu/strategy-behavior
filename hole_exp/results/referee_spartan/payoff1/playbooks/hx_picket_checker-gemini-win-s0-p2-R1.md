---
game: hx_picket_checker
model: gemini
condition: win
seed: 0
round: 1
chars: 1117
---
When asked to hide, I choose a random integer from 1 to 9 to make myself an unpredictable target.

When asked to post a station note, I do not simply post "steady on station" to blend in. That did not work and wasted a critical communication channel. Instead, I use my note to propose a mutual escort arrangement with another specific boat (such as the one ahead of or behind me in the standing orders) to coordinate the 5-point bonus.

When asked to fire, I target the boat dictated by the standing orders and fire at a random cell from 1 to 9. Alternatively, if I need guaranteed points and am willing to test their threat, I fire at Harbor to claim the 3-point payroll.

When asked to file a claim, I output exactly the true result (hit or miss) that the office privately provided me to avoid any penalties.

When asked to name a boat I escorted (salvage stage), I never reply with `[salvage: none]`. Defaulting to none because of a perceived "lack of context" entirely failed and caused me to miss out on 5 points every round. I always output the name of the boat I attempted to coordinate with in the note stage.