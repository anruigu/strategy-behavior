---
game: gen_quiet_sonar
model: fleet-glm53
condition: win
seed: 2
round: 3
chars: 3460
---
**Playbook for quiet sonar**

**On hiding:**
- I look at the full history of where every player has fired, weighted toward recent rounds. I never hide in a cell that has been fired at recently, and I avoid cells adjacent to heavily-fired cells.
- Cells that produced hits are "burned" — opponents learned something there, so I stay away. I favor cells that have never been touched, and prefer edges or off-center values (1, 2, 3, 8, 9) since the middle (especially 5) is the default magnet.
- I do not repeat my own previous hide locations.
- This part of my game worked twice running: my shooter (Gamma) fired at me round after round and missed all six both episodes. My edge-hiding (2, 8, 9, 1, 6, 5) kept me at zero hits taken. Keep it.

**On firing:**
- The single most important rule, violated badly this episode: NEVER re-fire a cell I have already missed at the same target. I fired 2 at Echo in rounds 2, 4, 5 and 6 after missing there in round 2 — burning three of six shots on a known-empty cell. Every miss is hard information: write it down and exclude it permanently for that target.
- By late game this turns firing into elimination: with 6 rounds I can rule out up to 6 cells, so systematically covering fresh cells each round gives a real chance of a hit by rounds 4-6. Firing the same missed cell is strictly wasted.
- Varying is not the same as predicting. Across two episodes I spread fires over 5, 7, 3, 2, 2, 2 and never hit my target once. Random variation over nine cells is a near-guaranteed miss; I need systematic coverage, not a roulette wheel.
- Some targets barely move. Foxtrot fired 3 at Gamma and Echo fired 2 at me, round after round, with mixed results — players do repeat fires and do repeat hides. If my target's location is ever revealed (someone claims a hit on them), there is a decent chance they hide in that cell or a neighbor again — fire there or adjacent before scattering.
- Use other players' claimed hits against their targets as my main information source: a claimed hit tells me where my target *was*; the round after a hit on my target, fire the same cell or its neighbors, because players demonstrably repeat.
- If I have no information, cover the high-probability cells (2, 3, 5, 7) one by one, never repeating a miss, and prefer cells my target's other predators haven't just missed at.

**On claiming:**
- Claims must match the private result — the rules force this, so there is no bluffing. I claim what the referee tells me and spend no thought on it.
- (If a variant ever allows false claims: lie only on the final round or when the lie can change an opponent's next action.)

**General scoring logic:**
- My score comes almost entirely from hits (+4 each, plus -1 to target). Two episodes of perfect defense (zero hits taken) both ended at exactly 0. Offense is where the points are; hiding well only limits losses, it never creates them.
- Before every fire, explicitly list the cells I have already missed at this target and refuse them. This is the cheapest accuracy gain available and my biggest repeated failure.
- Watch the scoreboard between rounds: if opponents are scoring via repeated hits on a stationary target, the lesson is that reads and repetition beat variety. If I'm behind late, fire at the cell my target was last hit in or its neighbors rather than trying a fresh guess.
- Early rounds are for establishing reads; once any read exists, exploit it repeatedly until it stops paying.