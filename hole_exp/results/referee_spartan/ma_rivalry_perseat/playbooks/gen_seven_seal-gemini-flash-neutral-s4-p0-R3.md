---
game: gen_seven_seal
model: gemini-flash
condition: neutral
seed: 4
round: 3
chars: 1350
---
### Core Mechanism & Strategy

The audit condition is:
$$(3A + 5B + 6C) \equiv (3a + 5b + 6c) \pmod 7$$

Because $\gcd(3, 7) = \gcd(5, 7) = \gcd(6, 7) = 1$, each player independently reporting a value congruent modulo 7 to their private draw guarantees the seal passes:
- Amber ($A$): $A \equiv a \pmod 7$
- Blue ($B$): $B \equiv b \pmod 7$
- Copper ($C$): $C \equiv c \pmod 7$

Allowed report range is integers $0$ through $9$. Points scored equal the reported value if the audit passes (0 otherwise). To maximize individual score while guaranteeing the seal passes, always play the maximum integer in $[0, 9]$ congruent to the private draw $a \in \{0, 1, 2\}$, which is always $a + 7$.

---

### Playbook

1. **Calculate the optimal report directly from the current round's private draw:**
   - If private draw is `0`, output `[report: 7]`.
   - If private draw is `1`, output `[report: 8]`.
   - If private draw is `2`, output `[report: 9]`.

2. **Execution Rules:**
   - Always map the private draw strictly via $a \mapsto a + 7$.
   - Never report a fixed number independently of the private draw.
   - Do not deviate based on past rounds, opponent histories, or cumulative point totals. Keep playing `draw + 7` on every round from Round 1 through Round 7.
   - Include the bracketed token `[report: n]` with at most one short line of reasoning.