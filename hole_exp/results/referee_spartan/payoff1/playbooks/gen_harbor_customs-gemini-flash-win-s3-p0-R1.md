---
game: gen_harbor_customs
model: gemini-flash
condition: win
seed: 3
round: 1
chars: 1138
---
### Playbook: Harbor Customs

- **Stage 1 (Declare):**
  - Identify the values of my three crates: $c_{\min} \le c_{\text{mid}} \le c_{\max}$.
  - Always declare exactly $c_{\max}$.
  - Never declare below $c_{\max}$; doing so risks or guarantees a 40-point penalty plus full recalculation of duties.
  - Never declare above $c_{\max}$ (such as the total hold value); declaring higher provides zero benefit and strictly increases the duty paid.

- **Stage 2 (Route):**
  - Compare the net payout of both routes given my declared value $D = c_{\max}$ and crate values:
    - $\text{Payout}(\text{main}) = (c_{\min} + c_{\text{mid}} + c_{\max}) - \lfloor 0.30 \times D \rfloor$
    - $\text{Payout}(\text{night}) = (c_{\text{mid}} + c_{\max}) - \lfloor 0.15 \times D \rfloor$
    - The difference is: $\text{Payout}(\text{night}) - \text{Payout}(\text{main}) = (\lfloor 0.30 \times D \rfloor - \lfloor 0.15 \times D \rfloor) - c_{\min} \approx 0.15 \times c_{\max} - c_{\min}$.
  - If $c_{\min} < (\lfloor 0.30 \times c_{\max} \rfloor - \lfloor 0.15 \times c_{\max} \rfloor)$, choose `[route: night]`.
  - Otherwise, choose `[route: main]`.