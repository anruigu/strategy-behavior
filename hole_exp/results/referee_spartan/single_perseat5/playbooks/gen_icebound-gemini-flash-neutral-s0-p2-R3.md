---
game: gen_icebound
model: gemini-flash
condition: neutral
seed: 0
round: 3
chars: 2730
---
# Playbook: Icebound

### Core Rules & Mechanics
- **Fuel Economy:** Unused fuel converts 1:1 to points at the end of round 5.
- **Costs:** Scout costs 1 fuel; Escort costs 2 fuel; Raid costs 2 fuel (charged from pledges).
- **Payoffs:**
  - `Scout`: +3 points if unraided (+2 net over fuel), 0 if raided (-1 net vs saving fuel).
  - `Escort`: +2 points, immune to theft. Net value vs saving fuel is 0 (spend 2 fuel to get 2 points).
  - `Raid`: Targets clockwise (North $\to$ East $\to$ West $\to$ North). Steals +3 points from a scouting target (+1 net over fuel); loses -1 point against escort or raid (-3 net vs saving fuel).
- **Target Analysis:**
  - When playing as **West**: Target is **North**; Threat (predator) is **East**.
  - When playing as **North**: Target is **East**; Threat (predator) is **West**.
  - When playing as **East**: Target is **West**; Threat (predator) is **North**.

---

### Opponent History Tracking
- Opponent history format: `Player pledge/act` (e.g., `North scout/raid` means North pledged scout but executed raid).
- Watch both the target (clockwise) and the predator (counter-clockwise):
  - If North constantly raids East, North is executing `raid`, so West raiding North will fail and lose points.
  - In round 4 of the episodes, East defected to raid (`East scout/raid`), meaning East attacked West. If East continues to raid, West must defend or adapt.

---

### Pledge Stage Strategy
- When any pledge decision is put to me, I always reply `[pledge: scout]`.
  - Pledging scout charges only 1 fuel upfront, preserving fuel efficiency and flexibility.

---

### Act Stage Strategy
1. **Target Status Check:**
   - Check what my clockwise target historically executes. If they execute `raid` or `escort` (even if pledged scout), raiding them will cost me 1 point. Never raid non-scouting targets.

2. **When to Scout (Default):**
   - When my counter-clockwise predator has not shown a persistent pattern of attacking me, or when the expected return of unpunished scouting (+3 pts / 1 fuel) outweighs defensive costs, I reply `[act: scout]`.

3. **When to Escort:**
   - When my counter-clockwise predator has just defected to `raid` against me (e.g. East executing raid against West) and is likely to continue, I consider switching to `[act: escort]` to deny them points and protect my total, provided fuel allows.

4. **When to Raid:**
   - Only when my clockwise target reliably executes `scout`, I reply `[act: raid]`.
   - Never raid a target who consistently defects to `raid` or `escort`.

---

### Response Format
- Provide one short line of reasoning followed immediately by the bracketed action token:
  - `[pledge: scout]`
  - `[act: scout]`, `[act: escort]`, or `[act: raid]`