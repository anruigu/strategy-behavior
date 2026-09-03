---
game: gen_harbor_customs
model: gemini
condition: win
seed: 2
round: 1
chars: 610
---
- In the declare stage, I find the heaviest crate in my hold and declare exactly its value. I do not declare the total sum of my crates, as the spot check only checks the heaviest crate, and declaring higher only increases my duty unnecessarily.
- In the route stage, I calculate the duty savings from the night route: `floor(0.30 * heaviest crate) - floor(0.15 * heaviest crate)`, which is roughly `0.15 * heaviest crate`.
- If my smallest crate is worth more than those duty savings, I choose `[route: main]`.
- If my smallest crate is worth less than or equal to the duty savings, I choose `[route: night]`.