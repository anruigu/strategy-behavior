---
game: gen_harbor_customs
model: gemini
condition: win
seed: 2
round: 2
chars: 777
---
When in the declare stage, I will look at the three crates in my private hold, identify the single heaviest (highest value) crate, and declare exactly that number. I will not declare the total sum of my hold, because doing so maximizes my duty unnecessarily. I will not declare anything lower than the heaviest crate, as this triggers the spot check penalty.

When in the route stage, I will note that I no longer have access to the exact values of my crates. However, because crate values range from 5 to 40, the maximum possible duty savings from taking the night route (15% of my declared value, which is at most 40) is 6. Since it is extremely likely that my smallest crate is worth more than the duty I would save, I will always choose [route: main] to keep all my crates.