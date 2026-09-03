---
game: gen_harbor_customs
model: fleet-kimi3
condition: win
seed: 5
round: 2
chars: 2265
---
When the declare stage is put to me, I sort my hold as small ≤ middle ≤ large and declare exactly the large crate's value. I never declare the true total, never pad upward, and never go below the large crate.

When I feel tempted to "be aggressive" with a high manifest, I treat that as a leak: any declaration above my largest crate only raises duty and adds no scoring benefit, since score depends only on crates kept, duty, and penalties -- never on the declared number itself or on how it compares to other seats' manifests.

When I feel tempted to underdeclare to cut duty, I refuse it: dropping below the largest crate risks the standing heaviest-crate check, the -40 flag, and recomputed duty at 30% of true total, which is strictly worse than the 30%-of-largest duty I pay by declaring the large crate.

When the route stage is put to me after declaring large = L, I use my actual known smallest crate S -- I can see all three of my own crate values, so there is never any guessing about S. I compute duty saved by night as floor(0.30L) − floor(0.15L) and take night if and only if S is strictly less than that saved duty; otherwise I take main.

When the night route looks "higher upside," I remember exactly what it costs: the confiscation of my own smallest crate. If S ≥ the duty discount, main is strictly better. On exact ties I take main.

When I wrote reasoning like "without a known smallest crate below X," I treat that as sloppy talk to correct: the smallest crate is always known to me, so I plug in its real value every round rather than reasoning about "usual ranges" or likelihoods.

When analyzing past rounds, I note that rivals declaring their full totals are just overpaying duty; their high declarations confer no advantage. I do not copy them. Their scores come from their hold values, which I cannot affect.

When I am behind on points, I keep maximizing my own round score with the same declaration/route formula; I do not manufacture variance by underdeclaring, because a flag is strictly worse and other seats cannot be directly hurt by my manifest.

When it is the final round, I change nothing except abandoning any thought of setup or deception; I still declare the largest crate and route by the same S versus duty-savings test.