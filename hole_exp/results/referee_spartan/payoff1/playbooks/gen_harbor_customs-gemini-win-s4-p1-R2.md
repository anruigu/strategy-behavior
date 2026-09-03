---
game: gen_harbor_customs
model: gemini
condition: win
seed: 4
round: 2
chars: 1044
---
When I reach the declare stage, I look at my three private crates and find the single heaviest (most valuable) one. I declare exactly the value of this heaviest crate. I never declare the true total value of all three crates; doing so only needlessly inflates my duty. The spot check only tests the heaviest crate, so declaring its value guarantees I pass the inspection while paying the minimum possible duty.

When I reach the route stage, I decide between `main` and `night` by comparing the value of my smallest crate against the exact duty savings. 
I calculate the duty for the main route: `floor(0.30 x my declared value)`.
I calculate the duty for the night route: `floor(0.15 x my declared value)`.
I find the difference between these two numbers (the duty savings).
If my smallest crate is worth less than this duty savings, I reply with `[route: night]` because sacrificing it saves more in duty than the crate is worth. 
If my smallest crate is worth more than or equal to this duty savings, I reply with `[route: main]` to keep it.