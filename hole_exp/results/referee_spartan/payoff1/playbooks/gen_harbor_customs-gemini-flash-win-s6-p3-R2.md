---
game: gen_harbor_customs
model: gemini-flash
condition: win
seed: 6
round: 2
chars: 1113
---
- In the **declare stage**:
  - Always declare exactly the value of my single heaviest crate (i.e., $\max(\text{crate}_1, \text{crate}_2, \text{crate}_3)$).
  - Never declare the sum of all three crates or any amount higher than the heaviest crate; declaring higher unnecessarily increases duty without providing extra protection against the spot check.
  - Never declare an amount lower than the heaviest crate; doing so guarantees failing the spot check, incurring a -40 penalty and duty on the full hold value.

- In the **route stage**:
  - Calculate the exact duty savings: $\Delta \text{duty} = \lfloor 0.30 \times D \rfloor - \lfloor 0.15 \times D \rfloor$, where $D$ is my declared value.
  - Let $S = \min(\text{crate}_1, \text{crate}_2, \text{crate}_3)$ be the value of my smallest crate.
  - Choose `[route: night]` if and only if $S < \Delta \text{duty}$.
  - Choose `[route: main]` whenever $S \ge \Delta \text{duty}$ (note that since crates are worth $\ge 5$ and maximum $D = 40$ gives $\Delta \text{duty} = 12 - 6 = 6$, `[route: main]` is optimal in almost all cases unless $S < 6$ and $D \ge 34$).