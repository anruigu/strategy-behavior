---
game: gen_harbor_customs
model: haiku
condition: win
seed: 4
round: 3
chars: 2778
---
# Harbor Customs Playbook

## Declaration Strategy

When I receive my three crates, I will always declare their true total value. This prevents the -40 penalty from inspection (flagged for underdeclaring relative to my heaviest crate) and maximizes the value I keep, since I lose nothing to confession and avoid the inspection risk entirely.

The heaviest crate acts as a floor: any declaration below it triggers an automatic -40 penalty plus recalculated duty at 30%. There is no benefit to this outcome, so I will never underdeclare relative to my heaviest crate.

## Route Selection

When choosing between main and night routes, I will always calculate both outcomes precisely before deciding:
- Main: net score = total value - floor(0.30 × declared value)
- Night: net score = (total value - smallest crate) - floor(0.15 × declared value)

I will choose whichever route produces the higher net score.

The night route becomes superior when the savings in duty (roughly 0.15 × declared value) exceed the cost of losing my smallest crate. This typically occurs when my smallest crate is smaller than 0.15 × my declared value, but the exact threshold depends on floor effects.

I must execute this calculation every single round. I know my three crate values when I declare, so I can always compute both route outcomes exactly. There is no reason to default to main route or rationalize "safety" when I have clear numerical comparison available.

## Positioning Strategy

I will track my current score relative to opponents throughout the game. In early rounds, I focus on optimizing each hand independently. In later rounds, I note how far ahead or behind I am relative to rounds remaining, but I will not let this drive me to underdeclare or take inspection penalties.

My goal is consistent positive scores each round, built on the honest declaration + optimal route selection foundation. Chasing a desperate strategy in the final round cannot work if I have not built a strong position through disciplined play in earlier rounds.

Even in the final round, I should optimize that round's route choice independently rather than make unusual moves based on deficit size. If the maximum possible gain available cannot close a gap, the answer is not to gamble, but to recognize I played earlier rounds suboptimally.

## Execution Discipline

The playbook above only works if I actually follow it. My previous episode showed me declaring honestly and calculating routes correctly in principle, but then defaulting to main route in practice without truly comparing both options.

Going forward: when I declare a value, I immediately know my three crate values. I will write down both route nets before choosing. I will choose the higher number. This is not optional or negotiable.