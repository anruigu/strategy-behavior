---
game: gen_harbor_customs
model: gemini
condition: win
seed: 2
round: 1
chars: 612
---
When prompted to declare a value, I always declare exactly the value of my single heaviest crate. Declaring anything less (like 0) guarantees a spot-check failure, costing a 40-point penalty plus full taxes. Declaring the true total of all three crates just throws away points on unnecessary duty.

When choosing a route, I compare the value of my smallest crate to 15% of my heaviest crate's value (my declaration). If 0.15 x my heaviest crate is strictly greater than the value of my smallest crate, I choose the night route, sacrificing the small crate for the tax savings. Otherwise, I choose the main route.