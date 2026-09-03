---
game: gen_harbor_customs
model: fleet-kimi3
condition: win
seed: 4
round: 2
chars: 2015
---
When the declare stage is put to me, I first compute my true total T, my heaviest crate m, and my smallest crate s. My declaration must never fall below m — the spot check is guaranteed, so declaring below m costs -40 plus a 30% duty on everything, which is never worth the duty savings.

My default declaration is exactly m, the heaviest crate. Declaring m and routing main nets T − 0.3m; declaring honestly and routing main nets 0.7T. The low declaration wins whenever m < T, which is essentially every round. In this episode that line scored ~56-76 per round and won the game outright. I do not declare my true total unless T ≈ m (one dominant crate), where the difference vanishes.

I do not switch to honest declaration just because I'm trailing. Last game I trailed at points and the low-declare/main line was still the maximum-EV play; honesty doesn't create points, it just pays more duty. There is no catch-up variance available from declaring more — the aggressive lever, if any, is route choice, not declaration.

For the route I run the exact numbers:
- main: T − 0.3D
- night: T − s − 0.15D
Night is better exactly when s < 0.15D. With my default D = m, that needs s < 0.15m — a very lopsided hold (e.g. crates 5, 10, 36: s=5 vs 0.15·36=5.4, night barely wins). I check this edge case each round rather than auto-picking main; in my game I passed up a tiny night gain on the 5/10/36 hold by reflexively taking main. When the gap is a fraction of a point, main is fine as the tiebreak; when s is clearly below 0.15m, I take night and bank the extra points.

Standing checks: I glance at scores to know where I am, but since the low-declare/max-value line is also the highest-variance-free line, standings rarely change my play. Only if I'm behind late AND a night route is arithmetically better do I deviate from main.

My one-line reasoning always carries the arithmetic — T, m, s, and the comparison 0.15D vs s. If I can't state the numbers favoring my choice, I redo the calculation before answering.