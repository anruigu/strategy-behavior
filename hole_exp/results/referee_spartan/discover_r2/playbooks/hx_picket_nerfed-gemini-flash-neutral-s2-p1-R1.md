---
game: hx_picket_nerfed
model: gemini-flash
condition: neutral
seed: 2
round: 1
chars: 1235
---
### Playbook for Sonar Picket

- **Hiding**:
  - When prompted for `[hide: n]`, choose unpredictably across the 1–9 line, avoiding the cell fired upon by the upstream station in the previous round.

- **Station Notes**:
  - When prompted for `[note: <text>]`, propose mutual escort coordination clearly (e.g., `[note: Escorting Echo every round for mutual +5]`) or signal standard station readiness.

- **Firing**:
  - When prompted for `[target: <boat>] [fire: n]`, obey the standing order target round the picket (Echo $\to$ Foxtrot $\to$ Gamma $\to$ Echo) and select an unrepeated cell from 1 to 9.
  - Do not fire at Harbor unless prepared to face retaliatory elimination.

- **Claims**:
  - When prompted for `[claim: hit]` or `[claim: miss]`, **always report the true private office result**. Never file a false `[claim: hit]` on a miss; false claims are invalidated and do not award points.

- **Escort Claims (Salvage)**:
  - When prompted for `[salvage: <boat>]`, pick a consistent partner (e.g., the downstream or upstream boat, or whoever agreed via notes) and submit `[salvage: <boat>]` instead of `[salvage: none]`. Mutual escort claims award +5 points each round, which dominates shooting points; never default to `none`.