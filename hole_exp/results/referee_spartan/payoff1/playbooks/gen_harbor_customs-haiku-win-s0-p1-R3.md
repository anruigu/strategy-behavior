---
game: gen_harbor_customs
model: haiku
condition: win
seed: 0
round: 3
chars: 2354
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

## Error Correction: Memory and Clarity

In my last game, I repeatedly failed to retain and use my own crate values across the declare-to-route transition, even though I had explicitly calculated with them during declaration. I asked the game to restate information I had already been given.

I will write down my crate values immediately upon seeing them in the declare stage. The moment I see "Your private hold: crates worth X, Y, Z," I will note X, Y, Z. I will retain these values through to the route stage. I will use them to compute both route scores without asking for restatement.

I will not second-guess myself or claim I lack information I have already processed. If I declared a value with sound reasoning in the declare stage, I had the crate breakdown. I will trust my prior work and move to route calculation.