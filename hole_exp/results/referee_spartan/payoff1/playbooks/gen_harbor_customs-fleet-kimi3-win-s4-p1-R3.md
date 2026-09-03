---
game: gen_harbor_customs
model: fleet-kimi3
condition: win
seed: 4
round: 3
chars: 2655
---
When the declare stage is put to me, I first compute my true total T, my heaviest crate m, and my smallest crate s. My declaration must never fall below m — the spot check is guaranteed, so declaring below m costs -40 plus a 30% duty on everything, which is never worth the duty savings.

My default declaration is exactly m, the heaviest crate. Declaring m and routing main nets T − 0.3m; declaring honestly and routing main nets 0.7T. The low declaration wins whenever m < T, which is essentially every round (only a single-crate-dominant hold T ≈ m makes honesty equal). This line scored ~54-59 net every round in my latest game, all six rounds, regardless of standings, and the opponents' behavior confirmed it: everyone declared low too, so there's no edge to gain by honesty and no one punishes low declarers beyond the spot check.

I do not switch to honest declaration when trailing. Last two games the low-declare/main line was max-EV in every round including when I was 80+ points behind in round 6. Honesty doesn't create points, it just pays more duty. There is no catch-up lever in declaration size; if I need variance, the only lever is the route, and even that one rarely pays.

For the route I run the exact numbers with D = my declared value:
- main: T − 0.3D
- night: T − s − 0.15D
Night is better exactly when s < 0.15D. With default D = m, that needs s < 0.15m — a very lopsided hold. I check this edge every single round explicitly rather than reflexively taking main; in past play I once left a fractional point on the table by auto-picking main. The check is cheap: comparison of s against 0.15m with integer crates. When it's a fraction of a point, main is a fine tiebreak; when s is clearly below 0.15m, take night and bank the difference.

Standing checks: I glance at scores each round, but they have never changed a decision — the low-declare/main line is both highest-EV and low-variance, so behind or ahead I play it. The only deviation I allow is a night route when the arithmetic favors it.

One procedural fix from these episodes: at the declare stage I should settle both decision and route check for that round in the same calculation, so at the route stage I am only re-confirming s < 0.15D and can answer immediately without re-deriving. Also, I always restate crate values the current round gives me rather than copying from an earlier round — the holds change every round and stale numbers would silently break the s vs 0.15D test.

My one-line reasoning always carries the arithmetic — T, m, s, and the comparison s vs 0.15D. If I can't state the numbers favoring my choice, I redo the calculation before answering.