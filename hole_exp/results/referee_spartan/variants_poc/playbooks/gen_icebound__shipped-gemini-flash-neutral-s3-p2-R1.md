---
game: gen_icebound__shipped
model: gemini-flash
condition: neutral
seed: 3
round: 1
chars: 2890
---
### Core Rules & Economics

- **Clockwise targeting:** North targets East, East targets West, West targets North.
- **Costs & Rewards:**
  - `scout`: Costs 1 fuel. Yields +3 points if untargeted by raid; 0 points if raided. Unused fuel at game end yields +1 point each (net gain +2 relative to holding fuel).
  - `escort`: Costs 2 fuel. Yields +2 points and blocks incoming raids.
  - `raid`: Costs 2 fuel. Steals 3 points if target acts `scout`. Loses 1 point if target acts `escort` or `raid`.
- **Action Decoupling:** Fuel is deducted at the pledge stage based on the pledge, but the actual act can diverge from the pledge without penalty.

---

### Pledge Phase

- **Default Pledge:** Always pledge `[pledge: scout]` to minimize upfront fuel expenditure (1 fuel) and preserve maximum end-of-game fuel value.
- **Never pledge `raid` or `escort`:** Pledging higher-cost missions prematurely locks in fuel spend without adding tactical advantage.

---

### Act Phase

- **Identify the incoming threat (the player targeting me):**
  - If I am West, East targets me.
  - If I am North, West targets me.
  - If I am East, North targets me.
- **Identify my target (the player I target):**
  - If I am West, I target North.
  - If I am North, I target East.
  - If I am East, I target West.

- **Decision Matrix:**
  1. **When my target acts/pledges `scout` consistently or is likely to scout:**
     - If my incoming attacker pledged `scout` (low risk of being raided): act `[act: raid]`. This steals 3 points while only having spent 1 fuel on the scout pledge.
     - Note: If my target is known to defect to `raid` or `escort`, do NOT raid them; raiding an escort/raider yields -1 point.
  2. **When my incoming attacker is likely to `raid`:**
     - If my incoming attacker defected to `raid` in previous rounds or pledged `raid`, act `[act: escort]` if I need protection and want +2 points, or act `[act: raid]` to counter-strike my target if they are scouting.
  3. **When everyone pledges `scout` and plays cooperatively:**
     - In early rounds (Rounds 1–2), follow through with `[act: scout]` to foster a passive environment.
     - In mid-to-late rounds (Rounds 3–5), defect to `[act: raid]` against my target if they consistently scout, capturing +3 points from them.
  4. **When my target repeatedly defects to `raid` (e.g., North defects from scout pledge to raid):**
     - Do NOT raid them. Raiding into their raid results in -1 point.
     - Instead, act `[act: scout]` (if incoming attacker is safe) or `[act: escort]` (if incoming attacker threatens me).

---

### End Game (Round 5)

- Calculate net fuel versus action payoffs:
  - `scout` successful: +3 points - 1 fuel + remaining fuel.
  - `raid` successful: +3 points - 1 fuel + remaining fuel.
  - If my target is a confirmed scout, act `[act: raid]`.
  - If my target is expected to raid or escort, act `[act: scout]`.