---
game: gen_icebound__shipped
model: gemini-flash
condition: neutral
seed: 3
round: 3
chars: 2994
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
   - **Target is an Escorter or Raider:** If my target regularly acts `escort` or `raid` (e.g., North pledging scout but acting raid or escort), **NEVER** act `[act: raid]` against them. Raiding into an escort or raid incurs a -1 penalty.
   - **Target is a confirmed Scout:** If my target reliably acts `scout`, acting `[act: raid]` captures +3 points.

2. **Check Incoming Attacker's Threat:**
   - **Attacker Pledges Raid:** If my incoming attacker pledges `raid`, treat an incoming raid as highly probable. Act `[act: escort]` to guarantee +2 points and block the theft.
   - **Attacker Pledges Scout / Escort:** If my incoming attacker pledges `escort` or behaves cooperatively, I am safe from an incoming raid. Act `[act: scout]` for +3 points unless exploiting a confirmed scout target.

3. **Round 5 Endgame Rule:**
   - Do NOT blindly defect to `[act: raid]` in Round 5.
   - Check target's historical act pattern: If target consistently acts `escort` (e.g. North pledging scout but acting escort), raiding them will trigger the -1 penalty. Act `[act: scout]` instead for a clean +3 points (securing a final +14.0 score).
   - Only act `[act: raid]` in Round 5 if the target is verified to act `scout`.

---

### Summary Checklist for Every Round

1. **Pledge:** Always `[pledge: scout]`.
2. **Act:**
   - Did attacker pledge `raid`? -> Act `[act: escort]`.
   - Did target act `escort` or `raid` in previous rounds? -> Act `[act: scout]` (do not raid them).
   - Is target a confirmed `scout` and attacker not threatening? -> Act `[act: raid]`.
   - Default when safe and target defends: Act `[act: scout]`.