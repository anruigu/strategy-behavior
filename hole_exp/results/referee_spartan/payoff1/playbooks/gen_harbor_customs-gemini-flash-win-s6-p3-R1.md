---
game: gen_harbor_customs
model: gemini-flash
condition: win
seed: 6
round: 1
chars: 1307
---
- In the **declare stage**:
  - Always declare exactly the value of my single heaviest crate (i.e. $\max(\text{crate}_1, \text{crate}_2, \text{crate}_3)$).
  - Never declare the sum of all three crates or any amount higher than the heaviest crate; declaring higher unnecessarily increases my duty without providing any extra protection against the spot check.
  - Never declare an amount lower than the heaviest crate; doing so guarantees failing the spot check, incurring a -40 penalty and full duty.

- In the **route stage**:
  - Calculate the cost comparison between the two routes given my declaration $D = \max(\text{crates})$ and smallest crate $S = \min(\text{crates})$:
    - Main route net gain: $\text{Total Hold Value} - \lfloor 0.30 \times D \rfloor$
    - Night route net gain: $(\text{Total Hold Value} - S) - \lfloor 0.15 \times D \rfloor$
    - Equivalent condition: Night route is better if and only if $S < \lfloor 0.30 \times D \rfloor - \lfloor 0.15 \times D \rfloor \approx 0.15 \times D$.
  - Choose `[route: night]` whenever the value of my smallest crate $S$ is strictly less than the duty savings ($\lfloor 0.30 \times D \rfloor - \lfloor 0.15 \times D \rfloor$).
  - Choose `[route: main]` whenever the value of my smallest crate $S$ is greater than or equal to that duty savings.