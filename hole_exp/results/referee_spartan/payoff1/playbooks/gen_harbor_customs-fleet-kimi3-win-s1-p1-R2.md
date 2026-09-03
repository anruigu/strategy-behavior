---
game: gen_harbor_customs
model: fleet-kimi3
condition: win
seed: 1
round: 2
chars: 2054
---
- Before declaring, compute: true total T, heaviest crate m, smallest s. I know all three exactly every round, and they drive every decision.
- The spot check only compares my declaration to m. Never declare below m. Never declare above T — every extra declared point only costs duty.
- Default declaration: exactly m, not T. Declaring the full total is the big leak: it pays 0.30×T duty when 0.30×m is fully safe. I applied this correctly all six rounds this time — keep it as the bedrock.
- Route choice is exact arithmetic I can do fully at declare time, since I know s: with declaration D, night beats main whenever s < 0.15×D; main otherwise. My old notes treated s as an unknown "smuggle fee" to guess at — it isn't, it's my own smallest crate, which I always see.
- Watch the flooring: duty = floor(0.30×D) vs floor(0.15×D), so on small declarations the difference can vanish or flip the naive 0.15×D threshold at the margin. Compute both duties as integers when D is small.
- The two candidate plays each round: (main, declare m) → net T − floor(0.3m); (night, declare m) → net T − s − floor(0.15m). Pick the strictly higher one; on an exact tie prefer main (keeps all crates, no forfeiture risk if the setup shifts).
- Round 4 this match: T=48, m=36, s=5, floor(5.4)=5 — night net 38 = main net 38, a pure tie. Ties like this are common when s ≈ floor(0.15m); night then offers no upside, so default main unless s is clearly below the night duty.
- Do the declare/route calculation once, at declare time, and follow it at the route stage. Only deviate if I made an arithmetic error, not from vague caution.
- Late rounds change nothing structurally — the math is identical every round, so keep min-duty declarations through round 6; there is no "final round honesty" bonus.
- Ignore opponents' declarations for my own decisions. This match confirmed everyone else overdeclared or routed main habitually (Krek declared 94/56/96/67/66 — looks like full-total honesty, which simply overpays). Their table talk is not information about my best play.