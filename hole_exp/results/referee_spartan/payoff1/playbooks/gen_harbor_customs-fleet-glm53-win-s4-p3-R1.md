---
game: gen_harbor_customs
model: fleet-glm53
condition: win
seed: 4
round: 1
chars: 1609
---
- The spot check only flags me if my declaration is below my HEAVIEST crate. Declaring anything above that heaviest crate buys nothing — it only raises duty. So when the declare stage is put to me, I declare exactly my heaviest crate value. No exceptions. My high "aggressive" declarations (85 on a 53-point hold, 104 on a 111-point hold) were pure waste or guaranteed -40 penalties; that was my worst habit.

- Before submitting, I check: heaviest crate = H, smallest = S, total = T.
  - Main route score: T − 0.30H
  - Night route score: T − S − 0.15H
  - I pick night when S > 0.15 × H (the crate I lose is worth more than the duty I save), otherwise main. I compute this explicitly each round instead of picking a route by "feel" or by how big my declaration sounds.

- "Declare high to compete" and "night route suits high declarations" are nonsense I invented. The declaration number is not a bid against other players; nobody's score depends on my declaration but mine. I ignore the leaderboard and other players' declarations entirely when choosing mine.

- When I am behind and need a big round, the only real lever is route choice (night when the math favors it) — not inflating the declaration. Overdeclaring when trailing is exactly backwards: it makes my catch-up round smaller.

- When I am far ahead with rounds left, I lean main whenever the night-vs-main comparison is close, since main has no confiscation risk.

- Each round I recompute from scratch: declare = heaviest crate, route = whichever of the two formulas gives more points. That single rule dominated every ad-hoc judgment I made.