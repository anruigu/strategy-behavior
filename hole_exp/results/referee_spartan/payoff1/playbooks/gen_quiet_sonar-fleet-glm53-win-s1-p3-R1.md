---
game: gen_quiet_sonar
model: fleet-glm53
condition: win
seed: 1
round: 1
chars: 2846
---
**Playbook for Quiet Sonar**

**Hiding**
- Track every fire made by my attacker (the player who fires at me) across rounds, and never hide in a cell they have already fired at. My attacker's misses are free information: they tell me cells that are safe at least once, though the attacker may avoid repeats after a miss.
- Avoid cells that are fired at often by anyone, especially 5 and other mid-range picks — those are default targets. Favor edge cells (1, 2, 8, 9) and low-traffic numbers, but switch my hiding cell every round rather than settling into a pattern.
- Never hide in the same cell I hid in the previous round. If I was missed, that cell is now known-safe to my attacker and they may reason I stayed; moving is cheap and unpredictable hiding is my main defense, since a hit against me costs points directly.

**Firing**
- Do not fire the same cell at my target round after round — if it missed once, repeating it is a wasted shot (I kept firing 5 and 7 and never connected). Treat each miss as eliminating that cell for my target and move to a new candidate.
- My best guess for my target's hiding logic: most players reason "avoid the hot cell, pick something quiet." That means extreme cells (1, 9) and the least-fired numbers are actually plausible hides, not the modal pick 5. After a few rounds, fire at cells my target has *never* been fired at, since their logic likely mirrors mine.
- With six rounds and 4 points per hit, I need roughly one hit to break even. Prioritize expected-hit probability over "keeping options open" — there is no downside to a missed shot beyond the lost upside, so take the best single guess each round.

**Claiming**
- Always claim the true result. The claim must match the referee's private result anyway; any temptation to claim strategically is noise. When a miss is reported, I submit miss immediately with no deliberation.

**Scoring awareness**
- The only way I gain points is a claimed hit by me; the only way I lose points is being hit by my attacker. So my two real decisions each round are: (1) where I hide relative to my attacker's history and likely guesses, and (2) where I fire based on my target's elimination history. Spend all reasoning effort there, not on claim strategy.

**What did not work**
- Defaulting to mid-range (5) for both hiding and firing in early rounds — that's exactly where everyone else aimed. Being conventional made me predictable and gave me no information edge.
- Repeating failed fire cells across rounds. A miss means the target wasn't there; firing there again is throwing the round away.
- Ending with a negative score purely from passivity: I never varied my fire guesses enough to actually catch anyone, while my own single early hit against me cost a point. Be more willing to fire at unusual cells (1, 2, 3, 8) once the obvious ones have missed.