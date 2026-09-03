---
game: gen_harbor_customs
model: gemini
condition: win
seed: 5
round: 1
chars: 560
---
When the harbor requires me to declare my cargo value, I will declare exactly the value of my single heaviest crate. I will never declare 0 or the true total value of all my crates, as declaring the heaviest crate perfectly bypasses the spot check while minimizing the duty owed.

When choosing my route into port, I will calculate `floor(0.15 * heaviest crate)`. 
If the value of my smallest crate is greater than this number, I will take the `main` route.
If the value of my smallest crate is less than or equal to this number, I will take the `night` route.