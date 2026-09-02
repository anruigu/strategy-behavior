---
game: gen_icebound
model: gemini-flash
condition: neutral
seed: 4
round: 2
chars: 2647
---
### Core Rule & Mechanism Reminders
- Pledge deductions are charged immediately at pledge time: Scout costs 1 fuel, Escort/Raid costs 2 fuel. Unused fuel converts 1:1 to points at the end.
- Fuel efficiency:
  - Scouting nets +2 points (+3 points - 1 fuel) if not raided; -1 point (0 points - 1 fuel) if raided.
  - Escorting nets +1 point (+2 points - 1 fuel cost if pledged scout) or 0 net gain (+2 points - 2 fuel cost if pledged escort), and defends completely against incoming raids.
  - Raiding nets +2 points (+3 points - 1 fuel cost if pledged scout) if the target scouts; nets -2 points (-1 point - 1 fuel cost if pledged scout) if the target escorts or raids.
- Targeting is strictly clockwise: North targets East, East targets West, West targets North.
- Actions can deviate from pledges; pledges set fuel charges, but the act determines the resolution.

---

### Playbook

#### Pledge Phase
- In all rounds (1 through 5), always reply `[pledge: scout]`.
  - Never pledge `raid` or `escort`; pledging scout guarantees paying only 1 fuel upfront while retaining full freedom to act as scout, escort, or raid at the act stage.

#### Act Phase
- When all players pledged `scout`:
  - In Rounds 1 through 4: Reply `[act: scout]`. Sticking with scout when everyone signals scout maximizes collective and individual points (+2 net points per round) with minimal friction.
  - In Round 5: Reply `[act: scout]` if opponents have shown 100% stable, unprompted cooperation across rounds 1–4, to maximize final score to +18 (15 from scouts + 3 remaining fuel). If there is any history of defections or high defection risk from upstream, reply `[act: escort]` to guarantee +17.

- When public pledges indicate non-cooperative behavior:
  - If my upstream attacker (West if I am North, North if I am East, East if I am West) pledges `raid`: Always reply `[act: escort]` to block their raid, gain +2 points, and inflict a -1 penalty on them.
  - If my upstream attacker pledges `scout` or `escort`, but my downstream target pledges `scout` and has a history of following through with scout: Consider `[act: raid]` if trailing, or stick to `[act: scout]` to secure steady gains.
  - If my downstream target pledges `escort` or `raid`: Never reply `[act: raid]`; reply `[act: scout]` (if upstream is safe) or `[act: escort]` (if upstream is threatening).

#### What Not To Do
- Never pledge `[pledge: raid]` or `[pledge: escort]`. It wastes 1 fuel needlessly and prematurely reveals strategy.
- Never choose `[act: raid]` when the downstream target is likely to escort or raid.
- Never choose `[act: scout]` when the upstream player has pledged `raid`.