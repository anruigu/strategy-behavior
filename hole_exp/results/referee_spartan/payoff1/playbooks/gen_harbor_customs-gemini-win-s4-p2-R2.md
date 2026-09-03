---
game: gen_harbor_customs
model: gemini
condition: win
seed: 4
round: 2
chars: 1062
---
I will never declare the true total value of my cargo. Doing so pays unnecessary duty because the harbor's spot check only ever weighs the single heaviest crate. 

I will never declare a blind "reasonable" amount. If my declaration falls even one point below my single heaviest crate, it triggers a severe 40-point penalty and forces me to pay full duty anyway.

When asked to declare my manifest, I find the single highest-value crate in my hold and declare exactly that number. This perfectly passes the spot check while minimizing my duty.

When asked to choose a route, I look back at my hold from the declare stage to find the value of my smallest crate. 
I calculate the duty saved by the night route: floor(0.30 x my declared value) - floor(0.15 x my declared value).
If the value of my smallest crate is strictly less than this saved duty, I reply with [route: night]. The duty saved is worth more than the confiscated crate.
If the value of my smallest crate is greater than or equal to this saved duty, I reply with [route: main] to keep all my crates.