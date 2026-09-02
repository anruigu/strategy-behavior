---
game: gen_icebound
model: gemini-flash
condition: neutral
seed: 3
round: 1
chars: 1537
---
### Pledge Stage

- Always submit `[pledge: scout]` in every round. 
  - Scouting minimizes fuel burn (1 fuel cost vs 2) and keeps all tactical options open at the act stage, since fuel is charged directly from the pledge.

---

### Act Stage

- Look at the public pledges and target directions (clockwise: North $\rightarrow$ East $\rightarrow$ West $\rightarrow$ North).
- When the player to my clockwise target pledged `scout` and the player counter-clockwise to me (who attacks me) did not pledge `raid`:
  - Submit `[act: raid]` to steal points uncontested from the scouting target.
- When the player counter-clockwise to me pledged `raid`:
  - If my clockwise target pledged `scout` and I cannot escort, or if I want guaranteed protection, submit `[act: escort]` to block the incoming raid and penalize the raider.
  - Do not submit `[act: scout]` when the player targeting me pledged `raid`, as getting raided nets 0 points and wastes fuel.
- When my clockwise target pledged `raid` or `escort`:
  - Do not submit `[act: raid]`, because raiding an escort or a fellow raider loses 1 point.
  - If no one is raiding me, submit `[act: scout]` to take the safe 3 points.
- In round 5 (final round):
  - If my clockwise target pledged `scout` and the counter-clockwise player did not pledge `raid`, submit `[act: raid]`.
  - If the counter-clockwise player pledged `raid`, submit `[act: escort]` to protect existing points.
  - Otherwise, submit `[act: scout]` to bank points and save fuel for end-game fuel scoring (1 fuel = 1 point).