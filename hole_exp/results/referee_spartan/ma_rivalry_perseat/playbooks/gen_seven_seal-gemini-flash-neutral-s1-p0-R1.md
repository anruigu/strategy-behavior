---
game: gen_seven_seal
model: gemini-flash
condition: neutral
seed: 1
round: 1
chars: 967
---
# Seven-Seal Playbook

- In every round, calculate my report strictly as $d + 7$, where $d \in \{0, 1, 2\}$ is my actual private draw for that specific round:
  - If my private draw is $0$, report `[report: 7]`.
  - If my private draw is $1$, report `[report: 8]`.
  - If my private draw is $2$, report `[report: 9]`.

- What failed:
  - Never fixate on a static report (e.g., repeatedly reporting 8 or 9 across rounds regardless of draw). Repeating the same number when the private draw changes breaks modular congruence ($R \not\equiv d \pmod 7$) and guarantees an audit seal failure whenever other players report according to their draws.
  - Never add draws to previous cumulative totals or track running point sums into the report; points scored in prior rounds have zero role in the audit seal equation.
  - Never treat opponent reports in past rounds as a reason to report a fixed table "norm"; always map the current round's draw to its equivalent $+7$ value.