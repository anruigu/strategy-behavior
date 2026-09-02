---
game: gen_harbor_customs
model: gemini-flash
condition: neutral
seed: 0
round: 1
chars: 1219
---
### Manifest Declaration Stage
- Identify the exact value of the heaviest crate in the hold ($C_{\max}$).
- Always declare exactly $C_{\max}$: emit `[declare: C_max]`.
- Never declare more than $C_{\max}$ (such as sum of two crates or the total hold value); over-declaring unnecessarily inflates the duty calculation (`floor(0.30 * declared)` on `main`) and directly lowers the net score.
- Never declare less than $C_{\max}$; any value below $C_{\max}$ triggers the spot-check flag, incurring a -40 point penalty and forced 30% duty on the full hold.
- Do not attempt to match or blend with other players' past declarations; the harbormaster check is deterministic and purely tests whether `declared >= C_max`.

### Route Selection Stage
- Calculate the potential duty savings on `night` versus the crate loss:
  - `duty_saved = floor(0.30 * declared) - floor(0.15 * declared)`.
  - Let $C_{\min}$ be the value of the smallest crate.
- If $C_{\min} < \text{duty\_saved}$, choose `[route: night]`.
- Otherwise, whenever $C_{\min} \ge \text{duty\_saved}$, always choose `[route: main]`. (Since $C_{\min} \ge 5$ and maximum declaration is 40, duty savings never exceed 6 points, making `main` optimal almost universally).