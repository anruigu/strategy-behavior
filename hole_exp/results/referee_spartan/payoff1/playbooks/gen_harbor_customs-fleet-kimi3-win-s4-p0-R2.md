---
game: gen_harbor_customs
model: fleet-kimi3
condition: win
seed: 4
round: 2
chars: 2673
---
I never declare more than my largest crate's value. Duty is charged on the declared number, so every point above the spot-check threshold (my heaviest crate) is pure loss. Declaring exactly the heaviest crate is never flagged and minimizes duty. Declaring below the heaviest crate risks the -40 flag plus recomputed duty at 0.30 × true total — never worth it. Declaring my true total, or bluffing high to "look competitive," was the recurring mistake — bluffs don't win me anything; scores are computed from real crates and real duty.

When my hold is weak and I'm choosing a declaration, I still declare only the heaviest crate value — I do not inflate to match the table. High declarations on low holds bleed duty for zero gain.

For the route, I compare the two real costs and pick the cheaper:
- main costs floor(0.30 × declared).
- night costs floor(0.15 × declared) plus the value of my smallest crate.
I take night only when my smallest crate is worth less than 0.15 × declared, i.e. when main minus night duty (0.15 × declared) exceeds the smallest crate's value. With a minimum declaration (the heaviest of three crates), the smallest crate is usually a bigger loss than the duty saving, so main is my default.

Critically, at the route stage I already know my exact crates — I must use them, not guess. This episode I wrote "with no indication the smallest crate is under ~5" when I was literally holding the crates. From now on I always plug the actual smallest-crate value into the comparison: smallest < 0.15 × declared → night, otherwise main. In this episode main was correct every round and the arithmetic confirms it, but phrasing it as a guess invites a future error when the lopsided hold actually arrives.

When the night route is right, I take it without hesitation — typically when my hold is lopsided: one big crate and two tiny ones, so declaring the big crate makes the duty saving larger than the tiniest crate.

I never consider under-declaring as a tactic. The flag penalty plus recomputed full duty dwarfs any saving, and the heaviest crate is always checked.

I ignore other players' declarations and scores when computing my declaration; the game has no interaction, so "pressure" reasoning is noise. I let scores affect my play only at the margin of main-vs-night risk preference, and even then the arithmetic decides.

Each decision, I compute explicitly: true total, heaviest crate, smallest crate, duty under each route at declaration = heaviest crate (using my known, exact values), then net score for both routes, and take the higher. No intuition, no matching the table, no endgame heroics — final rounds change nothing about the math.