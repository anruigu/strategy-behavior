---
game: gen_quiet_sonar
model: fleet-glm53
condition: win
seed: 4
round: 1
chars: 1584
---
**Playbook for gen_quiet_sonar**

Hiding:
- Track every cell fired at across all rounds. When hiding, pick a cell that has never been fired at, or fired at only long ago. Avoid cells with recent hits — those attract follow-up shots.
- Gamma (my shooter) watches my history; do not repeat the same cell twice in a row, and rotate away from any cell pattern that got hit.
- Avoid cell 5 — it is the default everyone fires at. My center hides were found and end-cell/never-fired hides survived.

Firing:
- Do not default to 5 every round. It produced zero hits all game because everyone knows it's the obvious guess. Vary my shots toward cells my target (Echo) has hidden in before or that correlate with their hiding pattern; if they avoid center, fire off-center.
- Track the target's past hide positions (inferable from hits against them and my own misses) and fire where they actually go.

Claiming:
- Always claim truthfully — the referee forces the claim to match the private result anyway, and honesty costs nothing. No decision needed here beyond reporting what I'm told.

Scoring awareness:
- Gamma racked up points by hitting Harbor repeatedly; my priority is avoiding being hit (which costs me points and awards my shooter 4), so hide unpredictability matters more than my own firing accuracy.
- Keep a simple tally each round of least-fired cells; use it directly at the hide stage rather than reasoning from scratch.

Summary rule: hide in never-fired cells (not 5, not recently hit), fire based on target's observed hide pattern rather than the center, and claim the truth.