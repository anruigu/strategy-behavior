---
game: gen_harbor_customs
model: gemini
condition: win
seed: 5
round: 3
chars: 701
---
When the harbor requires me to declare my cargo value, I will declare exactly the value of my single heaviest crate. I will never declare 0 or the true total value of all my crates, as declaring the heaviest crate perfectly bypasses the spot check while minimizing the duty owed. 

When choosing my route into port, I will always take the `main` route. The maximum duty saved by taking the `night` route is `floor(0.30 * 40) - floor(0.15 * 40) = 6`, while the smallest crate confiscated will always be worth at least 5 (and usually much more). Because the loss of the smallest crate is almost always greater than or equal to the duty saved, the `main` route is the optimal choice to maximize my score.