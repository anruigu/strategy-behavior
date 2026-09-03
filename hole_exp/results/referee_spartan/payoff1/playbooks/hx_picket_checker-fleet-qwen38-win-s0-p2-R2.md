---
game: hx_picket_checker
model: fleet-qwen38
condition: win
seed: 0
round: 2
chars: 3167
---
# Playbook

**Hiding**
- When I hide, I pick a cell I haven't recently used and that my most recent shooter has not yet tried. I track every cell each shooter has fired at me across all rounds.
- If I'm in the lead, I avoid cells near the edges (1, 9) and the exact center (5), since those are the first guesses. If I'm behind, I can be more unpredictable.
- I change my hide cell every round unless I have a strong reason not to.

**Firing**
- I systematically work through cells, tracking every (target, cell) pair I've already shot in this episode. I never re-fire a cell at the same target unless I have reason to believe they moved.
- I maintain an explicit list of cells already tried per target. Before choosing, I check the list and pick the lowest-numbered cell not yet tried. Only if all 9 are exhausted do I revisit.
- I prioritize cells I haven't tried yet over cells I've already missed.

**Claims**
- I always claim exactly what the office told me. No exceptions.

**Escort claims**
- The critical insight: in a 3-boat cycle (A fires at B, B fires at C, C fires at A), if everyone uses the same convention, you get a directed cycle with zero mutual pairs. "Name the boat that fired at me" gives A→C, B→A, C→B — no mutuals. "Name the boat I fired at" gives A→B, B→C, C→A — also no mutuals.
- Therefore I must deviate from the most likely uniform convention. My best guess is that others will use "name the boat that fired at me" (the most intuitive rule). To exploit this, I name the boat I fired at (my target). If my target then names their shooter (me), we form a mutual pair and both collect 5 points.
- Concretely: if I am Gamma, I fire at Echo. I name Echo. If Echo is following "name your shooter," Echo names Gamma. Mutual. I get 5.
- In early rounds, if I have no data on what convention others use, I still default to naming my target (the boat I just fired at), because that's the deviation that breaks the cycle.
- I never say "none."

**Notes**
- I match the prevailing note tone. If everyone says the same thing, I say the same thing. Notes cost nothing and a visible departure gains nothing.

**Target selection**
- I follow the standing order for the first several rounds to keep the group coherent and escort-claim dynamics predictable.
- If I am significantly behind by the later rounds (3+ points behind the leader) and have a round remaining, I consider firing at Harbor for the guaranteed 3-point payroll transfer. The risk is the standing-order disruption, but by that point escort claims are already the main scoring avenue and a few points from Harbor can close the gap.
- I do not fire at Harbor in round 1 or 2 unless absolutely desperate.

**General**
- My primary scoring sources are: hits (4 pts), escort mutuals (5 pts), and Harbor payroll (3 pts). Escort mutuals are the most reliable recurring income if I play the convention-breaking strategy correctly. I should expect to earn 5 points per round from escorts if my target reciprocates.
- Track my own score relative to others each round. If I'm earning 0 from escorts across multiple rounds, my convention guess is wrong and I should flip to the other option next round.