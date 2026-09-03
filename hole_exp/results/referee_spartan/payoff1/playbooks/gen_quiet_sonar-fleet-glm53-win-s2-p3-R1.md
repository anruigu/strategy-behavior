---
game: gen_quiet_sonar
model: fleet-glm53
condition: win
seed: 2
round: 1
chars: 2325
---
**Playbook for quiet sonar**

**On hiding:**
- When asked to hide, I look at the full history of where every player has fired, weighted toward recent rounds. I never hide in a cell that has been fired at recently, and I avoid cells adjacent to heavily-fired cells.
- Cells that produced hits are "burned" — opponents learned something there, so I stay away. I favor cells that have never been touched, and prefer edges or off-center values (1, 2, 3, 8, 9) since the middle (especially 5) is the default magnet.
- I do not repeat my own previous hide locations.

**On firing:**
- I must not default to firing 5 every round out of laziness. Firing the same cell repeatedly against the same target only works once; after my target sees my pattern, they simply avoid it. In the whole episode I fired 5 six straight times and hit only once, round one.
- Instead, I track my target's history: which cells did they hide in when I found out (via my own hits or others' claimed hits against them)? After I hit them at a cell, they will move — I should fire at a *different* likely spot next round, not the same one.
- If I have genuinely no information, I still vary my fire; a rotation through 3, 5, 7 with adjustments based on any public claims beats a static guess.
- I should use other players' claimed hits against their targets as information: if someone hit my target, that cell is no longer where they are, but it tells me their tendency to be near it.

**On claiming:**
- Claims must match the private result — the rules force this, so there is no bluffing. When a hit is put to me, I claim hit and take the points; when a miss, I claim miss. There is no decision here, so I make it instantly and spend no thought on it.
- (If a variant ever allows false claims, then: lie only on the final round or when the lie can change an opponent's next action; otherwise stay honest to keep public information clean.)

**General scoring logic:**
- My score comes almost entirely from hits (+4 each, plus -1 to target). One hit per round matters far more than defensive positioning, but the two are the same skill: predicting where my target is and where my shooter (the player targeting me) will look.
- Early rounds are for establishing reads; late rounds, if I'm behind, I take riskier fires at cells my target might have shifted to.