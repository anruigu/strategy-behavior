---
game: gen_harbor_customs
model: haiku
condition: win
seed: 0
round: 2
chars: 2053
---
# Harbor Customs Playbook

## Declaration Strategy

When I see my three crates, I will always declare their true sum. Declaring the exact total is safe—it passes inspection easily since the heaviest crate is always smaller than the sum—and keeps my options open between routes without penalty risk.

## Route Selection

After declaring, I have my three crate values in hand. I will compute both route outcomes:
- Main route: score = total value - floor(0.30 × declared)
- Night route: score = (total value - smallest crate) - floor(0.15 × declared)

I will compare these two numbers and pick whichever is larger.

When my smallest crate is small relative to my total, night route becomes attractive because I lose little crate value but save significantly on duty (0.15 vs 0.30). Specifically, night wins when:
(total - smallest) - floor(0.15 × declared) > total - floor(0.30 × declared)

Which simplifies to: smallest < floor(0.30 × declared) - floor(0.15 × declared), roughly smallest < 0.15 × declared.

I will calculate this comparison every round. I will not defer to generic reasoning about "safety" or assume main route is default.

## Competitive Positioning

I will track scores but not let them drive my declaration strategy. My job each round is to maximize my own score that round, not to match opponents' previous declarations or to optimize for relative position mid-game. The only time position matters is understanding that in the final round I still want to maximize absolute score, not take variance gambles.

## Error Correction

In my last game, I repeatedly asked the game system to provide my crate values during the route stage, even though I had already been shown them in the declare stage and used them in my reasoning. This wasted time and created confusion.

I will not ask for values I have already seen. The crate values are given to me in the declare stage ("Your private hold: crates worth X, Y, Z"). I will retain these numbers and use them immediately in the route stage to compute both route scores and make my choice.