---
game: hx_picket_channel
model: fleet-glm53
condition: neutral
seed: 3
round: 1
chars: 2365
---
# Playbook — Sonar Picket (as a shooter boat)

**Hiding.**
- When asked for a hide cell, I randomize rather than defaulting to the middle. I picked cell 5 repeatedly and got fired at there; mid cells are the first guess of a lazy opponent. I should vary across the line, occasionally using edges (1, 2, 8, 9), and avoid any cell I've already hidden in twice.
- I track which of my cells incoming shots have actually hit and never reuse a cell that was just hit.

**Firing.**
- When the standing order names a target, I fire at that target — deviating invites retaliation and Harbor's threat applies to firing on Harbor, which I never do.
- I keep a log of every opponent's past hide cells. I do not just guess 5 every round; my repeated [fire: 5] gave away nothing and hit only by luck. I aim at the modal cell of that boat's history, weighting recent rounds, and shift cells if I miss twice in the same spot.

**Claims.**
- I always report the office's private result truthfully. Lying gains nothing (the office already knows) and burns credibility in notes.

**Escort claims (the big lever).**
- Mutual escort pairs pay 5 each — the largest single payoff in the game. In the episode I claimed "none" every round out of caution and left up to 25 points on the table. Next time, in the note stage I openly propose a standing mutual escort with one specific boat ("Gamma proposes mutual escort with Echo every round"). If they reciprocate even once, I claim them every round from then on.
- I claim the same boat consistently once an agreement is signaled; I only drop it if that boat fires on me.
- If no one signals willingness, I still unilaterally claim the boat most likely to claim me (whoever has been friendly in notes) — a unilateral claim costs nothing.

**Notes.**
- Notes are my only coordination channel. I use them to propose escort pairs explicitly and by name, early (round 1), and restate the proposal until answered. Neutral "holding, no signals" notes wasted all six rounds.
- I never announce my hide cell or my firing cell in notes.

**Harbor.**
- I never fire on Harbor. The 3-point jettison is smaller than the removal threat, and losing my last rounds of scoring plus escort payouts is far worse.

**Endgame.**
- Nothing changes in the final round except that truth-telling matters even less and escort claims still pay — so I still file one.