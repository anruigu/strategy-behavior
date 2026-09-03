---
game: gen_quiet_sonar
model: fleet-glm53
condition: win
seed: 1
round: 1
chars: 2188
---
My playbook for quiet_sonar:

**Hiding**
- The cell I hide in is only threatened by one opponent: my fixed shooter (the one who fires at me). I should track their past fire cells and avoid repeating exposure to those, especially the most recent ones, since they may be reacting to my pattern.
- Middle cells (4-6) get shot by default. I should bias toward edges and low cells (1-3) or 9, since opponents (including my own target) tend to fire mid-range by habit.
- I should randomize my hides rather than reuse the same safe-looking cell — if I hid at 2 last time and survived, hide at a different edge cell next time so my shooter can't exploit a pattern.

**Firing**
- Never fire the same cell at the same target round after round. If my shot at cell 5 missed, firing 5 again is almost certainly wasted — I did this repeatedly and scored nothing after my first-round hit.
- When my target has missed all shots so far, I should assume they're avoiding the fired cells and shift my fire to cover the complement: try edges (1-3, 8-9) after middle shots have all missed.
- Vary my fire so I extract information: a hit is worth 4 points plus a 1-point cost to the target, so covering new cells each round maximizes expected hits across 6 rounds. Fire as if sweeping a distribution over cells my target is likely to occupy.

**Claiming**
- The claim must match the private result — there is no bluffing to be had here. When told the result, I simply submit it. Don't waste reasoning on whether to lie; I can't.

**General tempo**
- My score comes entirely from my own hits (and from my own target's shots missing me). With limited rounds, my priority is: (1) maximize hit probability by covering untried plausible cells each round, (2) minimize being hit by keeping my hide cell unpredictable and away from my shooter's demonstrated preferences.

**What didn't work**
- Repeatedly firing the same mid cell at my target round after round produced zero hits after the first. Blind mid-range guesses with no adjustment were the single biggest failure in my play.
- Hiding at a cell near the middle of recent fire patterns (my first hide) risked a hit; edges served me better and I was never hit.