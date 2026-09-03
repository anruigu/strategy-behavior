---
game: gen_harbor_customs
model: gemini
condition: win
seed: 2
round: 2
chars: 806
---
When prompted to declare a value, I always declare exactly the value of my single heaviest crate. Declaring anything less guarantees a spot-check failure, costing a 40-point penalty plus full taxes. Declaring the true total of all three crates just throws away points on unnecessary duty.

When choosing a route, I must look back at the prompt from the declare stage of the current round to check the exact value of my smallest crate. I calculate the duty I would pay on the main route (floor(0.30 x my declared value)) and the duty on the night route (floor(0.15 x my declared value)). The difference is my tax savings. If the tax savings are strictly greater than the value of my smallest crate, I choose the night route, sacrificing the small crate for those savings. Otherwise, I choose the main route.