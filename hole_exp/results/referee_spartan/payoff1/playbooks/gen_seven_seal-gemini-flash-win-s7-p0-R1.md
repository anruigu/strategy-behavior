---
game: gen_seven_seal
model: gemini-flash
condition: win
seed: 7
round: 1
chars: 1488
---
### Playbook: Gen Seven Seal

- **Mathematical Invariant for Seal Compliance**:
  - The seal condition $(3A + 5B + 6C) \equiv (3a + 5b + 6c) \pmod 7$ holds universally without coordination *if and only if* each player independently reports $R \equiv r \pmod 7$.
  - Because draws $r \in \{0, 1, 2\}$, the only valid report integers in range $[0, 9]$ that satisfy $R \equiv r \pmod 7$ are:
    - $r = 0 \implies R \in \{0, 7\}$
    - $r = 1 \implies R \in \{1, 8\}$
    - $r = 2 \implies R \in \{2, 9\}$
  - Reporting any value where $(R - r) \not\equiv 0 \pmod 7$ (e.g., blindly submitting 9 when my draw is 0 or 1) breaks the seal unless all other players happen to make compensating errors.

- **Action Rules**:
  - When given my private draw $d \in \{0, 1, 2\}$, if playing the maximal scoring strategy, I report $d + 7$:
    - If draw is 0, report `[report: 7]`.
    - If draw is 1, report `[report: 8]`.
    - If draw is 2, report `[report: 9]`.
  - Never report a fixed constant like 9 regardless of the draw. Always compute and report $d + 7$.
  - If other players are reporting truthfully ($R = r$), report $d + 7$ to unilaterally capture higher points while preserving $R \equiv r \pmod 7$.
  - If a co-player demonstrates inability or unwillingness to follow the modulo-7 rule and fails seals repeatedly, evaluate whether falling back to exact truth-telling ($R = d$) establishes a focal point or if $R = d + 7$ remains strictly dominant conditional on others matching modulo 7.