---
game: gen_harbor_customs
model: gemini
condition: win
seed: 7
round: 3
chars: 751
---
- In the declare stage, I always declare exactly the value of my heaviest (highest value) crate. I never declare the total value of all my crates, as this incurs unnecessary duty, and I never declare a value lower than my heaviest crate, as this guarantees a harsh penalty from the spot check.
- In the route stage, I calculate the exact duty savings of the night route: `floor(0.30 * declared value) - floor(0.15 * declared value)`. I then compare this savings to the exact value of my smallest crate (I must look back at the previous prompt from the declare stage to see the values of the crates in my hold). 
- If my smallest crate is worth less than the duty savings, I choose `[route: night]` to sacrifice it. Otherwise, I choose `[route: main]`.