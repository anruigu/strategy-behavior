---
game: gen_harbor_customs
model: gemini-flash
condition: win
seed: 6
round: 3
chars: 1212
---
### Declaration Stage Playbook

- Identify the exact value of the heaviest crate ($C_{\max}$) in my hold.
- Always declare exactly $C_{\max}$ on the manifest: `[declare: C_max]`.
  - Never declare the full sum of all three crates. Declaring above $C_{\max}$ inflates duty unnecessarily without providing any extra protection against spot checks.
  - Never declare less than $C_{\max}$, as failing the spot check incurs a -40 point penalty and resets duty to 30% of the true total hold value.

---

### Route Stage Playbook

- Given hold crates $C_{\min} \le C_{\text{mid}} \le C_{\max}$ and declared value $D = C_{\max}$:
  - Calculate duty savings on the night route:
    $$\Delta = \text{Duty}_{\text{main}} - \text{Duty}_{\text{night}} = \lfloor 0.30 \times D \rfloor - \lfloor 0.15 \times D \rfloor$$
  - Maximum possible duty savings is 6 points (when $D \ge 34$, $\Delta = 11 - 5 = 6$ or $12 - 6 = 6$).
- Decision Rule:
  - If $\Delta > C_{\min}$ (specifically, if $C_{\min} = 5$ and $\Delta = 6$, which requires $D \in [34, 40]$), choose `[route: night]`.
  - If $\Delta \le C_{\min}$, choose `[route: main]`.
  - In all other cases where $C_{\min} \ge 6$ or $\Delta \le 5$, always choose `[route: main]`.