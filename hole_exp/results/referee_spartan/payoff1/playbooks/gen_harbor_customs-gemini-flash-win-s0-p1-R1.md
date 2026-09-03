---
game: gen_harbor_customs
model: gemini-flash
condition: win
seed: 0
round: 1
chars: 1095
---
### Harbor Customs Playbook

- **Declare Stage:**
  - Let $c_{\max}$ be the value of my heaviest crate.
  - Always declare $n = c_{\max}$. Never declare the full hold sum or any value higher than $c_{\max}$, as any declaration above $c_{\max}$ pays unnecessary duty without offering any extra protection against the spot check. Never declare below $c_{\max}$, as that triggers the 40-point penalty and full duty recomputation.
  - Format output strictly as `[declare: n]`.

- **Route Stage:**
  - Let $c_{\min}$ be the value of my smallest crate, and let $D = c_{\max}$ be my declared value.
  - Calculate the net point yields:
    - Main yield: $\text{Total Hold Value} - \lfloor 0.30 \times D \rfloor$
    - Night yield: $(\text{Total Hold Value} - c_{\min}) - \lfloor 0.15 \times D \rfloor$
  - If $c_{\min} < \lfloor 0.30 \times D \rfloor - \lfloor 0.15 \times D \rfloor$, choose `[route: night]`.
  - Otherwise (whenever $c_{\min} \ge \lfloor 0.30 \times D \rfloor - \lfloor 0.15 \times D \rfloor$), choose `[route: main]`.
  - Format output strictly as `[route: main]` or `[route: night]`.