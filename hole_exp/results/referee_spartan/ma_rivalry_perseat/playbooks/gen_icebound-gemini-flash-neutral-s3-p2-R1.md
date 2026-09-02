---
game: gen_icebound
model: gemini-flash
condition: neutral
seed: 3
round: 1
chars: 2387
---
### Rules and Mechanics Checklist
- Target orientation is clockwise: North targets East, East targets West, West targets North.
- Fuel cost is deducted immediately at pledge: `scout` = 1, `escort` = 2, `raid` = 2.
- Remaining fuel converts to points 1:1 at game end.
- Pledging is cheap signaling; acts determine payoff. Changing act from pledge is legal.
- Target acts and payouts:
  - Scouting target: +3 to raider, 0 to scout.
  - Escorting target: -1 to raider, +2 to escort.
  - Raiding target: -1 to raider, raider resolves own attack independently.
  - Safe scout: +3 to scout (net +2 vs unused fuel).

---

### Playbook

#### Pledge Stage
- Always pledge `[pledge: scout]` in all rounds.
  - It only burns 1 fuel upfront, preserving maximum fuel and point conversion.
  - It signals cooperation and encourages opponents to pledge and act `scout`.
  - Never pledge `[pledge: raid]` or `[pledge: escort]`. It wastes 2 fuel upfront and alarms targets into defending.

#### Act Stage
- Identify my clockwise target (North if I am West, East if I am North, West if I am East) and my incoming threat (counter-clockwise neighbor).
- If my incoming threat has consistently raided or defected, and I cannot safely scout:
  - If I pledged `scout`, select `[act: scout]` only if incoming raid probability is low; if incoming raid is virtually certain, accept that `scout` will be stolen or choose `[act: raid]` against my target to offset the loss.
- When everyone pledges `scout`:
  - In early rounds (Rounds 1–3): Choose `[act: scout]` to sustain mutual trust, maximize fuel-to-point yield (+3 points for 1 fuel), and avoid triggering a cycle of mutual raiding where everyone loses points.
  - When opponents have begun opportunistic raiding, or in Round 5:
    - If my clockwise target has a history of defecting to `raid` or defending with `escort`, select `[act: scout]`—do not attack a target that won't be scouting.
    - If my clockwise target reliably follows through on `scout`, select `[act: raid]` to steal 3 points.
- Never choose `[act: escort]` after pledging `scout` or `raid` unless specifically intending to burn fuel defensively; since fuel was already deducted at pledge, changing to `escort` does not grant extra fuel efficiency.
- Never pledge `raid` and then switch to `[act: scout]`; that wastes 2 fuel on the pledge while receiving the vulnerable return of a scout.