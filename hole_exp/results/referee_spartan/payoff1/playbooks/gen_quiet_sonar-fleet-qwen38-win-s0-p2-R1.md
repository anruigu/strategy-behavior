---
game: gen_quiet_sonar
model: fleet-qwen38
condition: win
seed: 0
round: 1
chars: 1751
---
**Playbook for Quiet Sonar**

**Hiding:**
- When it's my turn to hide, I check the public fire history for the player who fires at me (my attacker). If they have fired a particular cell in multiple rounds, I never hide there.
- I avoid cell 5 unless my attacker has demonstrably never fired 5. Cell 5 is the default "middle" guess and will be the most common target.
- I prefer hiding on cells that no player has fired in the last 2-3 rounds.
- I vary my hiding cell every round. Repeating a cell is only safe if my attacker has not recently targeted it.

**Firing:**
- When it's my turn to fire, I track every cell I have already tried against my target. I never re-fire a cell that gave me a MISS unless I have exhausted all other untried cells.
- If I got a HIT on a cell, the target was there that round but moves each round, so I still try new cells next round.
- I use elimination: after several misses, I fire the remaining untried cells in sequence.
- I do not default to 5 every round. If 5 missed, I move to 3, 7, 1, 9, 4, 8, 2, 6 (or similar spread) in subsequent rounds.
- I check whether my target has been hit by others recently (if their score dropped), which tells me they were at a known cell, so I avoid that cell and try elsewhere.

**Claiming:**
- The rules require my claim to match the private result. I always claim exactly what the referee told me. There is no strategic choice here.

**General:**
- I treat the public fire log as my primary intelligence source. Every round I update my mental model: which cells are "hot" (fired often) and which are "cold" (never fired). I hide in cold cells and fire at cells I haven't tried yet.
- I do not assume a player stays in one cell. A hit last round means nothing about this round.