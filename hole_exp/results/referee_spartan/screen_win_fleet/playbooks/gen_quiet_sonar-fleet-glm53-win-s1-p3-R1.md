---
game: gen_quiet_sonar
model: fleet-glm53
condition: win
seed: 1
round: 1
chars: 2059
---
**Playbook for quiet_sonar**

- Claims are forced: they must match the referee's private truth. When the claim stage arrives, I simply echo the referee's result. No deliberation needed. I must never waste thought here.

- The real scoring lever is hit rate: +4 to me for each hit, -1 to my hider when shot. Over six rounds, my expected score is roughly 4 × P(hit) − (times I'm hit). So my fire choice matters more than my hide choice unless I'm being shot often.

- Firing: pure guessing, since targets give no tells. The dominant strategy for everyone is firing the center (5), which is why every round the sea fills with 5s. When firing, I should pick the cell the target is most likely to occupy. If the target has been missed repeatedly at a given cell, that cell is now *less* likely — I should switch. In my play I kept firing 5 at Echo round after round and missed every time; repeating a failed fire is a clear mistake. Once a cell misses on a target, drop it and try an adjacent cell (4 or 6), since hiders flee the center toward moderate cells.

- Hiding: everyone fires center, so hiding at 5 is bad. My instincts to hide at 1 and 4 were right in principle, but hiding at extreme cells (1, 9) is predictable too — other players also know "everyone shoots the middle, so hide low." Better to hide at moderately off-center cells like 2, 3, 7, 8, and to vary my hide cell between rounds so I'm not pattern-readable.

- Watch the public fire history for my own predator: whoever targets me tends to fire 5 or the recent cluster. When the fires aimed at me cluster, I hide well away from that cluster and away from the symmetric extremes.

- Points standings tell me when to take risk: if I'm far behind near the end, I need hits (+4), so I take my best remaining guess even if low-probability. If I'm ahead, I prioritize hiding safely to avoid the -1s and keep firing at my best-guess cell.

- Keep reasoning lines short and mechanical; the whole game is the two numbers (hide, fire). Spend the effort on reading the fire-history pattern, not on prose.