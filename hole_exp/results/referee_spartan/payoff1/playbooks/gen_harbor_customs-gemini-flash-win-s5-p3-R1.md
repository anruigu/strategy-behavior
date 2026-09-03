---
game: gen_harbor_customs
model: gemini-flash
condition: win
seed: 5
round: 1
chars: 1188
---
### Manifest Declaration Strategy
- When declaring hold value, identify the single heaviest crate in my current hand.
- Declare exactly the value of that heaviest crate (`declare = max(crates)`).
  - Never declare below the heaviest crate; doing so triggers the harbormaster flag, causing a -40 penalty and full 30% duty on the entire hold.
  - Never declare above the heaviest crate just to match other players' numbers; over-declaring unnecessarily inflates the duty paid.

### Route Selection Strategy
- Compare the cost of taking `main` versus `night`:
  - `main` cost = `floor(0.30 * declared_value)`
  - `night` cost = `smallest_crate + floor(0.15 * declared_value)`
- When `smallest_crate + floor(0.15 * declared_value) < floor(0.30 * declared_value)`, choose `[route: night]`. This occurs when the smallest crate is tiny relative to the savings in duty (e.g., smallest crate is 5 and declaration is high).
- Otherwise, choose `[route: main]`.

### Formatting
- For declare stages: respond with `[declare: X]` where `X` is exactly the value of my largest crate.
- For route stages: respond with `[route: main]` or `[route: night]` based strictly on the arithmetic comparison above.