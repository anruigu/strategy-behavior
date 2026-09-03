---
game: gen_quiet_sonar
model: fleet-kimi3
condition: win
seed: 0
round: 1
chars: 1809
---
When I must claim, I always claim the true result exactly as the referee reported it — a hit claim on a miss either gets rejected or is pure risk, and an honest hit is worth 4 points with no downside, so there is never a reason to deviate from the truth.

When hiding, I pick uniformly at random across all 9 cells. Reusing the same cell repeatedly (like parking on 2) makes me predictable; the shooter targeting me only gets 1/9 if I'm truly random, and any pattern I settle into can be exploited.

When firing, I treat it as a lottery I can slightly rig: I scan the public fire/claim history for any cell my target seems to favor or avoid. If my target's claims reveal where they were when hit, or their firing shows a favorite number, I weight my shot toward their habits; otherwise I fire at a fresh random cell each round rather than fixating on one number.

I track the scoreboard every round: if I'm behind late, I accept that firing is the only way to gain (each hit is +4 net swing) and keep varying my shots to cover untried cells; hiding well only loses me 1 point at worst, so aggression in firing costs nothing.

I avoid the temptation to "play it safe" with central cells as either hider or shooter — opponents cluster mid-range, so as a hider I give slight extra weight to edges (1, 2, 8, 9), and as a shooter targeting someone I've seen hide centrally, I shoot center.

In the final round, standings matter: if I lead, I hide with maximum randomness and fire anywhere; if I trail, I fire at the cell the target's history most suggests. There is no benefit to conserving anything, so variance is my friend.

I keep my reasoning output minimal and never reveal my hide logic in the visible reasoning line, since anything I say can inform opponents' reads of me in later rounds of the same match.