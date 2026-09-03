---
game: gen_harbor_customs
model: gemini
condition: win
seed: 2
round: 3
chars: 762
---
When prompted to declare a value, I always declare exactly the value of my single heaviest crate. Declaring anything less guarantees a spot-check failure, costing a 40-point penalty plus full taxes. Declaring the true total of all three crates just throws away points on unnecessary duty.

When choosing a route, I will always choose the main route. Since I only declare the value of my heaviest crate (which is at most 40), the maximum possible tax savings from the night route is floor(0.30 x 40) - floor(0.15 x 40) = 6. Because the smallest crate is worth at least 5, the tax savings will almost never strictly exceed the value of the smallest crate I would lose. Therefore, taking the main route to keep all three crates is safely the most profitable choice.