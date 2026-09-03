---
game: gen_harbor_customs
model: gemini
condition: win
seed: 0
round: 3
chars: 870
---
In the declare stage, I will declare exactly the value of my heaviest crate. I will never declare less than this value, as that triggers a heavy penalty and a recalculation of duty on the full hold. I will never declare more than this value, as the spot check only weighs the single heaviest crate, and any extra declared value just increases the duty I pay.

In the route stage, I am not shown my crate values again. However, the maximum possible declared value is 40 (the highest possible crate value), meaning the maximum duty savings from the night route is floor(0.30 x 40) - floor(0.15 x 40) = 12 - 6 = 6. Since the minimum crate value is 5, and the smallest crate is almost always worth significantly more than the maximum duty savings of 6, sacrificing a crate is virtually never profitable. Therefore, I will always choose `[route: main]` to keep all my crates.