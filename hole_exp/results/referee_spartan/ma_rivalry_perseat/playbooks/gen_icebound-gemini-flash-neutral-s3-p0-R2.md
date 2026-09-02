---
game: gen_icebound
model: gemini-flash
condition: neutral
seed: 3
round: 2
chars: 2223
---
### Game Mechanics & Rule Clarifications

- **Rules & Mechanics**:
  - Fuel cost is deducted based on the **pledge** (scout = 1, escort = 2, raid = 2).
  - Any valid act word (`scout`, `escort`, `raid`) can be submitted regardless of pledge; the referee resolves scoring from the submitted acts, while fuel was charged from pledges.
  - Scouting earns +3 points unless raided (then 0). Escort earns +2 points and protects against incoming raids.
  - Raid steals 3 points from a scouting target (target gets 0, raider gets +3). Raid against an escort or raider loses 1 point (-1).
  - Raids rotate clockwise: North $\rightarrow$ East $\rightarrow$ West $\rightarrow$ North.
  - Opponents learn and adapt: East learned to raid North in later rounds after repeated North raids.

---

### Pledge Stage

- Always submit `[pledge: scout]`.
  - Scouting costs only 1 fuel (saving fuel for the 1:1 end-game conversion).
  - It leaves all act options viable at the act stage.

---

### Act Stage

- Identify:
  - **Clockwise Target**: The player I attack (North $\rightarrow$ East, East $\rightarrow$ West, West $\rightarrow$ North).
  - **Counter-Clockwise Attacker**: The player attacking me (West $\rightarrow$ North, North $\rightarrow$ East, East $\rightarrow$ West).
  - **Opponent History**: Track whether the clockwise target has adapted to defend/counter-raid after earlier rounds.

- **Decision Logic**:
  - **Rounds 1–2**:
    - If clockwise target pledged `scout` and counter-clockwise attacker pledged `scout`: submit `[act: raid]`.
  - **Rounds 3–5 (Adaptation Phase)**:
    - If clockwise target has begun counter-raiding or acting `raid`/`escort` in previous rounds:
      - Do **not** raid them, as attacking a raider or escort costs -1 point.
      - If counter-clockwise attacker is not raiding me: submit `[act: scout]` for +3 points.
      - If counter-clockwise attacker is likely raiding me: submit `[act: escort]` to protect points and inflict a -1 penalty on them.
    - If counter-clockwise attacker pledged `raid` or has a history of raiding:
      - Submit `[act: escort]`.
    - If clockwise target is consistently passive (pledges/acts `scout`) and attacker does not raid:
      - Submit `[act: raid]`.