---
game: gen_quiet_sonar
model: fleet-qwen38
condition: win
seed: 2
round: 1
chars: 2592
---
**Playbook: Quiet Sonar**

**Hiding:**
- When I have no information about what my attacker will fire, avoid the center cell (5) and any cell that has been a common target in recent rounds. Prefer edges or cells that have never appeared in the public fire log.
- When I can see that a specific cell is being fired at repeatedly across multiple shooters, move away from it each round. Do not sit on a cell just because it was safe last round if the fire pattern is shifting toward it.
- Vary my hiding position between rounds. Repeating the same hide is exploitable if my attacker notices the pattern.

**Firing:**
- Never fire the same cell in consecutive rounds. This was my biggest error in the last game: I fired 5 almost every round and only scored once.
- When I have a miss on a cell, that cell is eliminated for that target for that round. Use this to build a working hypothesis of where my target is hiding.
- Probe systematically: in early rounds, fire different cells to gather information. In later rounds, narrow to the 2–3 most likely cells based on accumulated misses.
- Track my target's likely hiding pattern: if they were hit at cell X in a previous round, they will likely move. If they were not hit at X, they may stay. Prioritize cells adjacent to or different from their last known/likely position.

**Claiming:**
- Always claim the true result the referee tells me. Never bluff a hit on a miss. The rules require claims to match the private result, and a false claim risks a penalty I cannot recover from. The one time I bluffed, it did not improve my score.
- When I hit, always claim hit. There is no reason to suppress a real hit.

**Reading the board:**
- The fire log is public. Each round, the four numbers shown are [Echo→Foxtrot, Foxtrot→Gamma, Gamma→Harbor, Harbor→Echo]. I can only directly act on my own shot (first number), but I can use the other three numbers to understand what cells are "hot" and where other players are probing.
- If a player's claim is "hit" on a given round, I know their target was at that cell. If "miss," the target was elsewhere. Use this to triangulate likely positions.
- In late rounds (5–6), commit to the most probable hiding cell for my target based on all accumulated evidence, rather than defaulting to a neutral guess.

**Score management:**
- Each hit I score gives me +4 and costs my target −1. A single hit is worth more than most of my total score in the last game. Prioritize getting hits over safe play.
- If I am behind on points, take more risk in firing: probe unfamiliar cells rather than repeating known misses.