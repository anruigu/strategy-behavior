---
game: gen_harbor_customs
model: haiku
condition: win
seed: 6
round: 3
chars: 4118
---
# Harbor Customs Playbook

## Declaration Strategy

When declaring, calculate your true hold value first. Then decide between truthful declaration and understatement based on your heaviest crate.

If your heaviest crate exceeds your declared value, you get flagged: -40 points and duty is recomputed at 0.30x true total. This penalty is severe. Always declare at least your heaviest crate value to stay legal.

When you hold moderate to high values, declare your true total. The flagging penalty (-40 plus duty recomputation) is worse than any duty savings from understatement. Truthful declaration gives you clean, predictable scoring and full flexibility on route choice.

For all holds, truthful declaration is the safe default. I have not found a scenario in play where understatement beats truthful declaration once the -40 flagging penalty is properly weighted.

## Route Selection

Every round, run the fresh calculation: net score from night = (total - smallest) - floor(0.15 × declared), compared to net score from main = total - floor(0.30 × declared). Pick whichever is higher.

The breakeven point is: night wins if 0.15x declared > smallest crate value. Main wins if 0.30x declared > smallest crate value (equivalently, if smallest crate value > 0.15x declared).

When routes tie in expected value, I have tried both main and night. Ties are common with balanced, medium-value holds. In a tie, either choice is defensible; I will prefer main route as the default tiebreaker to avoid overthinking.

Do not default to main route out of habit. If the math favors night, take it. The night route is not inherently risky when you declare truthfully—it simply surrenders your smallest crate in exchange for lower duty. Calculate every time.

## Common Patterns

With holds in the 35-65 range (small to moderate), night route often wins because the duty savings outweigh a modest smallest crate value.

With holds where the smallest crate is very small (6-10) relative to a larger total (50+), night route usually wins decisively.

With balanced holds (all three crates similar value), main and night routes often tie or come very close. Recalculate to be sure, then pick main as tiebreaker.

With holds where the smallest crate is large (25+) relative to total value, main route is more likely to win. But still calculate—do not assume.

## Position-Based Adjustments

Position matters for psychology but not for math. Whether I am leading or trailing, the calculation for each route is the same. Execute it precisely.

When tied or leading late in the game, maintain position with calculated choices. A 3-point swing from correct route selection can separate winners from runners-up in a tight field.

When behind in the final rounds, do not gamble on understatement or risk-taking. One more round's optimal play—truthful declaration + correct route calculation—may not close the gap, but it is the only play available. Do the math and execute it.

## What I Learned This Episode

I declared truthfully in every round and avoided flagging entirely. This consistency was rewarded: I finished with 261 points in a four-player game, competitive even though I did not lead outright.

I made arithmetic errors on route selection twice (Rounds 1 and 5) but caught and corrected them during the route stage. This shows the value of recalculating at every decision point rather than committing to a route too early.

In Round 5, I declared 63 (truthfully), calculated night route at 63 - 16 - 9 = 38 and main route at 63 - 18 = 45, and correctly chose main. Then in the route stage I recalculated and found them tied at 45. I had made an arithmetic error in my reasoning—I had written that night was 38 points but then said I'd take night. I caught this and corrected to night in the actual route choice. Either choice tied, so it did not matter, but this shows I need to verify my arithmetic before committing.

Truthful declaration + accurate route calculation beats any pattern or habit. Do not carry assumptions from one round to the next. Each hand is independent. Declare the truth, calculate the route, execute.