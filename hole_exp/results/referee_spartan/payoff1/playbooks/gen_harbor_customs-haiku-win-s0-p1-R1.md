---
game: gen_harbor_customs
model: haiku
condition: win
seed: 0
round: 1
chars: 1861
---
# Harbor Customs Playbook

## Declaration Strategy

When I see my three crates, I will always declare their true sum. Declaring the exact total is safe—it passes inspection easily since the heaviest crate is always smaller than the sum—and keeps my options open between routes without penalty risk.

When choosing between routes given my declared value, I will calculate both outcomes explicitly:
- Main route: score = total value - floor(0.30 × declared)
- Night route: score = (total value - smallest crate) - floor(0.15 × declared)

I will compare these two numbers and pick whichever is larger. I will not invoke generic reasoning about "consistency" or "variance" when the math gives a clear answer.

## Route Selection

I noticed in my record that I chose main route repeatedly without actually calculating night route's advantage. The math often favored night route for moderate-to-high declarations, especially when my smallest crate was close in value to my largest. I will do the arithmetic every time, not assume main is safer.

When my smallest crate is significantly smaller than my total value, night route becomes more attractive because I'm avoiding proportionally more duty than I'm losing in crate value.

## Competitive Positioning

I will track scores but not let them drive my declaration strategy. My job each round is to maximize my own score that round, not to match opponents' previous declarations or to optimize for relative position mid-game. The only time position matters is understanding that in the final round I still want to maximize absolute score, not take variance gambles.

I ended with 311 points, finishing second. This was solid play mechanically—I did not get penalized for false declarations and I chose reasonable routes—but I underused the night route when the math supported it. That is where my next game improves.