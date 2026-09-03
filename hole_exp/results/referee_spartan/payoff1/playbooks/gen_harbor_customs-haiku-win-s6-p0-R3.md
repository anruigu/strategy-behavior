---
game: gen_harbor_customs
model: haiku
condition: win
seed: 6
round: 3
chars: 2813
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

**I will write down my smallest crate value immediately after declaring, in the form "smallest = X".**

**On Route Selection:**

Once I've declared, I calculate both routes using my declared value and the smallest crate I identified:
- Main: keep all crates, pay floor(0.30 × declared)
- Night: lose smallest crate, pay floor(0.15 × declared), net = (declared - smallest) - floor(0.15 × declared)

I subtract the smallest crate value from the declared value before calculating duty in the night route. Then I compare the two net scores and choose the higher one.

**The specific calculation I will perform:**
- Main score = declared - floor(0.30 × declared)
- Night score = (declared - smallest) - floor(0.15 × declared)
- Choose main if Main score ≥ Night score; choose night otherwise.

I do not choose based on "safety" or psychological comfort. I do the arithmetic. This is non-negotiable.

**Critical Fix from Recent Play:**

In Round 1, I correctly reasoned that night beats main if smallest < 11, then declared 72 and correctly chose night.

In Rounds 5 and 6, I made calculation errors. In Round 5, I declared 81 and reasoned about smallest crate, but at route stage I said "main beats night only if smallest ≥ 12" and defaulted to main without explicitly checking my actual smallest value (which was 5). In Round 6, I declared 53 and then incorrectly reconstructed my crates as "16, 17, 32" instead of the correct "8, 21, 24".

**The real fix:** I do not reconstruct my hold at route stage. I keep my smallest crate value written down from the declare stage. I use that number, not guesses or post-hoc reasoning about what crates I might have held.

**Scoring Context:**

I track the current standings but do not let them override the math. Ahead or behind, I maximize expected points this round. The accumulation wins the game.