---
game: gen_harbor_customs
model: haiku
condition: win
seed: 4
round: 2
chars: 2398
---
# Harbor Customs Playbook

## Declaration Strategy

When you see your three crates, always declare at least the value of your heaviest crate—this is the minimum safe floor to avoid the -40 penalty. The scale check always reveals your heaviest crate, so underestimating it costs you -40 plus recalculated duty at 0.30 rate.

For any hold, calculate both routes:
- Main route score: (sum of all three crates) - floor(0.30 × declaration)
- Night route score: (sum of two largest crates) - floor(0.15 × declaration)

Declaring your full hold value gives you maximum flexibility in route choice and removes the risk of being flagged. Do not artificially suppress your declaration to appear less threatening—other players will see you have three crates regardless, and suppressing costs you points if you get flagged.

The advantage of the night route over main is: (duty savings) - (cost of smallest crate). Calculate this precisely for each hand. If night saves more than 10 points, plan to take it. Otherwise, main is more reliable.

## Route Selection

When choosing your route after declaring, always calculate exactly:
- Main: (sum of all three crates) - floor(0.30 × declaration)
- Night: (sum of two largest crates) - floor(0.15 × declaration)

Pick whichever number is larger. Do not default to main out of caution or habit. The math will tell you which route wins. In this episode I often defaulted to main even when night scored better—this cost me points in rounds 2, 4, and 5.

Specific calculation method: If my smallest crate is worth C, then night beats main when:
C < floor(0.30 × declaration) - floor(0.15 × declaration)

This is a simple threshold test. Run it every time.

## Competitive Positioning

Do not factor other players' scores into your route decision. Your job is to maximize your own score on each round. Worrying about trailing competitors or signaling weakness through conservative declarations does not change the math of your own payoff.

Track your standing to stay aware of the game state, but when it's your decision to make, optimize for your individual score, not relative position.

## End-game Adjustments

In the final round, apply the same calculation discipline as any other round. The fact that scores are close does not justify abandoning the math. Maximize your personal score with the crates in front of you. Other players' outcomes are not your control.