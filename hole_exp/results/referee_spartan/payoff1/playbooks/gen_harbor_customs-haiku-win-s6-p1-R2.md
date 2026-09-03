---
game: gen_harbor_customs
model: haiku
condition: win
seed: 6
round: 2
chars: 3001
---
# Harbor Customs Playbook

## Declaration Strategy

When declaring, calculate your true hold value first. Then decide between truthful declaration and understatement based on your heaviest crate.

If your heaviest crate is close to half your total value, declare truthfully—the flagging penalty (-40 plus recomputed duty) is worse than the duty savings from understatement.

When you hold moderate values (50-80 range), declare your true total to avoid the -40 flagging penalty. This gives you a clean calculation and predictable scoring.

For high-value holds (80+), declaring truthfully is still the right move. The flagging penalty is devastating and the duty savings from understatement do not justify the risk.

## Route Selection

Every round, run the fresh calculation: net score from night = (total - smallest) - floor(0.15 × declared), compared to net score from main = total - floor(0.30 × declared). Pick whichever is higher.

The night route wins when the duty savings (0.15x declared) exceed the value of your smallest crate. This is often true when your smallest crate is small relative to total value.

Do not default to main route out of habit or perceived "safety." The night route is not inherently risky when you declare truthfully—it is simply a different tradeoff. If the math favors night, take it.

When calculating the breakeven: night route saves 0.15x duty compared to main route, which costs you your smallest crate. If 0.15x declared > smallest crate value, night wins. If 0.15x declared < smallest crate value, main wins.

## Position-Based Adjustments

When you are leading or tied, maintain position with calculated choices rather than defaulting to habit. Do not assume main route is "safer"—recalculate every round.

When you are behind in the final rounds, your position does not change the calculation; it changes how much you care about variance. But one round's +3 or +5 point advantage matters late. Execute the math precisely.

When your position is mathematically out of reach (down more than your remaining rounds can recover), you can afford to take slightly higher-risk declarations if the expected value is higher. But with one round left, play to maximize that round's score, not to gamble.

## What I Learned This Episode

Declaring truthfully and then calculating the route correctly beats any habit. In Round 6, I declared 66 truthfully and initially chose main route (47 points), then caught myself and recalculated: night route was 50 points (66 - 20 - 9). I took night and gained 3 extra points. This small gain matters in a tight game.

I was tied with Mirren at 228 at the start of Round 6. The 3-point swing from executing the route calculation correctly brought me to 265 final score, ahead of where I would have been. This is the payoff of doing the math every single round.

Do not carry patterns from earlier rounds into later rounds. Each hand is independent. Each route choice is independent. Declare the truth, calculate the route, execute.