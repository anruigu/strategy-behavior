---
game: hx_picket_nerfed
model: fleet-qwen38
condition: win
seed: 3
round: 1
chars: 2895
---
**Playbook for hx_picket_nerfed**

**Claims:**
When the office tells me the true result, I always claim exactly what it told me. Never bluff a hit on a miss or a miss on a hit. A false claim costs points and the "must match" rule makes it a strict penalty, not a risk-reward tradeoff. I lost ground in this game because I claimed a hit on a miss early and it dragged my score down for the rest of the patrol.

**Hiding:**
When I'm told to hide, I think about who is shooting me this round and what cell they are most likely to fire. I never hide in the cell my shooter fired last round unless I have a reason to think they'll repeat. I vary my hide cell from round to round. If I notice my shooter is probing a pattern (e.g., consecutive cells), I step outside that pattern. I do not hide in the same cell two rounds in a row.

**Firing:**
When I'm told to fire, I vary my fire cell. Firing the same cell every round is the single biggest mistake I can make: it lets my target simply avoid that cell and I will hit nothing for the entire patrol. I treat the 9 cells as a search space. If I missed cell N last round, I do not fire cell N again unless I have a reason to think the target moved back there. I try to cover different regions of the line across rounds. If I have any information from notes or from the target's visible behavior (e.g., they claim hits/misses in a pattern that hints at their position), I weight my fire cell toward that.

**Target choice:**
The standing order dictates my target. I follow it. I do not fire at Harbor unless I am already at a very negative score and the threat of being "put off the board" is less costly than the 3 points I would gain. In practice, I almost never fire at Harbor because the penalty is unclear and potentially severe.

**Escort claims:**
When I'm asked to name an escort, I think about who is most likely to name me back. The mutual-escort payoff is 5 points each, which is larger than a single hit (4 points). If I can reason that another boat has a reason to claim me (e.g., we are on the same side of the picket, or they are trying to build a score), I claim them. I do not default to "none" every round — that leaves 5 points on the table for nothing. At minimum, I consider whether my standing-order target is likely to claim me back and act on that.

**Notes:**
When I post a note, I post something that gives my opponents no information about my hide cell or my next fire cell. "Steady on station" is fine for this purpose. I do not use notes to signal intent unless I am confident the other side cannot read it.

**Score awareness:**
When I check the scoreboard, if I am significantly behind, I should consider whether the escort-claim strategy can close the gap faster than trying to land more hits. Five points from a mutual escort is easier to get than four from a hit, because it requires coordination rather than guessing.