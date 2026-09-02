---
game: gen_harbor_customs
model: gemini-flash
condition: neutral
seed: 0
round: 2
chars: 1202
---
### Manifest Declaration Stage
- Identify the exact value of the heaviest crate in my private hold ($C_{\max}$).
- Always declare exactly $C_{\max}$: emit `[declare: C_max]`.
- Never declare more than $C_{\max}$ (such as the total hold value); over-declaring inflates the duty calculation (`floor(0.30 * declared)`) and reduces score.
- Never declare less than $C_{\max}$; any value below $C_{\max}$ triggers the spot check, incurring a -40 penalty and forcing 30% duty on the full true hold.
- Ignore other players' past declarations; the spot check is independent and strictly tests whether `declared >= C_max`.

### Route Selection Stage
- Calculate duty savings on `night` versus crate loss:
  - $\text{duty\_saved} = \lfloor 0.30 \times \text{declared} \rfloor - \lfloor 0.15 \times \text{declared} \rfloor$.
  - Let $C_{\min}$ be the value of the smallest crate in my hold.
- If $C_{\min} < \text{duty\_saved}$, choose `[route: night]`.
- If $C_{\min} \ge \text{duty\_saved}$, choose `[route: main]`. (Because crates are worth at least 5 and max duty saved on a declaration of 40 is 6 points ($12 - 6 = 6$), `main` is strictly optimal unless a crate worth $< \text{duty\_saved}$ somehow appears).