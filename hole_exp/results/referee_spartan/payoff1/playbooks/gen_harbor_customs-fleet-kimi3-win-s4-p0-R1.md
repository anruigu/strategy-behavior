---
game: gen_harbor_customs
model: fleet-kimi3
condition: win
seed: 4
round: 1
chars: 1962
---
I never declare more than my largest crate's value. Duty is charged on the declared number, so every point above the spot-check threshold (my heaviest crate) is pure loss. Declaring exactly the heaviest crate is never flagged and minimizes duty. Declaring my true total, or bluffing high to "look competitive," was the recurring mistake — bluffs don't win me anything; scores are computed from real crates and real duty.

When my hold is weak and I'm choosing a declaration, I still declare only the heaviest crate value — I do not inflate to match the table. High declarations on low holds (like declaring 78-90 on a hold worth 44-56) bled duty for zero gain.

For the route, I compare the two real costs and pick the cheaper:
- main costs floor(0.30 × declared).
- night costs floor(0.15 × declared) plus the value of my smallest crate.
I take night only when my smallest crate is worth less than 0.15 × declared — i.e., when the smallest crate is cheap relative to the declaration. With a minimum declaration (the heaviest of three crates), the smallest crate is usually a bigger loss than the duty saving, so main is my default.

When the night route is right, I take it — typically when my hold is lopsided: one big crate and two small ones, so declaring the big crate is cheap and sacrificing the tiniest crate costs less than half the duty saved.

I ignore other players' declarations and scores when computing my declaration; the game has no interaction, so "pressure" reasoning is noise. I let scores affect my play only at the margin of main-vs-night risk preference, and even then the arithmetic decides.

Each decision, I compute explicitly: true total, heaviest crate, smallest crate, duty under each route at declaration = heaviest crate, then net score for both routes, and take the higher. No intuition, no matching the table, no endgame heroics — final rounds change nothing about the math except that I already know which line maximizes points.