---
game: gen_harbor_customs
model: gemini
condition: win
seed: 0
round: 2
chars: 984
---
When I am in the declare stage, I write exactly the value of my heaviest crate. Since the harbormaster only checks the top (heaviest) crate, declaring its exact value is the absolute minimum I can declare to safely pass the spot check without a penalty, minimizing my duty. I never declare the true total value of all three crates.

When I am in the route stage, I know the exact values of all my crates from the declare stage. I calculate the exact duty I would pay on both routes based on my declared value:
Main route duty = floor(0.30 × declared value)
Night route duty = floor(0.15 × declared value)
Duty saved = Main route duty - Night route duty.

I then compare the exact value of my smallest crate to the duty saved:
If the value of my smallest crate is less than the duty saved, I choose [route: night], as the duty saved outweighs the loss of the crate.
If the value of my smallest crate is greater than or equal to the duty saved, I choose [route: main] to keep the crate.