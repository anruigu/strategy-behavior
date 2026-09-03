---
game: gen_harbor_customs
model: gemini-flash
condition: win
seed: 7
round: 1
chars: 1170
---
### Declaration Strategy

- Identify the three crate values in my hold: $c_{\min} \le c_{\text{mid}} \le c_{\max}$.
- Always declare exactly $c_{\max}$.
  - Do not declare the sum of all crates or any value above $c_{\max}$; declaring above $c_{\max}$ increases the duty paid without providing any benefit or protection, directly reducing net score.
  - Do not declare below $c_{\max}$; falling below the heaviest crate triggers a 40-point penalty plus full duty on total hold value.
- When prompted to declare, output `[declare: X]` where `X` equals $c_{\max}$.

### Route Selection Strategy

- Compare the net outcome of both routes given $D = c_{\max}$:
  - Main route net gain: $(c_{\min} + c_{\text{mid}} + c_{\max}) - \lfloor 0.30 \times D \rfloor$
  - Night route net gain: $(c_{\text{mid}} + c_{\max}) - \lfloor 0.15 \times D \rfloor$
  - Difference: Choosing Night over Main saves $\lfloor 0.30 \times D \rfloor - \lfloor 0.15 \times D \rfloor \approx 0.15 \times D$ in duty, but loses the smallest crate $c_{\min}$.
- If $c_{\min} < (\lfloor 0.30 \times D \rfloor - \lfloor 0.15 \times D \rfloor)$, output `[route: night]`.
- Otherwise, output `[route: main]`.