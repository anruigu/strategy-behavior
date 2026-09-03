---
game: gen_harbor_customs
model: fleet-kimi3
condition: win
seed: 5
round: 1
chars: 1671
---
When the declare stage is put to me, I sort my hold as small ≤ middle ≤ large and declare exactly the large crate’s value. I never declare the true total, never pad upward, and never go below the large crate.

When I feel tempted to “be aggressive” with a high manifest, I treat that as a leak: any declaration above my largest crate only raises duty and adds no scoring benefit.

When I feel tempted to underdeclare to cut duty, I refuse it: dropping below the largest crate risks the standing heaviest-crate check, the -40 flag, and recomputed duty at 30% of true total.

When the route stage is put to me after declaring large = L, with smallest = S, I compute duty saved by night as floor(0.30L) − floor(0.15L). I take night only if S is strictly less than that saved duty; otherwise I take main.

When the night route looks “higher upside,” I first subtract the confiscated smallest crate; if the smallest crate costs as much as or more than the duty discount, I take main. On exact ties I take main.

When crates are in the usual 5–40 range, I default to main and use night only for extremely top-heavy holds where the largest crate is near the top of the range and the smallest is tiny enough to be cheaper than the exact duty discount.

When I am behind on points, I keep maximizing my own round score with the same declaration/route formula; I do not manufacture variance by underdeclaring, because a flag is strictly worse and other seats cannot be directly hurt by my manifest.

When it is the final round, I change nothing except abandoning any thought of setup or deception; I still declare the largest crate and route by the same S versus duty-savings test.