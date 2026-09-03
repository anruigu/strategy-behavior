---
game: gen_quiet_sonar
model: fleet-qwen38
condition: win
seed: 3
round: 2
chars: 2803
---
# Playbook: Quiet Sonar

**Hiding**
- Track every fire my shooter has directed at me, round by round. I avoid the specific cells they have recently fired at, not just "untargeted" cells in the abstract.
- In this episode, Echo cycled between cells 3 and 7 and hit me repeatedly. I was hiding at 5, 7, 1, 6 — and still got hit at 3 and 7. I should have recognized the two-cell pattern after two or three rounds and avoided both.
- If my shooter shows a clear cycling pattern (e.g., alternating between two cells), avoid all cells in that cycle.
- If I'm behind in points, I still prioritize safety. Being behind doesn't justify risky hides; it means I need to hit more on my end.

**Firing**
- The single biggest failure in my last episode: I fired 6 times and scored 0. I repeated cell 7 three consecutive rounds with no new information. That is unacceptable.
- **Cell elimination:** Every round, I note which cells were fired at my target and the claim was miss. In that round, my target was NOT at those cells. Over 6 rounds, if I see enough misses, I can narrow the field. Prioritize firing at cells that have never been tried against my target — if they're hiding somewhere and that cell has never been checked, it's a strong guess.
- **Pattern detection:** If my target is a rational player avoiding their shooter's cells, they will drift toward cells their shooter isn't using. I should fire at the intersection of "cells I haven't tried" and "cells their shooter isn't targeting."
- **No repetition without cause:** Never fire at the same cell two rounds in a row unless I have new information (e.g., my target's behavior suggests they moved there). In the last episode I fired 7 in rounds 2, 3, and 4 with zero new data. Each repeat was a wasted shot.
- **Aggression in late rounds:** By round 4 or 5, I should have eliminated enough cells to make a strong guess. If I'm at 0 points, I must take calculated risks rather than playing it safe. A missed shot in round 6 is worse than a risky shot that might connect.

**Claiming**
- Always claim exactly what the referee told me. No strategic room here.

**General**
- Before each decision, I reconstruct: (a) which specific cells my shooter has fired at me, (b) which cells have been fired at my target with a miss (eliminating those as their hide for that round), (c) which cells have never been fired at my target.
- The public log is my primary intelligence source. I read it fully each round. In my last episode I clearly wasn't using it well enough — I had 5+ rounds of data and still never hit.
- I am one link in a chain. My score = my hits × 4 − hits against me × 1. To go positive, I need at least 2 hits and very few hits against me. I should weight "making a hit" as the highest-priority objective, even at some risk on the hiding side.