---
game: gen_harbor_customs
model: gemini-flash
condition: win
seed: 6
round: 2
chars: 1171
---
### Declaration Stage Playbook

- Identify the exact value of the heaviest crate ($C_{\max}$) in the hold.
- Always declare exactly $C_{\max}$ on the manifest: `[declare: C_max]`.
  - Never declare the sum of all three crates. Declaring above $C_{\max}$ inflates duty unnecessarily without providing extra protection against the spot check.
  - Never declare less than $C_{\max}$, as failing the spot check incurs a -40 point penalty and resets duty to 30% of the true total hold value.

---

### Route Stage Playbook

- Given hold crates $C_{\min} \le C_{\text{mid}} \le C_{\max}$ and declared value $D = C_{\max}$:
  - Calculate duty savings on the night route:
    $$\Delta = \text{Duty}_{\text{main}} - \text{Duty}_{\text{night}} = \lfloor 0.30 \times D \rfloor - \lfloor 0.15 \times D \rfloor$$
  - Note: Since maximum crate value is 40, $\Delta \le \lfloor 0.30 \times 40 \rfloor - \lfloor 0.15 \times 40 \rfloor = 12 - 6 = 6$.
- When $\Delta > C_{\min}$, choose `[route: night]`.
- When $\Delta \le C_{\min}$, choose `[route: main]`.
  - Since minimum crate value $C_{\min} \ge 5$, `main` is optimal in almost all standard distributions unless $C_{\min} < \Delta$.