---
game: gen_icebound
model: gemini-flash
condition: neutral
seed: 2
round: 2
chars: 2114
---
# Icebound Strategy Playbook

## Core Rules & Economy Reminders
- Raids strictly target clockwise: North $\to$ East $\to$ West $\to$ North.
- Fuel cost is charged at the **pledge** stage: `scout` (1), `escort` (2), `raid` (2). Unused fuel converts to points 1:1 at game end.
- Actions resolve based on the **act** stage; deviation from the pledge is allowed by the engine.
- Against a `scout`, a `raid` steals 3 points (target gets 0).
- Against an `escort` or `raid`, a `raid` suffers a 1-point penalty (-1 net from raid, escort gets 2 points).
- A safe `scout` yields 3 points for 1 fuel (net +2 points vs holding fuel). An `escort` yields 2 points for 1 fuel (if pledged scout, yielding net +1 point vs holding fuel).

---

## Pledge Stage Playbook
- **Always pledge `scout` in every round (Rounds 1–5).**
  - Pledging `scout` charges only 1 fuel upfront, preserving fuel points while keeping maximum tactical flexibility for the Act stage.
  - Never pledge `escort` or `raid` upfront; it locks in an extra 1 fuel cost unnecessarily.

---

## Act Stage Playbook

### 1. Identifying Threats and Targets
- **Incoming Threat:** The player immediately counter-clockwise from me (West if I am North, North if I am East, East if I am West).
- **Clockwise Target:** The player immediately clockwise from me (East if I am North, West if I am East, North if I am West).

### 2. Rounds 1–4
- If the incoming threat pledged `scout` and has not raided in past rounds, act `scout`.
- If the incoming threat pledged `raid` or has recently raided, act `escort`.
- Act `scout` as the default to sustain mutual cooperative scoring (+3 points/round).

### 3. Final Round (Round 5)
- **Always act `escort` in Round 5.**
  - Other players frequently attempt end-game raids or switch to escort/raid.
  - Acting `raid` against a target that acts `escort` or `raid` results in a net penalty (-1 point), leading to lower scores (e.g. 14.0 instead of 17.0).
  - Acting `escort` guarantees defense against incoming raids and reliably secures 2 points for 1 pledged fuel (guaranteeing 17.0 total score under mutual 4-round scout history).