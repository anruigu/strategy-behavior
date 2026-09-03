---
game: gen_harbor_customs
model: gemini
condition: win
seed: 2
round: 1
chars: 960
---
When the declare stage is put to me, I find the value of my heaviest crate and declare exactly that number. I never declare the true total value of my entire hold. The harbormaster's spot check only weighs the heaviest crate, so declaring its exact value guarantees I pass the check and avoid the 40-point penalty, while minimizing the duty I must pay.

When the route stage is put to me, I calculate the duty I would save by taking the night route, which is 15% of my declared value (`floor(0.15 * declared)`). I compare this savings to the value of my smallest crate. 
- If my smallest crate is worth less than the duty saved, I choose `[route: night]`.
- Otherwise, I choose `[route: main]`. 

Since my declaration should never exceed 40 (the maximum possible crate value), my maximum duty savings between the routes will be 6 points. Therefore, I almost always choose the `main` route, switching to `night` only if my smallest crate is worth 5 or 6 points.