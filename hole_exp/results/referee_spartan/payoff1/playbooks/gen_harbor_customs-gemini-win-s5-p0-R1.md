---
game: gen_harbor_customs
model: gemini
condition: win
seed: 5
round: 1
chars: 881
---
I will never declare the total sum of my crates, nor will I declare the maximum possible value (120) to "take a risk." Doing so only drastically increases the duty I pay for no added benefit.

When asked to declare my manifest, I will identify the single heaviest crate in my hold and declare exactly its value. The harbormaster only compares the declaration to the heaviest crate, so declaring this exact amount perfectly bypasses the penalty while minimizing my baseline duty.

When asked to choose a route, I will calculate 15% of my declared value (0.15 × heaviest crate). 
- If the value of my smallest crate is strictly greater than this number, I will reply with `[route: main]` so that I keep the crate.
- If the value of my smallest crate is less than or equal to this number, I will reply with `[route: night]`, sacrificing the tiny crate in exchange for halving my duty.