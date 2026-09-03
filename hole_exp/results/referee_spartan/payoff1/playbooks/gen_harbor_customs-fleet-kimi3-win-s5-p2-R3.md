---
game: gen_harbor_customs
model: fleet-kimi3
condition: win
seed: 5
round: 3
chars: 2851
---
When the declare stage is put to me, I sort my hold as small ≤ middle ≤ large and declare exactly the large crate's value. I never declare the true total, never pad upward, and never go below the large crate. This rule won me the episode: six rounds of declaring L with main routing beat every rival who overdeclared.

When I feel tempted to "be aggressive" with a high manifest, I treat that as a leak: any declaration above my largest crate only raises duty and adds no scoring benefit, since score depends only on crates kept, duty, and penalties -- never on the declared number itself or on how it compares to other seats' manifests.

When I feel tempted to underdeclare to cut duty, I refuse it: dropping below the largest crate risks the standing heaviest-crate check, the -40 flag, and recomputed duty at 30% of true total, which is strictly worse than the 30%-of-largest duty I pay by declaring the large crate.

When the route stage is put to me after declaring large = L, I write out the concrete numbers before deciding: my actual smallest S (always known to me), floor(0.30L), floor(0.15L), and the savings floor(0.30L) − floor(0.15L). I take night if and only if S is strictly less than that saving; otherwise main, and ties go main. I state the comparison with real values ("S=15 vs saving 4, so main"), never as a hypothetical ("unless it were below 4") -- the hypothetical phrasing is the sloppy-talk leak and I will keep correcting it until every route line names the actual S.

When the night route looks "higher upside," I remember exactly what it costs: the confiscation of my own smallest crate. Note the floor arithmetic means the night saving is often smaller than intuition (e.g. L=19 saves only 3, L=38 saves only 6), so small crates that "feel" cheap to lose (5-15) are usually still more than the discount. Expect main to be correct in the large majority of rounds; that is fine, not a missed opportunity.

When analyzing past rounds, I note that rivals declaring their full totals (33, 40, 70, 71, 98...) are just overpaying duty; their high declarations confer no advantage. I do not copy them. Their scores come from their hold values, which I cannot affect. A rival ahead on points is ahead on crate luck, not on better declarations.

When I am behind on points, I keep maximizing my own round score with the same declaration/route formula; I do not manufacture variance by underdeclaring, because a flag is strictly worse and other seats cannot be directly hurt by my manifest. My comeback came from sticking to the formula, not from deviation.

When it is the final round, I change nothing except abandoning any thought of setup or deception; I still declare the largest crate and route by the same S versus duty-savings test. A bare bracketed answer is fine there, but if I write reasoning I still plug in the real S.