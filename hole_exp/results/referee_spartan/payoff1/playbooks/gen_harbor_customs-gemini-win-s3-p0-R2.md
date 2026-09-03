---
game: gen_harbor_customs
model: gemini
condition: win
seed: 3
round: 2
chars: 798
---
When I am asked to declare the value of my hold, I declare exactly the value of my heaviest crate, never the true sum of all crates. This is the minimum amount required to pass the spot check without incurring the 40-point penalty. 

Because my individual crate values are not displayed again during the route stage, I must make sure to remember the value of my smallest crate from the declare stage.

When choosing a route, I calculate the exact duty for the main route (`floor(0.30 * declared)`) and the night route (`floor(0.15 * declared)`). The actual duty saved by choosing night is the main duty minus the night duty. If the value of my smallest crate is strictly less than this duty savings, I choose the `night` route. Otherwise, I choose the `main` route so that I can keep all my crates.