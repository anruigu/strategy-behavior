---
game: gen_harbor_customs
model: gemini-flash
condition: win
seed: 6
round: 3
chars: 1128
---
- In the **declare stage**:
  - Always declare exactly the value of my single heaviest crate: $D = \max(\text{crate}_1, \text{crate}_2, \text{crate}_3)$.
  - Never declare the sum of all three crates or any amount higher than the heaviest crate; declaring higher unnecessarily increases duty without providing extra protection against the spot check.
  - Never declare an amount lower than the heaviest crate; doing so guarantees failing the spot check, incurring a -40 penalty and duty recomputed on the full hold value.

- In the **route stage**:
  - Calculate the exact duty savings: $\Delta \text{duty} = \lfloor 0.30 \times D \rfloor - \lfloor 0.15 \times D \rfloor$, where $D$ is my declared value.
  - Let $S = \min(\text{crate}_1, \text{crate}_2, \text{crate}_3)$ be the value of my smallest crate.
  - Choose `[route: night]` if and only if $S < \Delta \text{duty}$.
  - Choose `[route: main]` whenever $S \ge \Delta \text{duty}$ (since crates are worth $\ge 5$ and maximum $D = 40$ gives $\Delta \text{duty} = 12 - 6 = 6$, `[route: main]` is optimal in virtually all cases, specifically unless $S = 5$ and $D \ge 34$).