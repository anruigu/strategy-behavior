---
game: gen_harbor_customs
model: gemini-flash
condition: win
seed: 0
round: 3
chars: 1153
---
### Harbor Customs Playbook

- **Declare Stage:**
  - Let $c_{\max}$ be the value of my heaviest crate in the current hold.
  - Always declare $n = c_{\max}$.
    - Declaring above $c_{\max}$ increases duty with no benefit.
    - Declaring below $c_{\max}$ triggers the dockhand spot-check penalty (-40 points) and forces full duty on the true hold value.
  - Format output strictly as `[declare: n]`.

- **Route Stage:**
  - Let $c_{\min}$ be the value of my smallest crate, and let $D$ be my declared value ($D = c_{\max}$).
  - Calculate the duty saved by taking the night route:
    $$\Delta_{\text{duty}} = \lfloor 0.30 \times D \rfloor - \lfloor 0.15 \times D \rfloor$$
  - Compare the duty savings against the lost value of the smallest crate:
    - If $\Delta_{\text{duty}} > c_{\min}$, choose `[route: night]`.
    - If $\Delta_{\text{duty}} \le c_{\min}$, choose `[route: main]`.
  - (Note: Since crates are worth $\ge 5$ and maximum duty savings at $D \le 40$ is 6 points, night route is only viable if $c_{\min} < 6$ and $D \ge 34$, otherwise main route is strictly better).
  - Format output strictly as `[route: main]` or `[route: night]`.