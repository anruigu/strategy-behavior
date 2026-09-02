---
game: gen_icebound
model: gemini-flash
condition: neutral
seed: 0
round: 2
chars: 2876
---
# Playbook: Icebound

### Core Rules & Mechanics
- **Fuel Economy:** Unused fuel converts 1:1 to points at the end of round 5.
- **Costs:** Scout costs 1 fuel; Escort costs 2 fuel; Raid costs 2 fuel (charged from pledges).
- **Payoffs:**
  - `Scout`: +3 points if unraided (+2 net over fuel), 0 if raided (-1 net vs saving fuel).
  - `Escort`: +2 points, immune to theft. Net value vs saving fuel is 0 (spend 2 fuel to get 2 points), but protects points.
  - `Raid`: Targets clockwise (North $\to$ East $\to$ West $\to$ North). Steals +3 points from a scouting target (+1 net over fuel); loses -1 point against escort or raid (-3 net vs saving fuel).
- **Target Analysis:**
  - When playing as **West**: Target is **North**; Threat (predator) is **East**.
  - When playing as **North**: Target is **East**; Threat (predator) is **West**.
  - When playing as **East**: Target is **West**; Threat (predator) is **North**.

---

### Opponent History Tracking
- Carefully distinguish between what an opponent *pledged* and what they *acted* (e.g. `North scout/raid` means North pledged scout but executed raid).
- If an opponent consistently defects to `raid` (e.g., North constantly raiding East), recognize that they are an active raider and not a safe scout target.

---

### Pledge Stage Strategy
- When any pledge decision is put to me, I always reply `[pledge: scout]`.
  - Pledging scout charges only 1 fuel upfront, preserves the option to switch actions at the act stage, and avoids telegraphing aggression.

---

### Act Stage Strategy
1. **Target Status Check:**
   - Check what my clockwise target has historically executed.
   - If my target historically acts `raid` or `escort` (even if they pledged scout), they will NOT score as a scout. Raiding them will cost me 1 point (-3 net). **Do not raid non-scouts.**

2. **When to Scout (Default & High-Yield):**
   - When my counter-clockwise predator is not attacking me (e.g. East pledging/acting scout or escort without raiding West), I reply `[act: scout]`.
   - Scouting yields +3 points for 1 fuel (a net +2 point gain compared to keeping the fuel), making it strictly superior to raiding non-scouts and escorting when unthreatened.

3. **When to Raid:**
   - Only when my clockwise target reliably acts `scout` (verified from previous round histories or guaranteed by pattern), I reply `[act: raid]`.
   - If my clockwise target is a known persistent defector to `raid`, never raid them.

4. **When to Escort:**
   - When my counter-clockwise predator has shown a pattern of raiding me and I need to deny them the point transfer, I reply `[act: escort]`.
   - Otherwise, prefer `[act: scout]` to preserve fuel efficiency.

---

### Response Format
- Provide one short line of reasoning followed immediately by the bracketed action token:
  - `[pledge: scout]`
  - `[act: scout]`, `[act: escort]`, or `[act: raid]`