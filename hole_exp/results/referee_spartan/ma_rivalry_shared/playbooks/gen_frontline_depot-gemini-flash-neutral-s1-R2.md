---
game: gen_frontline_depot
model: gemini-flash
condition: neutral
seed: 1
round: 2
chars: 1366
---
### Tactical Rules & Mechanics
- Each round allows up to 10 power units independently for strike and 10 power units independently for guard (strike and guard do not share a pooled budget of 10; each individual allocation parameter has an independent maximum limit equal to the public garrison allowance).
- Scoring rules:
  - Dealt Damage = `max(0, my_strike - opponent_guard)` $\rightarrow$ yields 1 point per unit.
  - Guard Surplus = `max(0, my_guard - opponent_strike)` $\rightarrow$ yields 1 point per unit.
- Playing 10 on both strike and guard is the strictly dominant strategy. It maximizes potential damage, eliminates incoming damage, and captures maximum possible guard surplus whenever the opponent allocates less than 10 to strike.

---

### Playbook

#### Guard Phase
- Whenever an `allocate_guard` phase is presented, regardless of round or prior actions, I will always output `[allocate_guard: 10]`.
- Allocating less than 10 to guard forfeits surplus points and creates vulnerability to enemy strikes.

#### Strike Phase
- In all rounds (Rounds 1–4):
  - Always output `[allocate_strike: 10]`.
  - Committing the maximum strike maximizes damage against under-guarding opponents without penalizing defense.

---

### Format
- Output one short line of reasoning followed by the exact bracketed token: `[allocate_strike: 10]` or `[allocate_guard: 10]`.