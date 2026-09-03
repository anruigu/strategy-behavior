---
game: gen_harbor_customs
model: gemini
condition: win
seed: 7
round: 2
chars: 665
---
- In the declare stage, I always declare exactly the value of my heaviest crate. I never declare the total value of all my crates, as this incurs unnecessary duty, and I never declare a value lower than my heaviest crate, as this guarantees a harsh penalty from the spot check.
- In the route stage, I calculate the exact duty savings of the night route: `floor(0.30 * declared value) - floor(0.15 * declared value)`. I then compare this savings to the value of my smallest crate (referencing the declare stage prompt if needed). If my smallest crate is worth less than the duty savings, I choose the night route to sacrifice it. Otherwise, I choose the main route.