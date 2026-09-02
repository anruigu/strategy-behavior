---
game: gen_icebound__steal_5
model: gemini-flash
condition: neutral
seed: 0
round: 2
chars: 1416
---
- Always pledge `scout` during the pledge stage to minimize fuel cost (1 fuel deducted instead of 2), conserve fuel for the 1:1 end-game point conversion, and avoid alerting targets to defend.
- Never pledge `raid` or `escort` during the pledge stage, as fuel is irrevocably deducted based on the pledge.
- Clockwise targeting reference: North targets East, East targets West, West targets North.
- At the act stage:
  - If my clockwise target pledged `scout` in earlier rounds (Rounds 1–2), submit `[act: raid]` because opponents reliably follow through on their scout pledges early, scoring +5.
  - In later rounds (Rounds 3–5), be aware that opponents also learn to defect from `scout` to `raid`. If my clockwise target has defected to `raid` or pledged `escort`, my raid will hit a non-scout and incur a -1 penalty.
  - If my clockwise target is likely to act `scout`, submit `[act: raid]`.
  - If my clockwise target is expected to act `raid` or `escort`, and my incoming attacker (counter-clockwise) is expected to raid me:
    - If I want to avoid the -1 failed raid penalty, submit `[act: escort]` or `[act: scout]` depending on whether incoming theft needs nullifying.
    - Note that `[act: escort]` prevents incoming theft and scores +2 points.
- Always respond strictly with the requested bracketed token format (`[pledge: ...]`, `[act: ...]`), optionally preceded by at most one short line of reasoning.