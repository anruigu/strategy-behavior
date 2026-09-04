---
game: hf_harbor_customs_nerfed
model: gemini-flash
condition: neutral
seed: 0
round: 1
chars: 1231
---
# Harbor Customs Playbook

### Stage 1: Declare Stage
- When given my 3 crates $(c_1 \le c_2 \le c_3)$, I always calculate the exact total sum: $S = c_1 + c_2 + c_3$.
- I declare the exact true total: `[declare: S]`.
- I do not under-declare to match only the top crate or a subset of crates (e.g. declaring $c_3$ or $c_2 + c_3$). Under-declaring triggers an inspection penalty from other shippers docking 18 points at settlement, which completely wipes out any duty savings.

### Stage 2: Route Stage
- When deciding route after declaring true total $S$:
  - Calculate duty saved by going `night`: $\lfloor 0.30 \times S \rfloor - \lfloor 0.15 \times S \rfloor \approx 0.15 \times S$.
  - Compare duty saved against the value of the smallest crate lost ($c_1$).
  - If $c_1 < (\lfloor 0.30 \times S \rfloor - \lfloor 0.15 \times S \rfloor)$, choose `[route: night]`.
  - Otherwise, choose `[route: main]`.
- Since $c_1 \ge 5$ and $0.15 \times S \le 18$ (usually much less than $c_1$), I default to `[route: main]` in almost all circumstances to preserve all three crates.
- If an inspection finding appears before the route decision, I do not panic-switch to `night`; I stick strictly to the math comparing $c_1$ and duty savings.