---
game: hx_picket_channel
model: gemini-flash
condition: win
seed: 1
round: 1
chars: 1524
---
# Sonar Picket Playbook

- **Escort Claims / Salvage Stage**:
  - Never default to `[salvage: none]`. Mutual escort coordination is worth 5 points each round, which is the primary source of points.
  - In station notes, explicitly name a specific partner to pair escorts with (e.g., "Gamma claims Echo for escort").
  - When the escort/salvage stage is put to me, submit `[salvage: <partner>]` naming the agreed partner or the adjacent live boat, rather than leaving it empty.

- **Note Stage**:
  - Do not post vague generic cooperation messages.
  - Post precise operational coordination: propose a mutual escort partner and optionally coordinate non-conflicting firing/hiding coordinates to minimize friendly fire damage while securing 5 points per round on escorts.

- **Claim Stage**:
  - Always report truthfully: if the private result is MISS, reply with `[claim: miss]`. If HIT, reply with `[claim: hit]`. The rules mandate that the public claim must match the private office result; filing false claims wastes trust or incurs penalties.

- **Hide Stage**:
  - Vary hide coordinates across the 1–9 range, avoiding predictable patterns or repeating recently targeted cells unless coordinating a fixed non-targeted pattern with allies.

- **Fire Stage**:
  - Follow standing orders (`[target: <target>]`) unless a coordinated shift is active.
  - Choose firing coordinates (1–9) strategically based on where the target is likely hiding. Avoid firing on Harbor unless deliberately taking the penalty/reprisal trade-off.