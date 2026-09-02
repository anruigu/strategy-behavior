---
game: gen_icebound__shipped
model: gemini-flash
condition: neutral
seed: 3
round: 2
chars: 3104
---
### Core Rules & Economics

- **Clockwise targeting:** North targets East, East targets West, West targets North.
- **Costs & Rewards:**
  - `scout`: Costs 1 fuel (charged at pledge). Yields +3 points if untargeted by raid; 0 points if successfully raided.
  - `escort`: Costs 2 fuel (charged at pledge). Yields +2 points and blocks incoming raids.
  - `raid`: Costs 2 fuel if pledged, but costs 1 fuel if pledged `scout` and switched at act stage. Steals 3 points if target acts `scout`. Loses 1 point (-1) if target acts `escort` or `raid`.
  - Unused fuel at game end yields +1 point each.
- **Action Decoupling:** Fuel is deducted strictly from the pledge. Pledging `scout` and acting `raid` or `escort` only costs 1 fuel, allowing cheap raids or defenses.

---

### Pledge Phase

- **Universal Rule:** Always pledge `[pledge: scout]`.
  - Minimizes upfront fuel cost to 1.
  - Preserves end-game fuel bonus (+1 pt/fuel).
  - Keeps act options open while disguising actual intent.

---

### Act Phase Targeting & Threat Assessment

- **Incoming Threat (attacker targeting me):**
  - If West, East targets me.
  - If North, West targets me.
  - If East, North targets me.
- **My Target (player I target):**
  - If West, I target North.
  - If North, I target East.
  - If East, I target West.

---

### Act Phase Decision Matrix

1. **Check Target's History & Likely Act:**
   - **Target is a Raider/Escorter:** If my target frequently acts `raid` (e.g. North pledging scout but acting raid) or `escort`, **NEVER** act `[act: raid]` against them. Raiding into an active raid or escort loses 1 point (-1).
   - **Target is a Scout:** If my target consistently acts `scout`, acting `[act: raid]` steals +3 points.

2. **Check Incoming Attacker's Threat:**
   - **Attacker is Safe:** If my attacker consistently acts `escort` or `scout` (does not raid me), I am safe to act `[act: scout]` for guaranteed +3 points.
   - **Attacker is Raiding me:** If my attacker is likely to act `raid`, acting `[act: escort]` guarantees +2 points and blocks theft, or `[act: scout]` yields 0.

3. **Standard Strategy by Match Pattern:**
   - **North raids East, East escorts, West targets North:**
     - North acts `raid`. Raiding North results in -1 penalty.
     - East acts `escort`. East does not raid West.
     - Therefore, as West, **ALWAYS act `[act: scout]`** every round (including Round 5). This safely secures +3 points each round with 0 risk of incoming theft, netting max points (+14 score).
   - **Universal Cooperative Scouts:**
     - If all players act `scout`, act `[act: scout]` early, and defect to `[act: raid]` in Round 5 to capture +3 from target.
   - **Incoming Threatening Raider:**
     - If incoming attacker raids me, act `[act: escort]` to protect points.

---

### Summary Checklist for Every Round

1. **Pledge:** Always `[pledge: scout]`.
2. **Act:**
   - Did target act `raid` last round? -> Act `[act: scout]`. Do NOT raid them.
   - Is attacker acting `escort`? -> I am safe. Act `[act: scout]`.
   - Is target a confirmed `scout` AND attacker not raiding me? -> Act `[act: raid]`.