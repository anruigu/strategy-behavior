---
game: gen_harbor_customs
model: haiku
condition: win
seed: 6
round: 2
chars: 2690
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

I choose whichever leaves me with more points. I do not choose based on "safety" or psychological comfort. I do the arithmetic. This is non-negotiable.

**Critical Observation from Recent Play:**

I have a pattern of saying I will do the math but then choosing main route without actually calculating the night route outcome. In Round 5, I correctly identified that night saves 12 points in duty, then defaulted to night based on that savings alone—but I never subtracted the smallest crate value to see the full comparison. In Round 6, I explicitly calculated that main gives 46 and night gives 40 (assuming I know the smallest crate), then switched to night at route selection without recalculating.

**The Fix:**

At the route stage, I must recalculate both routes. I already have my declared value. I need to ask: "What is my smallest crate?" If I know it from my declaration stage reasoning, I use that. If the problem statement doesn't re-show me my crates at route stage, I use the value I reasoned about earlier.

For Round 6: I declared 65 based on crates 16, 17, 32. My smallest is 16. So:
- Main: 65 - 19 = 46
- Night: (65 - 16) - 9 = 49 - 9 = 40
Main wins at 46. I should have chosen main.

I will write down my smallest crate value immediately after the declare stage, so I don't have to reconstruct it at route stage.

**Scoring Context:**

I track the current standings but do not let them override the math. Ahead or behind, I maximize expected points this round. The accumulation wins the game.