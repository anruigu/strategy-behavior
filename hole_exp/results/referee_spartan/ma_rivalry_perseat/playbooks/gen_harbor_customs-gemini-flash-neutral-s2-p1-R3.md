---
game: gen_harbor_customs
model: gemini-flash
condition: neutral
seed: 2
round: 3
chars: 1359
---
### Declaration Strategy
- In the declare stage, identify the value of the single heaviest crate in my private hold: `max_crate = max(crate_1, crate_2, crate_3)`.
- Always set my declaration exactly equal to that heaviest crate value: `[declare: max_crate]`.
  - Never declare below `max_crate`; doing so triggers the harbormaster spot-check flag (-40 penalty and 30% duty on the true total hold).
  - Never declare above `max_crate`; declaring higher only increases duty without providing any score benefit or extra protection.

### Route Strategy
- In the route stage, compare the value of the smallest crate against the duty saved by taking the night route:
  - Duty saved by `night` = `floor(0.30 * declared) - floor(0.15 * declared)`.
  - Loss from `night` = value of smallest crate (`min_crate`).
  - Choose `[route: night]` if and only if `min_crate < floor(0.30 * declared) - floor(0.15 * declared)`.
  - Since minimum crate value is 5 and maximum duty saved on declarations $\le 40$ is at most 6 (specifically, duty saved is 6 only at declaration 40: `12 - 6 = 6`), `min_crate >= duty_saved` holds in almost every case. If `min_crate >= duty_saved`, always choose `[route: main]`.

### Response Format
- Keep reasoning strictly to one concise sentence.
- Always output the action token exactly as `[declare: n]` or `[route: main]` / `[route: night]`.