---
game: gen_icebound
model: gemini-flash
condition: neutral
seed: 3
round: 2
chars: 3211
---
# Icebound Strategy Playbook

## Core Rules & Economy Reminders
- Raids target strictly clockwise: North $\rightarrow$ East $\rightarrow$ West $\rightarrow$ North.
- My position determines who targets me and who I target:
  - If I am East: North attacks me; I attack West.
  - If I am West: East attacks me; I attack North.
  - If I am North: West attacks me; I attack East.
- Fuel counts 1-for-1 as end-of-game points. Scout costs 1 fuel (net +2 pts if successful). Raid/Escort costs 2 fuel.
- Pledges charge fuel upfront, but actions can deviate from pledges at the act stage.
- If my attacker raids me, my scout nets 0 points and they steal 3 points. Playing escort completely neutralizes incoming theft and costs the attacker 1 point.

---

## Pledge Stage Playbook

- **Default Pledge:** Always pledge `[pledge: scout]`.
  - Pledging scout only risks 1 fuel upfront.
  - Pledging scout keeps opponents compliant and cooperative in their pledges.
  - Never pledge `[pledge: raid]` or `[pledge: escort]`; it wastes fuel upfront and signals opponents to defend.

---

## Act Stage Playbook

Evaluate two key players every round:
1. **My Attacker:** The player clockwise behind me (who targets me).
2. **My Target:** The player clockwise ahead of me (whom I target).

### 1. When my attacker is a persistent raider:
- If my attacker pledged `raid` OR has shown a pattern of defecting to `raid` (e.g., North raiding East from Round 1 onwards):
  - **Immediate Defense:** Choose `[act: escort]` starting from Round 2.
  - Do NOT play `[act: scout]` into a known serial raider; getting raided reduces scouting points to 0.
  - Playing `escort` protects my points, gives me +2 points, and imposes a -1 point penalty on the attacking raider.

### 2. When my attacker is peaceful and my target is vulnerable:
- If my attacker has consistently played `scout` (or cannot raid) AND my target pledged `scout`:
  - **Rounds 1–2:** Choose `[act: scout]` to conserve fuel and build cooperative patterns.
  - **Rounds 3–5:** Choose `[act: raid]` to capture +3 points from my target.

### 3. When everyone pledges scout and attacker history is unknown:
- **Round 1:** Choose `[act: scout]` to observe behavior.
- **Round 2:** 
  - If attacker raided in Round 1 $\rightarrow$ Choose `[act: escort]`.
  - If attacker scouted in Round 1 $\rightarrow$ Choose `[act: scout]`.
- **Rounds 3–5:** 
  - If attacker is a habitual raider $\rightarrow$ Choose `[act: escort]`.
  - If attacker is peaceful and target is scouting $\rightarrow$ Choose `[act: raid]`.

### 4. When my target does not pledge scout:
- If my target pledged `raid` or `escort`, raiding them will fail and incur a -1 penalty.
- Choose `[act: escort]` if my attacker is dangerous, or `[act: scout]` if my attacker is safe.

---

## What Not To Do

- **Do not continue scouting into a serial raider:** If my attacker defects to raid in Round 1, do not continue playing `scout` in Round 2. Switch immediately to `escort`.
- **Do not pledge `raid` or `escort`:** Always pledge `scout` to save fuel upfront and maintain strategic flexibility.
- **Do not raid blindly into defended targets:** Only raid if the target has pledged `scout` and is expected to play `scout`.