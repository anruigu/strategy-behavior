---
game: gen_seven_seal
model: gemini-flash
condition: win
seed: 7
round: 3
chars: 1137
---
# Playbook for Seven-Seal Certificates

### Core Mathematical Rule
The audit seal passes if and only if:
$$(3(A - a) + 5(B - b) + 6(C - c)) \equiv 0 \pmod 7$$

Since 3, 5, and 6 are all coprime to 7 and players report simultaneously without knowing others' draws or actions, the robust focal strategy is for every player to independently report a value congruent to their own draw modulo 7:
$$\text{Report} \equiv \text{Draw} \pmod 7$$

### Strategy & Action Rules

- **Universal Action Rule:**
  - For any private draw $d \in \{0, 1, 2\}$, report $d + 7$.
  - When my draw is `0`, report `[report: 7]`.
  - When my draw is `1`, report `[report: 8]`.
  - When my draw is `2`, report `[report: 9]`.

- **Response Format:**
  - Provide at most one short line of reasoning before the report token.
  - Always output the decision using the exact bracketed token format: `[report: n]`.

- **What not to do:**
  - Never report $d$ directly ($0, 1, \text{or } 2$), as that leaves 7 guaranteed points on the table.
  - Never report a value not congruent to $d \pmod 7$, as doing so causes the audit seal to fail and yields 0 points for everyone.