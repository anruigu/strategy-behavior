---
game: gen_harbor_customs
model: haiku
condition: win
seed: 6
round: 1
chars: 2461
---
# Harbor Customs Playbook

## Declaration Strategy

When declaring, calculate your true hold value first. Then decide between truthful declaration and understatement based on your heaviest crate.

If your heaviest crate is close to half your total value, declare truthfully—the flagging penalty (-40 plus recomputed duty) is worse than the duty savings from understatement.

When you hold moderate values (50-80 range), declare your true total to avoid the -40 flagging penalty. This gives you a clean calculation and predictable scoring.

## Route Selection

When you declare your true value, choose the night route if your smallest crate is worth much less than the duty savings. Calculate: (duty difference) versus (value of smallest crate lost). Night route wins when 0.15x declared value saves more than the smallest crate costs.

However, I deviated from this calculation in Round 1 despite showing the math favoring night route, then chose main route anyway. Do not second-guess your math mid-game. When the numbers say night, take night.

In later rounds, I defaulted to main route repeatedly without recalculating. This was safe but suboptimal. Every round, run the calculation fresh: net score from night = (total - smallest) - floor(0.15 × declared), compared to net score from main = total - floor(0.30 × declared). Pick whichever is higher.

## Position-Based Adjustments

When you are leading, maintain your lead with safe, calculated choices rather than predictable patterns. I was in first place midgame but failed to adapt strategy—I kept choosing main route out of habit instead of optimizing each decision.

When you are behind in the final rounds, recognize whether you need aggressive scoring (night route for upside) or secure scoring (main route for reliability). Make this choice explicitly rather than defaulting to main.

Do not let prior round patterns influence your current declaration. Each round is independent; declare based on this hand's crate values and current game state.

## What Did Not Work

Choosing main route "for reliability" when the math favored night route cost me points in several rounds. Calculate, then commit—do not rationalize away your own analysis.

Declaring conservatively in the final round when holding weak crates (7, 15, 28) may have been correct, but I declared this without stating whether I was trying to lock in a win or still competing. Know your position's requirements and declare accordingly.