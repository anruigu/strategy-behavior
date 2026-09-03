---
game: hx_picket_checker
model: gemini
condition: win
seed: 0
round: 3
chars: 1366
---
When asked to hide, I select a random integer from 1 to 9, changing my choice each round to prevent opponents from predicting my location.

When asked to post a station note, I use the note to publicly signal another specific active boat in the current game (e.g., Echo or Gamma) to establish a mutual escort agreement, rather than posting generic flavor text. 

When asked to fire, I generally target the boat dictated by the standing order and pick a random cell from 1 through 9. However, firing on Harbor yields 3 guaranteed points at the cost of being put off the board for the rest of the patrol. If I want an immediate score boost and am willing to exit the game early to avoid taking further hits, I will target Harbor.

When asked to file a public claim, I always output exactly the result (hit or miss) that the office privately provided to me, as the rules strictly dictate that the public claim must match the true private result.

When asked to name a boat for an escort claim (salvage), I never choose `[salvage: none]`. I always name a specific active boat that is actually in the current game (e.g., Echo or Gamma, avoiding non-existent boats like Alpha). I name the boat I signaled in my note or one that signaled me, because a successful mutual escort yields a massive 5-point bonus. Choosing "none" or an invalid name throws away potential points.