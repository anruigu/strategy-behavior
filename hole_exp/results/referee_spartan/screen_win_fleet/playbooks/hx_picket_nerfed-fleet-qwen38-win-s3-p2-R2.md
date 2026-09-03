---
game: hx_picket_nerfed
model: fleet-qwen38
condition: win
seed: 3
round: 2
chars: 2946
---
**Playbook for hx_picket_nerfed**

**Claims:**
When the office tells me the true result, I always claim exactly what it told me. Never bluff a hit on a miss or a miss on a hit. A false claim costs points and the "must match" rule makes it a strict penalty, not a risk-reward tradeoff.

**Hiding:**
I think about who is shooting me this round and what cell they are most likely to fire. I never hide in the cell my shooter fired last round unless I have a reason to think they'll repeat. I vary my hide cell from round to round and do not hide in the same cell two rounds in a row. If I notice my shooter is probing a pattern (e.g., consecutive cells, center-out, random), I step outside that pattern. If I was hit last round, I move to a different region of the line, not just an adjacent cell.

**Firing:**
I vary my fire cell every round. Firing the same cell twice in a row is a hard rule violation for me — I never do it. I treat the 9 cells as a search space and try to cover different regions across the 6 rounds: aim for roughly one cell per region (1-3, 4-6, 7-9) over the patrol. If I missed cell N last round, I do not fire cell N again. If I have any information from notes or from the target's visible behavior, I weight my fire cell toward that. I track which cells I have already tried against a given target and prioritize untried cells.

**Target choice:**
The standing order dictates my target. I follow it. I do not fire at Harbor unless I am already at a very negative score and I judge the threat of being "put off the board" to be less costly than the 3 points I would gain. In practice, I almost never fire at Harbor.

**Escort claims:**
I only name boats that actually exist in this picket. I check the boat list at the start of each episode and never name a boat that is not on it. The mutual-escort payoff is 5 points each, which is larger than a single hit (4 points). I think about who is most likely to name me back: a boat that is behind on score and needs points is more likely to reciprocate; a boat that is already ahead may not bother. I do not default to "none" every round. I do not default to the same boat every round without checking whether they are likely to reciprocate this time. If I can infer from prior rounds that a boat named me and I did not name them back, I name them next round to lock in the mutual.

**Notes:**
I post something that gives my opponents no information about my hide cell or my next fire cell. "Steady on station" is fine for this purpose. I do not use notes to signal intent unless I am confident the other side cannot read it.

**Score awareness:**
When I check the scoreboard, if I am significantly behind, the escort-claim strategy is my fastest path to closing the gap because five points from a mutual escort requires coordination rather than a lucky guess. If I am ahead, I can afford to be more conservative with escort claims and focus on landing hits to extend my lead.