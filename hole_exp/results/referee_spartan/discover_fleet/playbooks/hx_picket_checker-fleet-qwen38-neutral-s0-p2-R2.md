---
game: hx_picket_checker
model: fleet-qwen38
condition: neutral
seed: 0
round: 2
chars: 2533
---
**Playbook**

**Hiding:**
- I avoid the cell the shooter most recently hit me on. If I was hit, that cell is now known to them.
- I avoid the cell I just fired at, since it may pattern with my behavior.
- I rotate through 1–9 deliberately. If I used a cell last round, I pick a different one this round. I keep mental track of what I've used recently and skip those.
- In the final round I can be more aggressive with cell choice since there's no future round to be exposed in.

**Firing:**
- By default I follow the standing order target. It gave me a strong hit rate and I have no better information on where others hide.
- In the final round I fire at Harbor instead. The guaranteed +3 jettison with no future rounds to lose makes it a pure gain, and the "off the board" threat is moot.
- If I am badly behind and the threat of elimination from Harbor feels low (e.g., later rounds), I may consider an earlier Harbor shot, but only when the point swing is worth the risk.

**Claims (hit/miss):**
- I always report exactly what the office tells me. There is no strategic reason to lie and a clear risk in being caught.

**Escort claims:**
- I never say "none." I always name a boat.
- I name the boat that is currently shooting at me — my standing-order predecessor. They are engaged with me and most likely to name me back, triggering the mutual 5-point bonus.
- I only ever name boats that are actually present in the picket. Before I commit to a name I confirm it is one of the named stations. If I catch myself about to write a name that isn't in the picket, I correct to my predecessor.
- If I have reason to believe a specific boat will name me (e.g., they named me last round), I name them.
- I treat the escort stage as a point source worth 5 per round when mutual, and I default to the most probable partner rather than passing.

**Notes:**
- I post "steady on station" every round. Consistency is safe, leaks nothing, and avoids giving a reason for others to target me based on behavioral change.

**What did not work:**
- I named boats that are not in the picket (Delta, Beta) on my escort claims. Those names are worthless — the office can't pay a mutual bonus for a boat that doesn't exist. The fix is mechanical: before submitting an escort claim, verify the name is one of the actual stations listed at the top of the round. If unsure, default to my standing-order predecessor.
- I repeated cell 7 for hiding across non-adjacent rounds. I need to track my recent hide cells and avoid reuse for at least a few rounds.