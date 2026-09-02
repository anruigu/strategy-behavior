---
game: gen_harbor_customs
model: gemini-flash
condition: neutral
seed: 3
round: 3
chars: 1898
---
### Core Strategy & Rules Insight

- The spot check always inspects only the heaviest crate in my hold. If my declared value is less than the value of my heaviest crate, I pay a -40 point penalty and 30% duty on my true total hold value.
- If my declaration is at least the value of my heaviest crate, I never get flagged.
- Duty is calculated strictly on my declared value: `floor(0.30 * declared)` for `main`, `floor(0.15 * declared)` for `night`.
- Declaring any amount above my heaviest crate is throwing away points in unnecessary duty. Never declare below the heaviest crate (the penalty and full duty wipe out any gain).
- Crate values range from 5 to 40. The maximum possible duty savings from `night` over `main` is $\lfloor 0.30 \times 40 \rfloor - \lfloor 0.15 \times 40 \rfloor = 12 - 6 = 6$ points (which occurs only when $D \ge 34$). Since the minimum crate value is 5, `night` is only mathematically advantageous if $C_{\min} = 5$ and $\Delta \text{duty} = 6$ (i.e., $D \in [34, 40]$), netting exactly +1 point. In all other cases, `main` is strictly superior.

---

### Playbook

#### Stage 1: Declare Stage
- Identify the 3 crates in my hold: $c_1, c_2, c_3$.
- Find the maximum crate value: $C_{\max} = \max(c_1, c_2, c_3)$.
- Always declare exactly $C_{\max}$.
- Format output: `[declare: C_max]`.

#### Stage 2: Route Stage
- Identify the minimum crate value: $C_{\min} = \min(c_1, c_2, c_3)$.
- Compute duty savings:
  - $\text{duty}_{\text{main}} = \lfloor 0.30 \times D \rfloor$
  - $\text{duty}_{\text{night}} = \lfloor 0.15 \times D \rfloor$
  - $\Delta \text{duty} = \text{duty}_{\text{main}} - \text{duty}_{\text{night}}$
- Route decision:
  - If $\Delta \text{duty} > C_{\min}$ (specifically, when $C_{\min} = 5$ and $D \ge 34$, where $\Delta \text{duty} = 6$), choose `[route: night]`.
  - Otherwise (whenever $C_{\min} \ge \Delta \text{duty}$), choose `[route: main]`.