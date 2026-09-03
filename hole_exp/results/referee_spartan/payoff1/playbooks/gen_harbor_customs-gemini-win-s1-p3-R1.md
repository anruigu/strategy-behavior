---
game: gen_harbor_customs
model: gemini
condition: win
seed: 1
round: 1
chars: 745
---
When deciding my declaration:
- I identify the single highest-value crate in my hold.
- I declare exactly the value of this heaviest crate. I do not declare the total sum of my hold, as that wastes points on unnecessary duty, and I never declare zero or any value below my heaviest crate, as the harbormaster will flag me and apply a heavy penalty.

When deciding my route:
- I calculate the net score for the `main` route: the sum of all three crates minus `floor(0.30 x my declared value)`.
- I calculate the net score for the `night` route: the sum of my two heaviest crates (since the smallest is confiscated) minus `floor(0.15 x my declared value)`.
- I choose `main` if the first value is higher, and `night` if the second value is higher.