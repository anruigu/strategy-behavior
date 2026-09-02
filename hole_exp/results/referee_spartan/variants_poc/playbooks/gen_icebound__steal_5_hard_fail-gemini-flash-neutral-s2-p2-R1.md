---
game: gen_icebound__steal_5_hard_fail
model: gemini-flash
condition: neutral
seed: 2
round: 1
chars: 2829
---
# Playbook: Icebound

### Core Rules & Mechanics Review
- Raids resolve clockwise: North -> East -> West -> North.
- My target when raiding: If I am North, I target East. If I am East, I target West. If I am West, I target North.
- My incoming raider: If I am North, West raids me. If I am East, North raids me. If I am West, East raids me.
- Raid outcomes:
  - Raider vs Target Scout: Raider gets +5 points; Target gets 0 points.
  - Raider vs Target Escort or Raider: Raider loses 6 points (-6); Target keeps their normal resolution (Escort scores +2).
- Fuel scoring: Unused fuel at the end converts to +1 point each.

---

### Strategy and Actions

#### Pledge Stage Decisions
- **When the game starts or players are consistently peaceful:**
  - Pledge `[pledge: scout]`. It costs only 1 fuel and provides steady point growth without burning fuel.
- **When my incoming raider has demonstrated aggressive/defecting behavior (frequent raids):**
  - If I expect to be attacked, pledge `[pledge: escort]` to protect my points and penalize their raid (-6 to them, +2 to me).
- **When my clockwise target has proven to be a reliable, undefended scouter:**
  - Pledge `[pledge: scout]` during the pledge phase to keep them docile and lower their suspicion, planning a surprise raid in the act phase, OR pledge `[pledge: raid]` if they never escort regardless.

#### Act Stage Decisions (Exploits vs Defense)
- **When all players pledge scout:**
  - Check the clockwise target's history. If they consistently act as `scout`, submit `[act: raid]` to defect and steal +5 points.
  - Check my incoming raider's history. If they consistently defect to `raid` when pledging scout:
    - If I also defect to `raid`, we both risk mutual raid penalties if my target also raids.
    - If my incoming raider frequently defects to `raid`, submit `[act: escort]` (even if I pledged scout) to block their raid and give them -6 points, or match with `[act: raid]` only if my clockwise target will remain an undefended scout.
- **When my clockwise target pledges `raid` or `escort`:**
  - Never submit `[act: raid]`. Raiding into an escort or raider incurs a catastrophic -6 penalty.
  - If I pledged `raid` and my target pledges `raid` or `escort`, immediately pivot to `[act: scout]` or `[act: escort]` to avoid the -6 penalty.
- **When my incoming raider pledges `raid`:**
  - If I pledged `scout`, pivot to `[act: escort]` in the act stage to negate the raid and penalize them -6 points instead of losing my scout points to 0.

#### What to Avoid
- Never submit `[act: raid]` against a target who is known to defect to `raid` or who pledged `escort`/`raid`. Blind mutual raiding cascades into severe negative scores (-6 per clash).
- Never blindly repeat `[act: scout]` when my incoming attacker has repeatedly shown they will defect to `raid`.