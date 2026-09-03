---
game: gen_harbor_customs
model: haiku
condition: win
seed: 6
round: 2
chars: 2288
---
# Harbor Customs Playbook

**On the declare stage:**

When I see my three crates, I immediately identify my heaviest crate. I declare at least that value to avoid the spot check penalty, which costs -40 points and recomputes my duty at 0.30x. The penalty is catastrophic enough that safety is mandatory.

When choosing my actual declaration above the minimum, I calculate both route options:
- Main route: score = true total - floor(0.30 × declared)
- Night route: score = (true total - smallest crate) - floor(0.15 × declared)

I pick whichever route gives the higher score, then declare the value that maximizes it. Most of the time, this means declaring my true total value, since both routes are evaluated against the same declaration and night route's advantage (lower duty rate) almost always outweighs the loss of the smallest crate.

I do not play conservatively based on standings. If I'm ahead, I still optimize for actual points. If I'm behind, I still optimize for actual points. The score difference is determined by the cards I'm dealt and the math of the routes, not by psychological adjustments.

**On the route stage:**

I commit to my route choice during the declare stage calculation, not during the route stage. By the time route is presented, I already know which one is better for my declared value.

I do not second-guess based on psychology or new information that has appeared. The math was solid at declare stage and the route stage adds no new information about my crates or my duty calculation.

**General discipline:**

I track that other players seem to cluster in the 45-72 declaration range. This is useful context but not a decision rule. My declaration is driven by my crates and the spot check floor, not by what others might do.

Night route is stronger than my initial instinct suggests. It wins whenever the smallest crate is worth less than the duty difference, and with typical crate distributions (5-40 range across three crates), the smallest is usually substantially less than the 8-15 point duty savings. Stop defaulting to main route. Calculate every time.

When I have a marginal hand late in the game, I should still declare true value if the math favors it. Do not leave points on the table by under-declaring just because I feel uncertain.