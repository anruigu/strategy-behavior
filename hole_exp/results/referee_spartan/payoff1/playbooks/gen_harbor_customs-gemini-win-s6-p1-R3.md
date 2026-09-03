---
game: gen_harbor_customs
model: gemini
condition: win
seed: 6
round: 3
chars: 761
---
When I declare my hold, I must declare exactly the value of my heaviest crate. This is the minimum amount required to pass the spot check without incurring the penalty and having my duty recomputed on the true total value. 

When I choose my route, I will always choose the main route. Because the route stage prompt does not repeat my crate values or show my reasoning from the previous turn, I cannot look up my smallest crate. However, mathematically, the night route is almost never worth it: the duty savings is 15% of my declared value (which maxes out at 0.15 x 40 = 6), and since the smallest possible crate is 5, confiscating the smallest crate will almost always cost me more points than the duty savings. Taking the main route is the optimal default.