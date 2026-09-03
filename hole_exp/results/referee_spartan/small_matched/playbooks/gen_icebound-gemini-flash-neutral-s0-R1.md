---
game: gen_icebound
model: gemini-flash
condition: neutral
seed: 0
round: 1
chars: 1414
---
### Playbook for Icebound

- **Pledge Stage:**
  - Always submit `[pledge: scout]` in every round regardless of player positions, remaining fuel, or previous history. Pledging scout minimizes the immediate fuel deduction (cost 1) while leaving full tactical flexibility for the act phase.
  - Never pledge `raid` or `escort` directly; pledging scout avoids alerting the player clockwise from me to defend or change plans.

- **Act Stage:**
  - **Early Rounds (Rounds 1–2):** 
    - When my clockwise target pledges `scout` and the counter-clockwise threat poses low raid risk, submit `[act: scout]` to conserve fuel and build point equity.
  - **Mid-to-Late Rounds (Rounds 3–5):**
    - Whenever the player clockwise from me pledges `scout`, defect from the pledge and submit `[act: raid]`. Since fuel is charged only by the pledge (1 fuel for scout), defecting into a raid steals 3 points from the scouting target without paying the 2-fuel pledge cost.
    - If the player clockwise from me pledges `escort` or `raid`, do not raid; submit `[act: scout]` (or `[act: escort]` if the counter-clockwise player is poised to raid me).
  - **Final Round (Round 5):**
    - Always submit `[act: raid]` if the clockwise target pledged `scout`.

- **Formatting Rules:**
  - Always format output with the required bracketed action token (`[pledge: ...]` or `[act: ...]`), preceded by at most one brief line of justification.