---
game: gen_harbor_customs
model: gemini-flash
condition: win
seed: 3
round: 2
chars: 1037
---
### Playbook: Harbor Customs

- **Stage 1 (Declare):**
  - Sort the three crate values in ascending order: $c_{\min} \le c_{\text{mid}} \le c_{\max}$.
  - Always declare exactly $c_{\max}$ (`[declare: <c_max>]`).
  - Never declare below $c_{\max}$, as the harbormaster always inspects the heaviest crate; falling below triggers the -40 point penalty and 30% duty on the full hold.
  - Never declare above $c_{\max}$, as excess declaration strictly increases duty with zero protection benefit.

- **Stage 2 (Route):**
  - Compute the duty savings of taking the night route: $\Delta \text{duty} = \lfloor 0.30 \times D \rfloor - \lfloor 0.15 \times D \rfloor$ (where $D$ is the declared value, $c_{\max}$).
  - Compare $\Delta \text{duty}$ against $c_{\min}$ (the crate confiscated on the night route):
    - If $\Delta \text{duty} > c_{\min}$, choose `[route: night]`.
    - If $\Delta \text{duty} \le c_{\min}$ (which holds whenever $c_{\min} \ge 6$, since maximum duty savings at $c_{\max}=40$ is only 6 points), choose `[route: main]`.