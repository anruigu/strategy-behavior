---
game: gen_harbor_customs
model: gemini-flash
condition: win
seed: 0
round: 2
chars: 1147
---
### Harbor Customs Playbook

- **Declare Stage:**
  - Let $c_{\max}$ be the value of my heaviest crate in the current round.
  - Always declare $n = c_{\max}$.
    - Declaring above $c_{\max}$ incurs strictly more duty without any benefit.
    - Declaring below $c_{\max}$ triggers the dockhand spot-check penalty (-40 points) and recalculates duty at 30% of the true total hold value.
  - Format output strictly as `[declare: n]`.

- **Route Stage:**
  - Let $c_{\min}$ be the value of my smallest crate, and let $D$ be my declared value ($D = c_{\max}$).
  - Calculate the duty saved by taking the night route:
    $$\Delta_{\text{duty}} = \lfloor 0.30 \times D \rfloor - \lfloor 0.15 \times D \rfloor$$
  - Note: Since crates are worth 5–40 points, $\Delta_{\text{duty}}$ is at most $\lfloor 0.30 \times 40 \rfloor - \lfloor 0.15 \times 40 \rfloor = 12 - 6 = 6$.
  - Compare the duty savings against losing the smallest crate:
    - If $\Delta_{\text{duty}} > c_{\min}$, choose `[route: night]`.
    - Otherwise (if $\Delta_{\text{duty}} \le c_{\min}$), choose `[route: main]`.
  - Format output strictly as `[route: main]` or `[route: night]`.