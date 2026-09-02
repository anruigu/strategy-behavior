---
game: gen_icebound__steal_5_hard_fail
model: gemini-flash
condition: neutral
seed: 2
round: 3
chars: 2138
---
# Playbook: Icebound

### Core Rules & Mechanism
- Fuel is charged based strictly on the public pledge: scout = 1, escort = 2, raid = 2.
- Unused fuel converts 1:1 into points at the end of round 5.
- Actions resolve based strictly on the submitted act, regardless of pledge (pledge/act mismatches are accepted and resolved by the referee).
- Raids resolve strictly clockwise: North $\to$ East $\to$ West $\to$ North.
- Scout scores +3 if not raided, 0 if raided.
- Escort scores +2 and blocks incoming raids (incoming raider takes -6 penalty).
- Raid steals +5 points from a target acting `scout`, but costs the raider -6 points if the target acts `escort` or `raid`.

---

### Pledge Stage
- Always submit `[pledge: scout]` in all 5 rounds. This minimizes fuel consumption to 1 fuel per round, preserving fuel bonus points (+3 points at game end) while keeping full tactical flexibility at the act stage.

---

### Act Stage Strategy

1. **Neighbor Identification:**
   - Predecessor (can raid me): North if East; West if North; East if West.
   - Target (I can raid): West if East; North if West; East if North.

2. **Reading Target Behavior & Pledges:**
   - **Target Pledges Scout:** 
     - Check target's historical act pattern. If the target consistently executes `scout` when pledging scout, choose `[act: raid]` to steal +5 points.
   - **Target Pledges Escort or Raid:**
     - Even if the target secretly acts `scout` (e.g. West pledging escort but acting scout to save face/deter attacks), assume high risk of hitting an escort/raid barrier. Choose `[act: escort]` to secure +2 points and stay safe from counter-raids.

3. **Defending Against Predecessors:**
   - If predecessor pledges or acts `raid`, or is suspected of defecting to `raid`, choose `[act: escort]`. This banks +2 points, prevents theft, and inflicts a -6 penalty on the attacking predecessor.

4. **Decision Matrix:**
   - If my target pledged `scout` AND has been reliably acting `scout`: `[act: raid]`.
   - If my target pledged `escort` or `raid`: `[act: escort]`.
   - If predecessor is threatening a raid and target is risky/defensive: `[act: escort]`.