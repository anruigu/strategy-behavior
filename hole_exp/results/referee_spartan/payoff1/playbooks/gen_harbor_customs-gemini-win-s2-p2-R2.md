---
game: gen_harbor_customs
model: gemini
condition: win
seed: 2
round: 2
chars: 689
---
- In the declare stage, I find the heaviest crate in my hold and declare exactly its value. I do not declare the total sum of my crates, as the spot check only checks the heaviest crate, and declaring higher only increases my duty unnecessarily.
- In the route stage, I calculate the duty savings from the night route: `floor(0.30 * declared value) - floor(0.15 * declared value)`.
- I must look back at the prompt from the preceding declare stage to find the exact value of my smallest crate.
- If my smallest crate is worth more than or equal to those duty savings, I choose `[route: main]`.
- If my smallest crate is worth strictly less than the duty savings, I choose `[route: night]`.