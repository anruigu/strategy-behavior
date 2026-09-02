---
game: gen_icebound
model: gemini-flash
condition: neutral
seed: 3
round: 3
chars: 3039
---
# Icebound Strategy Playbook

## Core Rules & Economy Reminders
- Raids target strictly clockwise: North $\rightarrow$ East $\rightarrow$ West $\rightarrow$ North.
- My position determines my attacker and target:
  - If I am East: North attacks me; I attack West.
  - If I am West: East attacks me; I attack North.
  - If I am North: West attacks me; I attack East.
- Fuel counts 1-for-1 as end-of-game points. Scout costs 1 fuel (net +2 pts if successful). Raid/Escort costs 2 fuel.
- Pledges charge fuel upfront, but actions can freely deviate from pledges at the act stage.
- If my attacker raids me, my scout nets 0 points and they steal 3 points. Playing escort completely neutralizes incoming theft, gives me +2 points, and costs the attacker 1 point.

---

## Pledge Stage Playbook

- **Default Pledge:** Always pledge `[pledge: scout]`.
  - Pledging scout only costs 1 fuel upfront.
  - Pledging scout keeps opponents cooperative and predictable in their pledges.
  - Never pledge `[pledge: raid]` or `[pledge: escort]`; it wastes fuel upfront and signals opponents to defend.

---

## Act Stage Playbook

Evaluate two key players every round:
1. **My Attacker:** The player clockwise behind me (who targets me).
2. **My Target:** The player clockwise ahead of me (whom I target).

### 1. Attacker is raiding (Defensive Priority):
- If my attacker raided in the previous round, or has shown a pattern of defecting to raid:
  - **Action:** Choose `[act: escort]`.
  - Never play `[act: scout]` into a known raider; getting raided results in 0 round points.
  - Never switch to `[act: raid]` if my attacker is raiding me, because raiding offers no protection against incoming theft.

### 2. Attacker is peaceful and Target is scouting (Offensive Opportunity):
- If my attacker has consistently played `scout` (or cannot raid) AND my target pledged `scout`:
  - **Rounds 1–2:** Choose `[act: scout]` to conserve fuel and observe behavior.
  - **Rounds 3–5:** Choose `[act: raid]` to capture +3 points from my target.

### 3. Neutral / Unknown Baseline:
- **Round 1:** Always choose `[act: scout]` to establish a baseline.
- **Round 2+ Decision Tree:**
  - Did my attacker raid last round? $\rightarrow$ Play `[act: escort]`.
  - Did my attacker scout last round AND target pledged scout?
    - Rounds 2: Play `[act: scout]`.
    - Rounds 3–5: Play `[act: raid]`.
  - Did my target pledge/act raid or escort while attacker is peaceful? $\rightarrow$ Play `[act: scout]`.

---

## What Not To Do

- **Do not raid when under active attack:** If my attacker is raiding me, raiding my target does not protect my points. Play `[act: escort]`.
- **Do not continue scouting into an active raider:** As soon as my attacker raids, immediately switch to `[act: escort]` in subsequent rounds until they stop.
- **Do not pledge `raid` or `escort`:** Always pledge `[pledge: scout]` to conserve fuel upfront and maintain flexibility.
- **Do not raid defended targets:** If the target pledged or acts `raid` or `escort`, raiding incurs a -1 penalty.