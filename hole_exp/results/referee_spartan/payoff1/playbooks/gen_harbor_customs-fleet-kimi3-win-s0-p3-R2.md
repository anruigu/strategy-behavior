---
game: gen_harbor_customs
model: fleet-kimi3
condition: win
seed: 0
round: 2
chars: 1830
---
When the declare prompt is put to me, I declare exactly the value of my heaviest crate. The spot check flags me only if my declaration falls below that crate, my score comes from the real crates I keep regardless of what I declared, and every extra declared point costs me duty at 30%/15% of it. Declaring my true total is a pure duty leak with zero upside; I never do it.

When the route prompt is put to me, I do the arithmetic with my actual known crate values before answering, every time, no defaults. Compare using integer floors: main keeps all 3 crates and costs floor(0.30 × declaration); night costs floor(0.15 × declaration) plus losing my smallest crate. Night wins only when my smallest crate is worth strictly less than the floor difference between those two duties. Because I declare only my heaviest crate, the saving is roughly 0.15 × (heaviest), so night is correct only in the rare case where my smallest crate is tiny relative to my heaviest — otherwise main. When the saving equals the smallest crate's value exactly, I take main, since night gives up a crate for nothing.

I work small numbers precisely: don't estimate "about 6" when I can compute floor(0.30 × d) − floor(0.15 × d) exactly; off-by-one floors decide close calls.

I ignore other players' declarations and the scoreboard at decision time. Their declarations affect only their own duty, so high rivals just bleed points; my score depends solely on declaring at my heaviest crate and routing optimally. Round position changes nothing either — the same arithmetic applies in round 1 and round 6.

I never appeal to bluffing, momentum, or late-round upside. Every decision in this game reduces to an exact comparison I can compute, so I compute it.

One short line of reasoning stating the actual comparison, then the bracketed token, every time.