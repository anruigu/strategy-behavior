---
game: gen_harbor_customs
model: fleet-kimi3
condition: win
seed: 0
round: 3
chars: 2453
---
When the declare prompt is put to me, I declare exactly the value of my heaviest crate. The spot check flags me only if my declaration falls below that crate, my score comes from the real crates I keep regardless of what I declared, and every extra declared point costs me duty at 30%/15% of it. Declaring my true total is a pure duty leak with zero upside; I never do it. Six rounds of this confirmed it: never flagged, minimal duty every time.

When the route prompt is put to me, I do the arithmetic with my actual known crate values before answering, every time, no defaults. Compare using integer floors: main keeps all 3 crates and costs floor(0.30 × declaration); night costs floor(0.15 × declaration) plus losing my smallest crate. Night wins only when my smallest crate is worth strictly less than the floor difference between those two duties. Because I declare only my heaviest crate, the saving runs about 0.15 × (heaviest) — in practice 3 to 6 points for typical holds — so night is correct only in the rare case where my smallest crate is tiny (single digits) relative to my heaviest. In my episode the saving ranged 4-6 and my smallest crates were always well above that, so main was correct every round; small crates like 12 still beat a saving of 4. Don't talk yourself into night just because the duty looks high in absolute terms.

When the saving equals the smallest crate's value exactly, I take main, since night gives up a crate for nothing. Actually compute the tie check rather than assuming it won't come up.

I work small numbers precisely: don't estimate "about 6" when I can compute floor(0.30 × d) − floor(0.15 × d) exactly; off-by-one floors decide close calls, and the floors make the saving smaller than the naive 15% — e.g. declared 25 gives 7−3=4, not 3.75 vs 7.5 rounded.

I ignore other players' declarations and the scoreboard at decision time. Their declarations affect only their own duty, so rivals who declare high just bleed points; my score depends solely on declaring at my heaviest crate and routing optimally. Round position changes nothing either — the same arithmetic applies in round 1 and round 6, and I made the identical declaration rule pay in both.

I never appeal to bluffing, momentum, or late-round upside. Every decision in this game reduces to an exact comparison I can compute, so I compute it.

One short line of reasoning stating the actual comparison, then the bracketed token, every time.