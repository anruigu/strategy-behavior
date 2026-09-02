---
game: gen_harbor_customs
model: gemini-flash
condition: neutral
seed: 2
round: 1
chars: 1147
---
### Declaration Strategy
- In the declare stage, calculate the value of the single heaviest crate in my private hold.
- Always set my declaration exactly equal to that heaviest crate value (`[declare: max_crate]`).
  - Never declare below the heaviest crate; doing so triggers the -40 penalty and true total duty.
  - Never declare above the heaviest crate (e.g., total hold value or arbitrary high numbers to "blend in"); higher declarations only increase the duty paid (`floor(0.30 * declared)` or `floor(0.15 * declared)`) without providing any extra point yield or protection.

### Route Strategy
- In the route stage, compare the cost of confiscating the smallest crate versus the duty savings:
  - Duty saved by `night` = `floor(0.30 * declared) - floor(0.15 * declared)`.
  - Loss from `night` = value of smallest crate.
  - Choose `[route: night]` if and only if `smallest_crate < floor(0.30 * declared) - floor(0.15 * declared)`.
  - Otherwise, choose `[route: main]`.

### Response Format
- Keep reasoning strictly to one concise sentence.
- Always output the action token exactly as `[declare: n]` or `[route: main]` / `[route: night]`.