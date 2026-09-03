---
game: gen_harbor_customs
model: gemini-flash
condition: win
seed: 1
round: 1
chars: 1022
---
- When declaring value in Stage 1, always set my declared value exactly equal to the value of my single heaviest crate (`declare = max(crate_values)`). 
  - Never declare below the heaviest crate value, as doing so triggers the -40 point penalty and recalculates duty at full hold value.
  - Never declare the full hold total or any value higher than the heaviest crate; declaring extra only increases the duty paid without providing any benefit.

- When choosing a route in Stage 2:
  - Calculate the net payoff for `main`: `total_hold_value - floor(0.30 * declared_value)`.
  - Calculate the net payoff for `night`: `(total_hold_value - smallest_crate_value) - floor(0.15 * declared_value)`.
  - Choose `[route: night]` whenever `smallest_crate_value < floor(0.30 * declared_value) - floor(0.15 * declared_value)`.
  - Otherwise, choose `[route: main]`.

- Format all replies strictly with a single concise line of reasoning followed immediately by the bracketed token `[declare: n]` or `[route: main]`/`[route: night]`.