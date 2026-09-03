---
game: gen_harbor_customs
model: gemini
condition: win
seed: 7
round: 1
chars: 942
---
To maximize my score in Harbor Customs, I will follow this strategy:

- During the declare stage, I will identify the highest-valued crate in my hold. I will declare exactly that crate's value. This is the absolute minimum I can declare to pass the spot check without triggering the -40 penalty and the full-value duty.
- I will never declare 0 or the true total sum of my crates, as under-declaring the heaviest crate incurs severe penalties, and declaring the true total wastes points on unnecessary taxes.
- During the route stage, I will evaluate my smallest crate. I will calculate 15% of my declared value (0.15 x heaviest crate). 
- If my smallest crate's value is less than 0.15 times my declared value, I will choose the `night` route to save on duty at the cost of a very cheap crate. 
- Otherwise (which is the vast majority of the time, since 15% of the maximum 40 is only 6), I will choose the `main` route to keep all my crates.