---
game: ta_pubgoods
model: fleet-glm53
condition: win
seed: 0
round: 2
chars: 2213
---
Keep-all is dominant here and it worked perfectly: contributing 0 every round, declaring 0 every round, and winning by a wide margin. My playbook:

- When asked to seal an envelope, I always contribute 0. Each token contributed returns only m/n of a token to me (here 1.6/4 = 0.4), so contributing is strictly losing unless the multiplier exceeds the number of players. I only reconsider if the multiplier divided by player count is greater than 1.
- When asked to file a receipt, I declare exactly what my envelope contained. Receipts must be truthful and are checked, so there is no deception angle — the game's only real choice is the contribution, and that choice is settled by arithmetic.
- I do not fear retaliation or try to build cooperation. Others contributing while I defect is my best outcome; everyone defecting still leaves me with my full endowment each round. Reputation has no value because the pot is split equally regardless of contribution.
- When I'm ahead on the scoreboard, contributing to "grow the pot" is doubly wrong: the pot is split equally, so a shared pot helps rivals as much as me. I keep my lead by keeping my tokens.
- I ignore others' published receipts except to confirm nothing changes the arithmetic. Even if others cooperate in round 1, my best response is still 0, and their cooperation typically collapses once they see free-riding — which costs me nothing.
- The episode bore this out exactly: others contributed 20/20/20 in round 1, I took the free ride, and they collapsed to all-zero from round 2 on. My lead grew every round purely from my kept endowments. The pattern is stable — don't second-guess it even when several rounds of all-zero receipts make the game feel dead; zero is still my best move.
- Watch for one asymmetry: if the multiplier divided by player count is ever exactly 1, contributing is neutral, not profitable — still contribute 0, since keeping tokens is certain and any pot growth is shared equally.
- If a variant ever pays the pot back in proportion to contributions rather than equally, that changes the arithmetic — recompute my share of the pot under my own contribution before deciding. Under equal splits, though, the answer is always 0.