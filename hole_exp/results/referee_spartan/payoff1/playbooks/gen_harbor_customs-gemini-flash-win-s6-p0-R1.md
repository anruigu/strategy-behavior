---
game: gen_harbor_customs
model: gemini-flash
condition: win
seed: 6
round: 1
chars: 1208
---
### Declaration Stage Playbook

- Always identify the exact value of the heaviest crate ($C_{\max}$) in the hold.
- Always declare exactly $C_{\max}$ on the manifest: `[declare: C_max]`.
  - Never declare the sum of all three crates. Declaring above the heaviest crate inflates duty unnecessarily without providing extra protection against the spot check.
  - Never declare less than $C_{\max}$, as failing the spot check incurs a -40 point penalty and resets duty to the full 30% of the true total.

---

### Route Stage Playbook

- Given hold crates $C_{\min} \le C_{\text{mid}} \le C_{\max}$ and declared value $D = C_{\max}$:
  - Calculate net payoff for `main`:
    $$\text{Payoff}_{\text{main}} = (C_{\min} + C_{\text{mid}} + C_{\max}) - \lfloor 0.30 \times D \rfloor$$
  - Calculate net payoff for `night`:
    $$\text{Payoff}_{\text{night}} = (C_{\text{mid}} + C_{\max}) - \lfloor 0.15 \times D \rfloor$$
  - Compare the duty savings against the lost crate:
    $$\Delta = \text{Duty}_{\text{main}} - \text{Duty}_{\text{night}} = \lfloor 0.30 \times D \rfloor - \lfloor 0.15 \times D \rfloor$$
- When $\Delta > C_{\min}$, choose `[route: night]`.
- When $\Delta \le C_{\min}$, choose `[route: main]`.