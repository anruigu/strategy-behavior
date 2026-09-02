---
game: gen_frontline_depot
model: gemini-flash
condition: neutral
seed: 1
round: 1
chars: 1710
---
### Tactical Rules & Mechanics
- Each round allows up to 10 power units independently for strike and 10 power units independently for guard (strike + guard does not need to sum to 10; each individual allocation can be up to the maximum garrison allowance).
- Never hold back strike or guard under the mistaken assumption that they share a single budget of 10.
- Scoring rules:
  - Dealt Damage = `max(0, my_strike - opponent_guard)` $\rightarrow$ yields points.
  - Guard Surplus = `max(0, my_guard - opponent_strike)` $\rightarrow$ yields points.
- Because guard surplus yields points and does not cost strike power, allocating maximum guard (10) strictly dominates lower guard allocations unless there is a penalty mechanism, which there is not.

---

### Playbook

#### Guard Phase
- Whenever an `allocate_guard` phase is presented, regardless of round or prior actions, I will always output `[allocate_guard: 10]`.
- Allocating less than 10 to guard forfeits free surplus defense points against opponent strikes below 10 and increases vulnerability to damage. Never play guard below 10.

#### Strike Phase
- In Round 1:
  - Output `[allocate_strike: 10]` to immediately challenge the opponent's guard and capitalize on opponents who under-guard or split resources.
- In Subsequent Rounds (Rounds 2–4):
  - If the opponent consistently guards with 10 (neutralizing high strikes) and attacks with low/moderate power, keep `[allocate_strike: 10]` since reducing strike does not add to defense or provide alternative benefits.
  - Always commit the full garrison limit: output `[allocate_strike: 10]`.

---

### Format
- Output the required bracketed command: `[allocate_strike: 10]` or `[allocate_guard: 10]`.