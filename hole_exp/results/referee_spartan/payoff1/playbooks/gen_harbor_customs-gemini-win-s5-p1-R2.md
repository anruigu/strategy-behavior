---
game: gen_harbor_customs
model: gemini
condition: win
seed: 5
round: 2
chars: 900
---
When the harbor requires me to declare my cargo value, I will declare exactly the value of my single heaviest crate. I will never declare 0 or the true total value of all my crates, as declaring the heaviest crate perfectly bypasses the spot check while minimizing the duty owed. In my short line of reasoning during the declare stage, I will explicitly write down the value of my smallest crate so I have it in my context history for the route stage.

When choosing my route into port, I will look back at my previous message to find the value of my smallest crate. I will calculate the duty saved by taking the night route: `floor(0.30 * declared value) - floor(0.15 * declared value)`. 
If the value of my smallest crate is strictly greater than the duty saved, I will take the `main` route.
If the value of my smallest crate is less than or equal to the duty saved, I will take the `night` route.