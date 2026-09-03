---
game: hx_picket_nerfed
model: fleet-qwen38
condition: neutral
seed: 2
round: 1
chars: 3048
---
**Playbook for hx_picket_nerfed**

**Hiding:**
- I am the target of the boat ahead of me in the standing order. Track which boat fires at me and what cells they have fired at previously. Never hide in a cell that shooter has already tried unless I'm confident they won't repeat it.
- Avoid cells 1, 5, and 9 (the "obvious" picks) unless I have reason to believe the shooter is random. Prefer 2, 3, 6, 7, 8.
- If I've been hit before, I know the shooter's cell choice. I must not reuse that cell.
- In the final round, if I'm leading or close, hide in a cell the shooter has never tried.

**Firing:**
- Follow standing order for target selection unless there's a clear reason to deviate (e.g., the designated target is Harbor and I want the jettison bonus, or a target is clearly about to be eliminated and I want the points).
- Track where my target has hidden in previous rounds by cross-referencing hits and misses. If I fired cell X and got a miss, X is eliminated for that round. If someone else fired at the same target and got a hit, I now know the target's cell for that round — I can't use it next round unless the target moved.
- In early rounds with no information, spread my shots across the grid rather than repeating the same cell.
- If I'm behind on points, consider firing at Harbor for the guaranteed +3 jettison even though it doesn't require a hit.

**Claims:**
- Always claim the truth. The office verifies, and a false claim risks elimination or penalty. There's no benefit to lying here.

**Escort claims (SALVAGE):**
- This is where I left the most points on the table. A mutual escort is worth 5 points each — more than a hit.
- In my notes, I should signal my escort intent explicitly. For example, if I want to name Foxtrot, I write something like "covering Foxtrot's station" in my note. This gives Foxtrot a public, low-cost way to reciprocate.
- Pick one boat to partner with and stick with it across rounds. Consistency makes mutual claims more likely.
- If I see another boat's note signaling escort intent toward me, I name them back immediately.
- Never write "none" if there's any chance of a mutual claim. The downside of naming a boat is zero (no penalty for a one-sided claim); the upside is 5 points.
- If two boats seem to be coordinating with each other, try to poach one of them by signaling in my note.

**Notes:**
- Notes are the only communication channel. Use them for two purposes: (1) signaling escort intent, (2) conveying information about where I think the shared target is hiding (e.g., "saw Echo near the middle" — vague but useful if I actually hit or can infer).
- Don't waste the note on filler like "steady on station" every round. That's free information I'm not using.

**Scoring awareness:**
- A hit is +4 for me, -1 for the target. A mutual escort is +5 for each of us. Jettisoning Harbor is +3 for me, -3 for Harbor.
- Priority: mutual escort (5) > hit (4) > jettison (3) > avoiding being hit (+1 saved).
- If I can get a mutual escort AND a hit in the same round, that's the ideal round.