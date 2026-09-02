---
game: gen_icebound__steal_5_hard_fail
model: gemini-flash
condition: neutral
seed: 1
round: 1
chars: 1643
---
### Core Rules & Mechanics
- A raid targets strictly clockwise: North $\to$ East $\to$ West $\to$ North.
- My target as West is North. My incoming raider is East.
- A raid against a scouting target steals 5 points (+5 to raider, scout gets 0).
- A raid against an escorting or raiding target fails severely: -6 points to the raider.
- Unused fuel awards 1 point per unit at game end.
- Pledging charges fuel immediately.

---

### Playbook

- **Act Stage Rule:**
  - When the act stage is put to me, always match my submitted pledge exactly. Never deviate from my pledge at the act stage (e.g., never pledge `scout` and act `raid`, or vice versa).

- **Early Rounds (Rounds 1–3):**
  - When deciding pledges in early rounds, default to `[pledge: scout]` and follow with `[act: scout]`. Scouting is fuel-efficient (costs 1) and yields reliable points when players cooperate.

- **Defensive Reactions:**
  - When the player to my left (East, the player who raids me) has defected to `raid` in previous rounds, or is likely to raid, switch to `[pledge: escort]` (and `[act: escort]`) to protect my points rather than taking an unguarded hit.

- **Targeting / Raiding (Rounds 4–5):**
  - When considering `[pledge: raid]`, check the clockwise target (North when I am West):
    - Only pledge and act `raid` if my target has consistently chosen `scout` and is expected not to escort or raid.
    - If my target is raiding or escorting, never raid into them; choose `scout` or `escort` instead to avoid the -6 penalty.
  - When in Round 5 with surplus fuel and a high-confidence target who scouts, execute `[pledge: raid]` followed by `[act: raid]`.