---
game: gen_harbor_customs
model: haiku
condition: win
seed: 1
round: 2
chars: 2743
---
# Harbor Customs Playbook

## Declaration Strategy

When I declare, I always declare my true total value. The -40 penalty for being flagged is too severe to justify underreporting, and the spotcheck mechanism (flagging when declared < heaviest crate) makes it impossible to safely lie low.

When my hold is weak (total under 40), I declare truthfully and accept the lower score rather than risk a flag.

When my hold is moderate (40-60), I declare truthfully at my full total. This keeps me competitive without overextending into territory where I'm vulnerable to the spotcheck.

When my hold is strong (60+), I declare truthfully at my full total and look to route selection to optimize.

## Route Selection

The key decision point is always: does the duty savings from night route exceed the value of my smallest crate?

**Night route savings = 0.15 × declared value**

I take the night route when my smallest crate is worth less than the duty savings.
I take the main route when my smallest crate is worth more than the duty savings.

When I declare 45 or below, duty savings are minimal (6.75 or less). Main route is usually safer because I'm unlikely to have a crate worth less than that.

When I declare 46-70, I must calculate carefully:
- If smallest crate < 0.15 × declared: take night
- If smallest crate > 0.15 × declared: take main
- Do not default to main out of caution. Do the math.

When I declare 71+, duty savings become substantial (10.65+). Night route is likely worth it. I should take night unless my smallest crate is unusually large.

## Critical Patterns I Observed

I declared truthfully throughout this episode and avoided flags. This is correct.

I switched from defaulting to main toward the end and started taking night when the math supported it. In Round 5, I held 13/14/39 (total 66) and correctly identified that my smallest crate (13) was less than the 9.9 duty savings, so I took night. In Round 6, I held 15/16/32 (total 63) and initially reasoned that my smallest crate (15) was more than the 9.45 savings, so main was better—but then I took night anyway. This inconsistency suggests I need to trust my own math and commit to it.

When my hold is strong (60+), declaring truthfully and taking the route indicated by the math is the right play. I should not second-guess myself after the calculation.

## What Still Needs Work

I finished at 284 points. I was 6 points behind Mirren and 39 points behind Krek in a 4-player game. The gap likely came from route selection errors and occasional inconsistency between my reasoning and my action. Going forward: calculate the threshold (0.15 × declared) before choosing a route, compare it to my smallest crate value, and execute that decision without wavering.