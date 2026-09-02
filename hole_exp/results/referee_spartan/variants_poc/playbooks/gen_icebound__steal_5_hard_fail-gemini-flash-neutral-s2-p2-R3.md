---
game: gen_icebound__steal_5_hard_fail
model: gemini-flash
condition: neutral
seed: 2
round: 3
chars: 3448
---
# Playbook: Icebound

### Core Rules & Mechanics Review
- **Directional targeting:** Raids resolve clockwise: North -> East -> West -> North.
  - As North: I raid East; West raids me.
  - As East: I raid West; North raids me.
  - As West: I raid North; East raids me.
- **Pledge vs Act Consistency:** The engine allows submitting any valid action token (`scout`, `escort`, `raid`) at the act stage regardless of pledge. Fuel cost is charged strictly at the *pledge* stage based on the pledge (Scout 1, Escort 2, Raid 2). Scoring resolutions are evaluated based *entirely* on the submitted act.
- **Raid outcomes:**
  - Raider vs Target Scout: Raider steals/gains +5 points; Target gets 0 points.
  - Raider vs Target Escort or Raider: Raider loses 6 points (-6); Target keeps their normal resolution (Escort scores +2).
- **Fuel scoring:** Unused fuel at the end converts to +1 point each.

---

### Strategy and Decision Making

#### 1. CRITICAL: Follow Through on Intended Acts
- **Never default-act `[act: scout]` when planning defense or offense.**
  - If I pledge `[pledge: escort]`, I paid 2 fuel for protection. I MUST submit `[act: escort]`. Submitting `[act: scout]` leaves me vulnerable to being raided for 0 points while wasting the extra fuel.
  - If I pledge `[pledge: raid]`, I paid 2 fuel to attack. I MUST submit `[act: raid]`. Submitting `[act: scout]` forfeits the raid payoff entirely.
- In general, when I choose an action strategy for a round, align both the pledge and the act to that action unless intentionally faking a pledge.

#### 2. Handling Aggressive Incoming Raiders
- When my incoming raider regularly defects to `raid` (e.g. East pledging scout and acting raid/escort):
  - I must actively defend. Submit `[pledge: escort]` and MUST submit `[act: escort]`.
  - When the incoming raider attacks into my escort, they suffer -6 points and I score +2 points.
  - Continue defending as long as the incoming raider poses an active threat.

#### 3. Exploiting Passive Scouters
- When my clockwise target consistently pledges and acts `scout` (and I am either safe from incoming raids or willing to risk it):
  - Raiding yields +5 points (net +4 accounting for the 1 extra fuel cost compared to scouting +3).
  - Submit `[pledge: raid]` (or `[pledge: scout]`) and crucially submit `[act: raid]`.
  - **Warning:** Do not raid if my clockwise target pledges `escort` or `raid`, or if they frequently defect to `raid`, as hitting an escort or raider inflicts a -6 point penalty.

#### 4. General Game Flow
- **Round 1:**
  - Pledge `[pledge: scout]`, Act `[act: scout]`. Establish baseline points and observe player tendencies.
- **Subsequent Rounds:**
  - **Defense First:** If my incoming raider has raided me in past rounds, pledge `[pledge: escort]` AND submit `[act: escort]`.
  - **Offense Second:** If incoming raid risk is low/absent and my clockwise target reliably acts `scout`, pledge `[pledge: raid]` AND submit `[act: raid]`.
  - **Cooperation / Conservation:** If incoming raider is peaceful and target is not safely raid-able, pledge `[pledge: scout]` AND submit `[act: scout]` to accumulate +3 per round and bank unused fuel (+1 per fuel at the end).

#### Key Execution Check
- At every act prompt, actively match my submitted act token to my chosen tactical stance for that round (`[act: escort]` for defense, `[act: raid]` for attack, `[act: scout]` for passive income). Never blindly output `[act: scout]`.