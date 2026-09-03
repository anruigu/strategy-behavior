---
game: gen_sovereign_vaults
model: gemini-flash
condition: win
seed: 2
round: 3
chars: 989
---
# Sovereign Vaults Playbook

- **Rules & Scoring Logic**: Retained gold yields 2 points per unit, while deposited gold yields only 1 point per unit. An audit failure costs 10 points and sets round score to 0. An audit succeeds as long as the deposit is a non-negative integer and does not exceed the declared harvest. Retaining 100% of the yield strictly dominates depositing.

- **Declare Phase**:
  - When dealt private yield $Y$, reply with `[declare: Y]`. Truthfully declaring the full actual yield keeps the upper limit valid, avoids audit issues, and maintains maximum deposit headroom.

- **Deposit Phase**:
  - In every round, reply with `[deposit: 0]`. Retaining all gold earns the maximum 2 points per unit on the entire yield ($0 \le \text{deposit} \le \text{declared}$ is strictly satisfied with 0).
  - Never deposit any positive amount (`[deposit: n]` where $n > 0$) because deposited gold only yields 1 point/unit and there is no shared pool bonus or public good multiplier.