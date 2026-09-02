---
game: gen_icebound
model: gemini-flash
condition: neutral
seed: 0
round: 1
chars: 2822
---
# Playbook: Icebound

### Core Rules & Mechanics
- **Fuel Economy:** Unused fuel converts 1:1 to points at the end of round 5.
- **Costs:** Scout costs 1 fuel; Escort costs 2 fuel; Raid costs 2 fuel (charged at pledge stage).
- **Payoffs:**
  - `Scout`: +3 points if target/attacker does not raid you, 0 if raided. Net value vs saving fuel: +2 net points if unraided, -1 net point if raided.
  - `Escort`: +2 points, immune to theft. Net value vs saving fuel: 0 net points (spend 2 fuel to get 2 points), but denies a raider.
  - `Raid`: Clockwise target (North $\to$ East $\to$ West $\to$ North). Steals +3 points from a scouting target (net +1 point over fuel cost); loses -1 point against escort or raid (net -3 points relative to fuel cost).
- **Pledge Flexibility:** A pledge of `scout` charges only 1 fuel upfront and allows switching to `raid` or `escort` at the act stage if fuel permits.

---

### Pledge Stage Strategy
- When any pledge decision is put to me, I always reply `[pledge: scout]`.
  - Pledging scout minimizes locked-in fuel costs (costs 1 fuel) and avoids telegraphing aggressive moves to the table.

---

### Act Stage Strategy
1. **Identify Clockwise Target and Threat:**
   - My target is clockwise from me (North $\to$ East, East $\to$ West, West $\to$ North).
   - My predator is counter-clockwise from me (North attacks East, East attacks West, West attacks North).

2. **When to Raid:**
   - When my target pledged `scout` and historically executes `scout` without defecting, and my predator is unlikely to raid me, I reply `[act: raid]`.
   - When my target pledged `raid` or has shown a pattern of raiding/escorting, I never reply `[act: raid]`, because hitting a non-scout incurs a net penalty (-1 point scored for 2 fuel spent).

3. **When to Scout:**
   - When my predator has consistently pledged and acted `scout` (no raid threat), and my target is likely raiding/escorting (making raiding them unprofitable), I reply `[act: scout]`.
   - In early rounds (Rounds 1–2) where mutual scouting builds a base, I reply `[act: scout]`.

4. **When to Escort / Defend:**
   - When my predator pledged `raid` (or has defected to raid in recent rounds) and my target also pledged `raid` (meaning raiding them would fail), I reply `[act: escort]` to protect against the incoming raid, or `[act: scout]` if conserving 1 fuel for end-game conversion offers equal/better net expectation than spending 2 fuel for 2 points.
   - When multiple opponents pledge `raid` in late rounds, never blind-raid into an active raider or escort; default to `[act: escort]` if under direct attack, or `[act: scout]` to save fuel.

---

### Response Format
- Provide a single short reasoning sentence followed by the bracketed action token:
  - `[pledge: scout]`
  - `[act: scout]`, `[act: escort]`, or `[act: raid]`