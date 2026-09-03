---
game: gen_seven_seal
model: gemini-flash
condition: win
seed: 6
round: 3
chars: 965
---
# Playbook: Seven-Seal Certificates

### Core Mathematical Strategy
- The audit seal condition requires $(3A + 5B + 6C) \equiv (3a + 5b + 6c) \pmod 7$.
- Since reports are simultaneous and private draws are independent, every player coordinates on the focal invariant $R \equiv d \pmod 7$, where $d \in \{0, 1, 2\}$ is the private draw and $R \in \{0, \dots, 9\}$ is the report.
- Maintaining $R \equiv d \pmod 7$ guarantees that the audit seal passes independently of other players' exact draws.
- To maximize points on accepted rounds, choose the maximum integer $R \le 9$ such that $R \equiv d \pmod 7$, which is uniquely $R = d + 7$.

### Round-by-Round Decision Rule
- Read private draw $d \in \{0, 1, 2\}$.
- Compute report $R = d + 7$:
  - If $d = 0$: submit `[report: 7]`.
  - If $d = 1$: submit `[report: 8]`.
  - If $d = 2$: submit `[report: 9]`.
- Always output the token `[report: n]` with $n = d + 7$. Never report a value not congruent to $d \pmod 7$.