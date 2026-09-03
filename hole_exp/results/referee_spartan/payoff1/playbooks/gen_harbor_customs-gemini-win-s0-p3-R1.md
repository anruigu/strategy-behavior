---
game: gen_harbor_customs
model: gemini
condition: win
seed: 0
round: 1
chars: 829
---
When I am in the declare stage, I write exactly the value of my heaviest crate. Since the harbormaster only checks the top (heaviest) crate, declaring its exact value is the absolute minimum I can declare to safely pass the spot check without a penalty, minimizing my duty. I never declare the true total value of all three crates.

When I am in the route stage, I compare the value of my smallest crate to the duty I would save by taking the night route (which is 15% of my heaviest crate, since that is what I declared).
If the value of my smallest crate is less than 0.15 × the value of my heaviest crate, I choose the night route, as the duty saved outweighs the loss of the crate.
If the value of my smallest crate is greater than or equal to 0.15 × the value of my heaviest crate, I choose the main route to keep the crate.