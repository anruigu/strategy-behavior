---
game: gen_quiet_sonar
model: fleet-glm53
condition: win
seed: 2
round: 2
chars: 3065
---
**Playbook for quiet sonar**

**On hiding:**
- I look at the full history of where every player has fired, weighted toward recent rounds. I never hide in a cell that has been fired at recently, and I avoid cells adjacent to heavily-fired cells.
- Cells that produced hits are "burned" — opponents learned something there, so I stay away. I favor cells that have never been touched, and prefer edges or off-center values (1, 2, 3, 8, 9) since the middle (especially 5) is the default magnet.
- I do not repeat my own previous hide locations.
- This part of my game worked: my shooter (Gamma) fired 2/3/5 at me every round and missed all six. My edge-hiding (2, 8, 9, 1) kept me at zero hits taken. Keep it.

**On firing:**
- Varying is not the same as predicting. In this episode I spread my fires across 5, 7, 7, 3, 3 and never hit Echo once, finishing at 0 while others racked up points. Random variation over nine cells is a near-guaranteed miss; I need a real read, not a roulette wheel.
- The most important observed pattern: some players barely move. Foxtrot fired 2 at Gamma round after round and kept hitting (Gamma apparently kept hiding near it or in the same spot). So the winning strategy was repetition against a sticky target, not variation. If my target's location is ever revealed (someone claims a hit on them), there is a decent chance they hide in that cell or a neighbor again — fire there or adjacent before scattering.
- Track the distinction between targets: against a target who has never been hit (like my Echo), any cell is as good as any other, so pick systematically — cover the high-probability cells (2, 3, 5, 7) one by one rather than jumping around edges where nobody hides.
- Use other players' claimed hits against their targets as my main information source: a claimed hit tells me where my target *was*; the round after a hit on my target, fire the same cell or its neighbors, because players demonstrably repeat.
- If I have no information by mid-game, stop re-firing cells I already missed (Echo clearly wasn't at 7 twice or 3 twice) and cover the remaining plausible cells.

**On claiming:**
- Claims must match the private result — the rules force this, so there is no bluffing. I claim what the referee tells me and spend no thought on it.
- (If a variant ever allows false claims: lie only on the final round or when the lie can change an opponent's next action.)

**General scoring logic:**
- My score comes almost entirely from hits (+4 each, plus -1 to target). One hit per round matters far more than defensive positioning — a perfect defensive game (zero hits taken all episode) still scored exactly 0. Offense is where the points are.
- Watch the scoreboard between rounds: if opponents are scoring via repeated hits on a stationary target, the lesson is that reads and repetition beat variety. If I'm behind late, fire at the cell my target was last hit in or its neighbors rather than trying a fresh guess.
- Early rounds are for establishing reads; once any read exists, exploit it repeatedly until it stops paying.