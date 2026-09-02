---
game: gen_icebound
model: gemini-flash
condition: neutral
seed: 3
round: 1
chars: 2690
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

---

## Pledge Stage Playbook

- **Default Pledge:** Always pledge `[pledge: scout]`.
  - Pledging scout only risks 1 fuel upfront.
  - Pledging scout encourages other players to pledge scout, keeping them vulnerable and cooperative.
  - Never pledge `[pledge: raid]` or `[pledge: escort]`; it wastes fuel at the pledge stage and warns opponents to defend or counter.

---

## Act Stage Playbook

Analyze the combination of:
1. The player who targets me (my attacker).
2. The player I target (my victim).

### 1. When my attacker has a history of defecting to raid (or has pledged raid):
- If the player targeting me has raided unprovoked in previous rounds, or if they pledged `raid`:
  - Choose `[act: escort]`.
  - Do not choose `[act: scout]`, as a successful raid against me costs 3 points and awards the attacker 3 points.

### 2. When my attacker is peaceful and my victim is vulnerable:
- If the player targeting me is reliable/peaceful AND my victim pledged `scout`:
  - If round $\ge 3$ or if it is round 5: choose `[act: raid]` to steal 3 points from my victim.
  - In rounds 1 and 2: choose `[act: scout]` to establish trust and maintain low fuel expenditure.

### 3. When everyone pledges scout and no one has shown aggression:
- In early rounds (Rounds 1–2): choose `[act: scout]`.
- In mid-to-late rounds (Rounds 3–5): choose `[act: raid]` if my victim has consistently followed through with `scout`.

### 4. When my victim pledged raid or escort:
- If my victim did not pledge `scout`, raiding them will fail or incur a penalty. Choose `[act: scout]` (or `[act: escort]` if my attacker is dangerous).

---

## What Not To Do

- **Do not pledge `raid`:** It burns 2 fuel immediately and telegraphs an attack, prompting your target to escort or retaliate.
- **Do not blindly scout all 5 rounds:** Pure cooperation leaves easy points on the table and makes me a passive target for endgame defection.
- **Do not raid blindly into multiple raiders/escorts:** Raiding against an escort or another raider costs 1 point and wastes 2 fuel. Only raid when confident the target will actually play `scout`.