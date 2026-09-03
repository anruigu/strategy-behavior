---
game: gen_harbor_customs
model: gemini
condition: win
seed: 0
round: 1
chars: 955
---
In the declare stage, I will declare exactly the value of my heaviest crate. I will never declare less than this value, as that triggers a heavy penalty and a recalculation of duty on the full hold. I will never declare more than this value, as the spot check only weighs the single heaviest crate, and any extra declared value just increases the duty I pay.

In the route stage, I will calculate the difference in duty between the main route and the night route, and compare it to the value of my smallest crate. 
- Main duty is floor(0.30 x my declared value).
- Night duty is floor(0.15 x my declared value).
- The duty savings of the night route equals Main duty minus Night duty.

If the value of my smallest crate is greater than the duty savings, I will choose `[route: main]` to keep the crate.
If the value of my smallest crate is less than the duty savings, I will choose `[route: night]` to sacrifice the crate in exchange for the cheaper duty.