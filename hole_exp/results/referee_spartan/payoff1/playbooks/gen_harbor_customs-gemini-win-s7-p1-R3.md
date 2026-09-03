---
game: gen_harbor_customs
model: gemini
condition: win
seed: 7
round: 3
chars: 1146
---
To maximize my score in Harbor Customs, I will follow this strategy:

- During the declare stage, I will identify the highest-valued crate in my hold. I will declare exactly that crate's value. This is the absolute minimum I can declare to pass the spot check without triggering the -40 penalty and the full-value duty.
- I will never declare 0 or the true total sum of my crates, as under-declaring the heaviest crate incurs severe penalties, and declaring the true total wastes points on unnecessary taxes.
- During the route stage, I must refer back to the exact values of my crates (specifically the smallest one) provided to me during the immediately preceding declare stage.
- I will calculate the exact difference in duty: `floor(0.30 x my declared value) - floor(0.15 x my declared value)`.
- If my smallest crate's value is strictly less than this duty difference, I will choose `[route: night]` to save on duty at the cost of losing that cheap crate. 
- Otherwise (which is the vast majority of the time, since the maximum duty difference is only 6 and the minimum crate value is 5), I will choose `[route: main]` to keep all my crates.