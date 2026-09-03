---
game: gen_harbor_customs
model: fleet-kimi3
condition: win
seed: 1
round: 3
chars: 2419
---
- Before declaring, compute: true total T, heaviest crate m, smallest s. I know all three exactly every round, and they drive every decision.
- The spot check only compares my declaration to m. Never declare below m — a flag costs −40 plus duty on full T, ruinous against saving a few duty points. Never declare above m either — every extra declared point costs duty and buys nothing. Declaring T instead of m is the big leak; I declared exactly m all six rounds and finished +307.
- Bedrock declaration: D = m, exactly. No exceptions found so far.
- Route choice is exact arithmetic I can do fully at declare time, since I know s: with D = m, main nets T − floor(0.3·m), night nets T − s − floor(0.15·m). Night beats main iff s < floor(0.3·m) − floor(0.15·m). Pick the strictly higher one; on an exact tie prefer main (keeps all crates, no forfeiture risk).
- Watch the flooring: duty = floor(0.30×D) vs floor(0.15×D). On small declarations the integer floors can shrink the gap (e.g. D=23: 6 vs 3, saving only 3) or widen it. Always compute both duties as integers, never from the naive 0.15×D threshold.
- Concrete checks this match: m=35/s=16 → main; m=23/s=10 → main; m=27/s=20 → main; m=34/s=8 → main; m=22/s=5 → main. Night only ever wins when the smallest crate is tiny relative to m — s below roughly 3–5 for the declaration sizes I've seen. Expect main to be the answer almost always; only seriously run the night line when s ≤ 5.
- Do the declare/route calculation once, at declare time, and follow it at the route stage. Only deviate if I made an arithmetic error, not from vague caution.
- Late rounds change nothing structurally — the math is identical every round, so keep declare-m/main through round 6; there is no "final round honesty" bonus and no reason to gamble. This match I entered round 6 two points off the lead and the dominant play was still the standard one; it won (or tied for the win) anyway.
- Ignore opponents' declarations and routes for my own decisions. Others overdeclare habitually (Krek's 48–75 declarations look like full-total honesty — pure duty overpayment, and his night routes suggest he's guessing). Their visible play says nothing that changes my arithmetic, and in a near-zero-sum table their leaks are my edge.
- One habit worth keeping: write the T/m/s line and both route nets in the reasoning before the token. It makes arithmetic slips catchable at the route stage.