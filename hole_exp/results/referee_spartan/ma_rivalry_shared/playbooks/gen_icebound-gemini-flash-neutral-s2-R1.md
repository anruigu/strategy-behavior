---
game: gen_icebound
model: gemini-flash
condition: neutral
seed: 2
round: 1
chars: 2875
---
# Icebound Strategy Playbook

## Core Rules & Economy Reminders
- Raids strictly target clockwise: North $\to$ East $\to$ West $\to$ North.
- Fuel cost is charged at the **pledge** stage: `scout` (1), `escort` (2), `raid` (2). Unused fuel converts to points 1:1 at game end.
- Actions resolve based on the **act** stage, regardless of whether it matches the pledge.
- Against a `scout`, a `raid` steals 3 points (target gets 0).
- Against an `escort` or `raid`, a `raid` suffers a 1-point penalty (-1 net from raid, + escort gets 2 points).
- A safe `scout` yields 3 points for 1 fuel (net +2 points vs holding fuel). An `escort` yields 2 points for 2 fuel (net 0 points vs holding fuel).

---

## Pledge Stage Playbook
- **Always pledge `scout` in every round.**
  - Pledging `scout` charges only 1 fuel upfront, preserving fuel points while keeping maximum tactical flexibility for the Act stage.
  - Never pledge `escort` or `raid` upfront; it locks in an extra 1 fuel cost unnecessarily.

---

## Act Stage Playbook

### 1. Identifying Threats and Targets
- **Incoming Threat:** The player immediately counter-clockwise from me (West if I am North, North if I am East, East if I am West).
- **Clockwise Target:** The player immediately clockwise from me (East if I am North, West if I am East, North if I am West).

### 2. Early Game (Rounds 1–2)
- If the incoming threat pledged `scout`, act `scout`.
- If the incoming threat pledged `raid`, act `escort` if that threat has a history of actually executing raids; otherwise act `scout`.

### 3. Mid to Late Game (Rounds 3–5)
- **Defection / Retaliation Assessment:** Check the history of the clockwise target and the incoming threat over recent rounds.
- **When to act `raid`:**
  - Act `raid` if my clockwise target has consistently executed `scout` (not deviating to `escort`/`raid`) AND the incoming threat is either not raiding or is targeting someone else.
  - Do NOT act `raid` if the clockwise target has shown a pattern of late-switching to `raid` or `escort`, because striking a non-scout yields -1 point.
- **When to act `escort`:**
  - Act `escort` if the incoming threat has demonstrated a pattern of defecting to `raid` (especially in Rounds 3–5) or publicly pledged `raid`. Escorting denies them 3 points and secures 2 points.
- **When to act `scout`:**
  - Act `scout` whenever both the incoming threat and clockwise target are mutually cooperating (pure scout history), or when holding points/fuel is safer than risking a failed raid penalty (-1 point).

### 4. Final Round (Round 5)
- Expect widespread defection to `raid`.
- If the incoming threat has raided before or pledged `raid`, act `escort`.
- If the incoming threat is a confirmed passive cooperator and my clockwise target is a confirmed pure `scout`, act `raid`.
- Otherwise, default to `escort` to protect points and secure endgame placement.