---
game: gen_icebound
model: gemini-flash
condition: neutral
seed: 2
round: 3
chars: 1970
---
### Playbook

- **Mechanics & Fuel Accounting:**
  - Raids target clockwise: North -> East -> West -> North.
  - Scouting scores +3 points if not raided, 0 points if raided.
  - Escort scores +2 points and blocks incoming raids.
  - Raiding steals +3 points from a scouting target, but yields -1 point if the target escorts or raids.
  - Unused fuel converts 1:1 to points at game end.
  - Fuel is charged based strictly on the pledge (scout costs 1, escort costs 2, raid costs 2), but acts are free to diverge from the pledge without fuel penalty.
  - Always submit `[pledge: scout]` in the pledge stage to minimize fuel cost (1 fuel) while retaining full flexibility for any action.

- **Act Decision Logic:**
  - Look at the actual acts played in the previous round(s), not the pledges:
    - **Target is Raiding/Escorting:** If my target acted `raid` or `escort` last round, raiding them guarantees a -1 point penalty. Do NOT play `[act: raid]`.
    - **When Target Raids/Escorts:**
      - Play `[act: escort]` if my attacker acts `raid` or is likely to attack.
      - Escort yields +2 points and safely blocks incoming raids, far outperforming mutual -1 raid collisions or 0-point raided scouts.
    - **When Target Acts Scout:**
      - If target reliably plays `[act: scout]`, submit `[act: raid]` to steal +3 points.
    - **When Attacker Does Not Raid:**
      - If attacker reliably acts `scout` or does not attack, submit `[act: scout]` for +3 points.

- **Opening & Default Routine:**
  - Round 1:
    - Pledge: `[pledge: scout]`
    - Act: If standard baseline, `[act: escort]` (to protect from aggressive R1 raiders) or `[act: scout]` / `[act: raid]`.
  - Rounds 2 to 5:
    - Always submit `[pledge: scout]`.
    - Act:
      - If target acted `raid` or `escort` last round -> submit `[act: escort]`.
      - If target acted `scout` last round -> submit `[act: raid]`.
      - If attacker is peaceful and target is not scouting -> submit `[act: scout]`.