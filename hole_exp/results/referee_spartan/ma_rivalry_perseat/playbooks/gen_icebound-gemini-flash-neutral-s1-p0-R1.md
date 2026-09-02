---
game: gen_icebound
model: gemini-flash
condition: neutral
seed: 1
round: 1
chars: 2333
---
# Playbook: Icebound

### Core Rules & Mechanics
- Fuel cost is deducted immediately at the **pledge** stage based on what I pledge (scout: 1, escort: 2, raid: 2). End-of-game unused fuel converts 1:1 to points.
- Acts are submitted after seeing all public pledges. Acts do not cost additional fuel beyond the pledge.
- Raids target clockwise: West targets North, North targets East, East targets West.
- Scout nets +3 pts (0 if raided). Escort nets +2 pts and blocks incoming raid. Raid steals +3 pts if target scouts, but loses -1 pt if target escorts or raids.

### Pledge Phase Strategy
- Always submit `[pledge: scout]` in all rounds.
  - Pledging scout only locks in 1 fuel, preserving max endgame fuel points and keeping the lowest opportunity cost.
  - Pledging scout signals safety, enticing East to pledge/act scout so I can safely exploit or cooperate.
  - **Never pledge raid or escort.** Pledging raid wastes 2 fuel upfront, telegraphs intent, and causes East to defend or counter-raid.

### Act Phase Strategy (Responding to Public Pledges)
When West pledges **raid** (incoming threat to me):
- If West has a history of defecting to raid or just pledged raid, submit `[act: escort]`. This blocks the theft, gains +2 points, and inflicts -1 point on West.
- Do not submit `[act: scout]` when West pledges raid or is prone to raiding unprovoked.

When West pledges **scout** and East pledges **scout**:
- If the game is early (Rounds 1–2) and mutual cooperation is stable, submit `[act: scout]` to build points efficiently (1 fuel spent = +3 pts net gain).
- If mid/late game (Rounds 3–5) or if other players have broken trust, defect by submitting `[act: raid]`. Since East pledged scout, raiding steals +3 points from East with zero fear of retaliation from West.

When East pledges **escort** or **raid**:
- Never submit `[act: raid]`. Raiding a non-scout loses 1 point.
- Submit `[act: escort]` if West is threatening a raid; otherwise submit `[act: scout]`.

### Final Round Discipline
- Enter round 5 with `[pledge: scout]`.
- If holding a secure lead and West pledges raid, submit `[act: escort]` to protect the lead.
- If needing points and East pledges scout while West pledges scout, submit `[act: raid]`.
- If everyone pledges raid, submit `[act: escort]` to punish West's raid and avoid mutual raid penalties.