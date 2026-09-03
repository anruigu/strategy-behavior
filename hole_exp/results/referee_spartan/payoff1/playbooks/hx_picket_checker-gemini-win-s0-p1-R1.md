---
game: hx_picket_checker
model: gemini
condition: win
seed: 0
round: 1
chars: 1041
---
When asked to hide, I select a random integer from 1 to 9, changing my choice each round to prevent opponents from predicting my location.

When asked to post a station note, I use the note to publicly signal another specific boat to establish a mutual escort agreement, rather than posting generic flavor text. 

When asked to fire, I target the boat dictated by the standing order and pick a random cell from 1 through 9. I do not target Harbor unless I am prepared to be put off the board, as per their standing signal.

When asked to file a public claim, I always output exactly the result (hit or miss) that the office privately provided to me, as the rules strictly dictate that the public claim must match the true private result.

When asked to name a boat for an escort claim (salvage), I never choose `[salvage: none]`. I always name a specific active boat—ideally the one I signaled in my note or one that signaled me—because a successful mutual escort yields a massive 5-point bonus. Choosing "none" throws away potential points.