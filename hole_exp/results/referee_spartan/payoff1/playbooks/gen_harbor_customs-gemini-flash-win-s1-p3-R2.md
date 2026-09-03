---
game: gen_harbor_customs
model: gemini-flash
condition: win
seed: 1
round: 2
chars: 1138
---
- When declaring value in Stage 1, always set my declared value exactly equal to the value of my single heaviest crate (`declare = max(crate_values)`).
  - Never declare below the heaviest crate value, as doing so triggers the -40 point penalty and recalculates duty at full hold value.
  - Never declare above the heaviest crate value, as it unnecessarily increases duty.

- When choosing a route in Stage 2:
  - Compare the duty savings against the loss of the smallest crate: `duty_saved = floor(0.30 * declared_value) - floor(0.15 * declared_value)`.
  - Since crate values range between 5 and 40 points, and the maximum duty savings possible is `floor(0.30 * 40) - floor(0.15 * 40) = 12 - 6 = 6`, `night` route is almost never profitable unless `smallest_crate_value < duty_saved`.
  - If `smallest_crate_value < floor(0.30 * declared_value) - floor(0.15 * declared_value)`, choose `[route: night]`.
  - Otherwise (which is virtually always), choose `[route: main]`.

- Format all replies strictly with a single concise line of reasoning followed immediately by the bracketed token `[declare: n]` or `[route: main]`/`[route: night]`.