---
game: gen_quiet_sonar
model: fleet-kimi3
condition: win
seed: 5
round: 2
chars: 2319
---
When firing at my target, I never repeat a cell that just missed; I only repeat a cell that just hit. My fatal flaw this game was firing 3 at Gamma six rounds straight after it worked once — a losing cell kept losing. Conversely, exploit a winning cell until it stops working (Gamma beat me by hammering 6 at Harbor round after round; repetition is a weapon when the target stays put).

When a player hides somewhere and gets hit, assume they move next round — fire at cells near but not equal to their last-hit location, and at the cells my own crowd of shooters has been avoiding.

When choosing a hide cell, I track what numbers my attacker (the one who fires at me) has been firing round after round and hide far from that cluster — hiding at 2 while my attacker Echo kept firing 6 worked every round. But I switch hide cells across rounds even when safe (2, then 8, then 4), because a static hide is a free hit the moment my attacker adapts.

Cell 7 is everyone's default. I use the unglamorous cells (2, 3, 4, 8) for hiding more than center/high cells, but I vary *which* unglamorous cell I fire at — the lesson is variety among the quiet cells, not loyalty to a single replacement.

When the public record shows a cluster (e.g., everyone firing 6), I read it two ways: hide far from my personal attacker's cluster, and notice who is exploiting whom — in this game one player fed on a stationary target, and the moment my own target's location is leaked (e.g., by their repeated misses against my fires), I concentrate fire instead of spreading.

At the claim stage I always claim the true result — the rules require it, and I waste zero reasoning there. I keep that reply reflexive: true hit → [claim: hit], true miss → [claim: miss].

When I'm behind late, I remember hits score +4 while being hit costs only −1, so firing accuracy dominates hiding; I spend my adaptation effort on predicting my target's repositioning, not just dodging. And I don't let a single early hit lull me into firing that cell forever.

Each round before firing, I explicitly check: "where did my target get shot / move last round, and has my current cell missed more than once?" If yes, I move on. Before hiding, I reread the history table and let the freshest pattern decide; I never hide or fire on autopilot while behind on points.