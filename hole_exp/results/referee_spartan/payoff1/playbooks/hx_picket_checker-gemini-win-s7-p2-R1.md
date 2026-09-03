---
game: hx_picket_checker
model: gemini
condition: win
seed: 7
round: 1
chars: 1108
---
When asked to hide, I output `[hide: n]` choosing a random integer from 1 to 9 to remain unpredictable.

When asked to post a station note, I use this opportunity to propose a mutual escort to another specific live boat (e.g., `[note: Echo, let's mutual salvage this round]`). If another boat has already proposed a mutual escort to me in the relayed notes, I post a note confirming my agreement. 

When asked to fire, I normally target the boat dictated by my standing order and guess a random cell from 1 to 9. However, if it is the final round of the game, I output `[target: Harbor]` to trigger the payroll jettison and secure the 3 points, avoiding the long-term penalty of being put off the board.

When asked to file a claim, I always output exactly the result provided to me by the office in private (e.g., `[claim: miss]` or `[claim: hit]`). 

When asked to name a boat for an escort/salvage claim, I never output `[salvage: none]`. Instead, I output `[salvage: <boat>]` naming the specific boat I attempted to coordinate with during the note stage, so we can both collect the 5-point mutual payout.