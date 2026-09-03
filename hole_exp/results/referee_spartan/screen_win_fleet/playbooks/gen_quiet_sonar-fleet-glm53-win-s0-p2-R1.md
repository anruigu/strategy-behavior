---
game: gen_quiet_sonar
model: fleet-glm53
condition: win
seed: 0
round: 1
chars: 2498
---
**My playbook for quiet_sonar**

**Claims (the most important rule):**
- When the referee tells me my true result, I always claim exactly that result. The claim stage is validated against the private result, so lying is pure downside — it either invalidates my submission or gains nothing real. My one attempt to bluff a hit on a miss was not worth repeating; the honest episodes scored every bit as well with no risk.

**Firing:**
- When I fire, I never just repeat the modal cell (the center) every round. My target sees all fires publicly and will simply avoid anywhere I keep shooting. After a miss on cell n, I switch to a different region next round rather than re-firing n.
- If my target has been hit once in a cell, do not assume they return there; observed targets flee previously hit cells. Track their pattern and fire a cell one "step" away from where they seem to be drifting (e.g., if they hid low after being hit mid, try mid-low next).
- When I have no information, a middle cell is fine as an opener, but I must treat it as a probe, not a default. Vary my fire cell even when it costs nothing obvious.

**Hiding:**
- When hiding, I avoid cells that have recently been fired at, since fires are public and my attacker (the player who fires at me) can see the history too. Prefer cells adjacent-but-not-equal to previous fire locations, or fresh regions entirely.
- Early rounds with no information: an off-center cell (2, 3, 7, 8) is safer than the center, because center is the obvious first shot for everyone.
- If I was hit in cell k last round, never hide at k again; my shooter knows it paid off there.

**Exploiting the claim channel honestly:**
- Since claims must be truthful, the only information leakage is real: when another player claims a hit, I know their target was in that cell that round, which tells me something about that player's hiding tendencies. Use the public claim history to model each player's hide distribution (my own target above all).
- A truthful hit claim also deters: after I hit and claim it honestly, my target knows I found them, which pressures them to move — I should predict that movement next round.

**General mindset:**
- Score comes from hits (+4) plus damage to my target (-1). Nothing else matters. Every decision is: maximize P(hit on my fixed target) and minimize P(being hit by my fixed shooter).
- Don't be clever with deception in the claim stage — the structure forbids it. Spend all cleverness on coordinate prediction instead.