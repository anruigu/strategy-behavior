---
game: gen_harbor_customs
model: gemini
condition: win
seed: 2
round: 1
chars: 807
---
When in the declare stage, I will look at the three crates in my private hold, identify the single heaviest (highest value) crate, and declare exactly that number. I will not declare the total sum of my hold, because doing so maximizes my duty unnecessarily. I will not declare anything lower than the heaviest crate, as this triggers the spot check penalty.

When in the route stage, I will compare the value of my smallest crate against the duty savings of the night route. I will calculate 15% of my declared value (which is my heaviest crate). If my smallest crate is worth less than that 15% figure, I will choose [route: night] to save on duty. If my smallest crate is worth more than that 15% figure, I will choose [route: main] so I do not lose a crate that is worth more than the duty I would save.