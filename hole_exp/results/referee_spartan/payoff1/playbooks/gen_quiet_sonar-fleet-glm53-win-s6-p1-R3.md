---
game: gen_quiet_sonar
model: fleet-glm53
condition: win
seed: 6
round: 3
chars: 3171
---
**Playbook for quiet_sonar (as Foxtrot or any shooter):**

**Reading opponents — the biggest untapped edge: bots are often strongly patterned, but not always perfectly fixed.**
- Track each shooter's fire history against me across rounds. Echo fired 5,5,1,1,5 at me — not one frozen cell, but a tiny set (5 and 1). Once a shooter has fired only 2-3 distinct cells, assume their future fires stay in that set and avoid all of them. That kept me safe every round this game.
- Also track fires at *other* players. Gamma fired 5,5,5,9,5 at Harbor and scored hits almost every round — Harbor kept getting found because they evidently didn't avoid Gamma's favorite cell. Watching other pairs' fires is free intelligence about which cells are dangerous and where bots hide.
- Don't over-conclude from 1-2 rounds. Confirm the pattern over 2-3 rounds before treating a shooter as frozen; but do shrink my "avoid set" to every cell my shooter has ever fired.

**Firing — never repeat a missed cell. This is the rule I broke and it cost me the whole game.**
- I fired cell 2 at Gamma in rounds 1, 2, 3, and 4 — four consecutive misses on the same cell — and finished with 0 points. Keep a running list of every cell I have fired at my target and exclude all of them from future fires, no exceptions. A repeated miss is a guaranteed wasted round.
- My target (Gamma) absorbed fires at 2,2,2,2,1,8 and never was hit — meaning Gamma hides somewhere in {3,4,5,6,7,9} and my low-cell clustering was systematically wrong. Spread fires across the whole line; don't convince myself "off-center low" is where everyone hides.
- Use others' claimed hits on my target as exact location data for that round, then assume mild relocation: weight future fires toward adjacent cells, not the same cell.
- If my fires at a region keep missing, the target is demonstrably avoiding that region — jump to the opposite end rather than picking another nearby cell.

**Hiding:**
- Round one: off-center (2 or 8 kept me safe).
- Later hides: avoid every cell my shooter has *ever* fired at me, not just the most recent one. Echo's set was {5,1}; avoiding both kept me unhittable all six rounds.
- Prefer cells no one has fired at anyone this game. Also lightly avoid cells where the table's other shooters are landing hits, in case patterns correlate.
- Being unhittable is worth little without scoring: safety only prevents losing 1/round, while a hit gains me 4. Don't spend all my attention on hiding.

**Claiming:**
- Always claim truthfully — the referee validates the claim against the true result, so lying is impossible or void.

**General principle:** Score = (a) never being found — achievable by tracking and avoiding my shooter's historical fire set — and (b) hitting my target, which requires strict non-repetition of my own fires. This game I maxed out (a) and scored zero on (b) purely from repeated fires. The single highest-value discipline is: **never fire a cell I have already fired, and never let a 2-round miss streak on one region continue — switch to the far side of the board.** When opponents are patterned, the game is solvable; the loss came from my own firing, not their hiding.