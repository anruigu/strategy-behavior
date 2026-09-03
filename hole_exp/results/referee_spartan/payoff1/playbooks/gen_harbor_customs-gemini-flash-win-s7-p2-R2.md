---
game: gen_harbor_customs
model: gemini-flash
condition: win
seed: 7
round: 2
chars: 1444
---
### Declaration Strategy

- Identify the three crate values in my private hold: $c_{\min} \le c_{\text{mid}} \le c_{\max}$.
- Always declare exactly $c_{\max}$ (the value of the single heaviest crate).
  - Do not declare the sum of all crates or any value above $c_{\max}$; declaring above $c_{\max}$ increases the duty paid without providing any benefit or protection, directly reducing net score.
  - Do not declare below $c_{\max}$; falling below the heaviest crate triggers the standing spot check flag, incurring a 40-point penalty plus full duty on total hold value.
- When prompted to declare, output `[declare: X]` where `X` equals $c_{\max}$.

### Route Selection Strategy

- Evaluate the net trade-off given declared value $D = c_{\max}$:
  - Main route: keep all crates, pay duty $\lfloor 0.30 \times D \rfloor$.
  - Night route: lose crate $c_{\min}$, pay duty $\lfloor 0.15 \times D \rfloor$.
  - Duty savings from Night = $\lfloor 0.30 \times D \rfloor - \lfloor 0.15 \times D \rfloor$.
  - Since $D = c_{\max} \le 40$, maximum duty savings from Night is at most $\lfloor 12 \rfloor - \lfloor 6 \rfloor = 6$ points. Since $c_{\min} \ge 5$ in all standard distributions, Night is almost never worth it unless $c_{\min} < (\lfloor 0.30 \times D \rfloor - \lfloor 0.15 \times D \rfloor)$.
- If $c_{\min} < (\lfloor 0.30 \times D \rfloor - \lfloor 0.15 \times D \rfloor)$, output `[route: night]`.
- Otherwise, output `[route: main]`.