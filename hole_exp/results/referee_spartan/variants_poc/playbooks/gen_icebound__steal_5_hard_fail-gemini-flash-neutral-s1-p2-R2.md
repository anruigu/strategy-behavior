---
game: gen_icebound__steal_5_hard_fail
model: gemini-flash
condition: neutral
seed: 1
round: 2
chars: 2133
---
### Core Rules & Mechanics
- A raid targets strictly clockwise: North $\to$ East $\to$ West $\to$ North.
- My target as West is North. My incoming raider is East.
- Costs & Payouts:
  - `scout`: Costs 1 fuel. Yields 3 points (0 if raided). Net value = 3 points - 1 fuel value = +2 vs remaining fuel.
  - `escort`: Costs 2 fuel. Yields 2 points and blocks raids. Net value = 2 points - 2 fuel value = 0 vs remaining fuel.
  - `raid`: Costs 2 fuel. Steals 5 points against a scout (+5), but loses 6 points against escort/raid (-6). Net value = +3 vs remaining fuel on success, -8 on failure.
- Unused fuel awards 1 point per unit at game end.
- Act must strictly match the submitted pledge.

---

### Playbook

- **Act Stage Rule:**
  - Always match my submitted pledge exactly (`[act: scout]`, `[act: escort]`, or `[act: raid]`).

- **Early Rounds (Rounds 1–3):**
  - Default to `[pledge: scout]` and `[act: scout]`. Build points efficiently with low fuel cost while mutual cooperation holds.

- **Defection / Raiding (Round 4):**
  - When my clockwise target (North) has scouted predictably every round, defect with `[pledge: raid]` and `[act: raid]` in Round 4 to harvest +5 points.

- **Endgame Decisions (Round 5):**
  - After raiding in Round 4, my target (North) is likely to escort/defend in Round 5, making a second raid high risk (-6 penalty). Never raid into a target who was just raided.
  - Evaluate Round 5 choices based on incoming threat from my raider (East):
    - If East has scouted/escorted and shows no aggression towards me, play `[pledge: scout]` (net +2 vs saving fuel; scores 19 total if unraided).
    - If East has raided or is expected to raid, play `[pledge: escort]` to protect against theft (net 0 vs saving fuel; scores 17 total).
    - If choosing to conserve fuel instead of escorting, remaining fuel gives +1/unit; escorting scores 2 points for 2 fuel (identical net score to doing nothing if unraided, but prevents theft).

- **Defensive Reactions:**
  - If the player targeting me (East) raids in any prior round, switch to `[pledge: escort]` / `[act: escort]` in subsequent rounds to block theft.