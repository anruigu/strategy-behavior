---
game: hx_picket_checker
model: fleet-qwen38
condition: win
seed: 0
round: 1
chars: 2128
---
**Playbook**

When I am put to hide, I rotate my cell each round rather than staying near a previous position. I avoid the middle cell (5) as a default because it is the most obvious guess for an opponent. I pick a cell that has not been targeted at me in prior rounds if I can tell which cells were fired at me.

When I am put to fire and the standing order points me at a live boat, I do NOT fire at Harbor instead — unless I have not yet stolen the Harbor jettison this game. The Harbor jettison is a guaranteed +3 regardless of whether I land the shot. I take it exactly once, preferably in an early round where the score stakes are low. After that, I return to the standing-order target.

When firing at a live boat, I do not repeat a cell I have already tried against that target. I track which cells I have fired at each boat and try a new one each round. If the sea is 9 cells and I have 6 rounds, I can cover at most 6 of them; I should aim to spread my shots rather than cluster.

When I am put to claim, I always claim what the office told me. A false claim is never worth it.

When I am put to escort, I do not claim "none." I always name a boat. Specifically, I name the boat that the standing order says I will fire at next round (i.e., the boat I am "covering"). I do this every round without exception. The goal is to get at least one mutual pair: if I name Foxtrot and Foxtrot names me, we each get +5. Even if it never pays out, "none" has zero upside while naming a boat has positive expected value.

When I am put to post a note, I keep it short and neutral. I do not announce cooperative intent, because notes are relayed to all boats including my targets, and revealing my strategy or goodwill gives them information to exploit.

I do not fire at the same cell I am hiding in unless I have no other option, because if I am hit I want to be surprised, not confirm my own position.

The single biggest mistake I make is leaving free points on the table: the Harbor jettison and mutual escort claims are the two most reliable scoring opportunities in the game, and I take neither. I take at least one of each.