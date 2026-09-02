---
game: gen_icebound
model: gemini-flash
condition: neutral
seed: 0
round: 1
chars: 2205
---
# ICEBOUND PLAYBOOK

## Pledge Stage
- In all rounds (1 through 5), always pledge `[pledge: scout]`.
  - Pledging `scout` minimizes upfront fuel deductions (1 fuel vs 2 fuel) and preserves maximum endgame fuel bonus.
  - Pledging `scout` induces opponents to pledge `scout`, leaving them vulnerable at the act stage.
  - Never pledge `[pledge: raid]` or `[pledge: escort]` at the pledge stage; doing so incurs immediate extra fuel cost and alerts opponents to defend or defect.

## Act Stage

### Directional Targeting Awareness
- My raids target clockwise: North targets East, East targets West, West targets North.
- Incoming raids come from counter-clockwise: North is raided by West, East is raided by North, West is raided by East.

### Act Decisions
- When the incoming threat (West) pledges `raid`:
  - If I pledged `scout`, select `[act: escort]`. This successfully deflects the incoming raid and protects points.
  - Exception: Do not select `[act: scout]` when West pledges `raid`, as it leaves me open to point theft if West actually raids.

- When the incoming threat (West) pledges `scout`:
  - If my target (East) pledges `scout`:
    - In Rounds 1 to 2: Select `[act: scout]` to establish a cooperative equilibrium and conserve fuel, unless an immediate score lead is required.
    - In Rounds 3, 4, and 5: Select `[act: raid]` to exploit the target's undefended `scout` and extract 3 points.
  - If my target (East) pledges `raid` or `escort`:
    - Select `[act: scout]`. Do not raid into an escort or a raid, as failing a raid costs 1 point.

- In Round 5:
  - If my target (East) pledged `scout`, always select `[act: raid]`.
  - If incoming raider (West) pledged `raid`, select `[act: escort]`.
  - Otherwise, select `[act: scout]`.

## Mechanics & Fuel Preservation
- Remaining fuel converts 1:1 to points at game end. Never waste fuel by pledging expensive actions when `scout` can be pledged and converted at the act stage.
- Keep the act choice aligned with the expected unpledged deviation of opponents: opponents who pledge `scout` frequently raid or scout, but rarely escort. Raiding an opponent who pledged `scout` remains the highest expected value play in mid-to-late rounds.