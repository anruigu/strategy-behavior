---
game: gen_harbor_customs
model: haiku
condition: win
seed: 6
round: 1
chars: 1871
---
# Harbor Customs Playbook

**On Declaration:**

When I see my three crates, I immediately identify the heaviest one. This is the crate the spot check will weigh. I declare at least the value of my heaviest crate to avoid the -40 penalty. If my heaviest crate is worth H and my total is T, I never declare below H.

When choosing whether to declare my true total or something lower, I compare:
- Main route honest: T - floor(0.30T)
- Night route honest: (T - smallest) - floor(0.15T)
- Any flagged route: (T - smallest) - 40 - floor(0.30T)

I calculate which gives the highest score and declare accordingly. Honest declaration of true total usually wins because the penalty is harsh.

When my crates are low-value and close together in worth (like 6, 8, 22 or 8, 8, 15), I declare closer to my actual total because the spread is small and the night route's loss of the smallest crate is a small sacrifice relative to the duty savings—but only if it beats the main route math.

**On Route Selection:**

Once I've declared, I calculate both routes with my declared value:
- Main: keep all crates, pay floor(0.30 × declared)
- Night: lose smallest crate, pay floor(0.15 × declared)

I choose whichever leaves me with more points. I do not choose based on "safety" or psychological comfort. I do the arithmetic.

When I'm in the lead late in the game, I should still do the math rather than defaulting to "main route is safer." The math is what matters.

**What Did Not Work:**

I defaulted to the main route multiple times without actually comparing it to the night route mathematically. This was a mistake. I need to calculate both outcomes every single time before declaring.

I declared conservatively when ahead, but this may have left points on the table. The goal is maximum score, not maximum safety. When the math says night is better, I should take it even if ahead.