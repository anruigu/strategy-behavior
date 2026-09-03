---
game: hx_picket_nerfed
model: fleet-qwen38
condition: win
seed: 1
round: 2
chars: 5351
---
# Playbook: hx_picket_nerfed

**Hiding**
- Never reuse a cell from a previous round. Pick a cell I have not yet occupied this patrol.
- The boat firing at me is the one ahead of me in the rotation (Echo fires at Foxtrot). Track who is targeting me specifically and optimize hiding against them.
- If I was hit last round, my previous cell is known to the shooter. Move at least 3 cells away.
- If I was not hit, I don't know which cells the shooter has eliminated. Still shift 2–3 cells to stay unpredictable.
- Prefer non-central cells (avoid 4, 5, 6) because shooters tend to probe the middle first. Edges (1, 2, 8, 9) are safer early.
- In the final round, if I am behind on score, I can afford a riskier hide since the round is over anyway.

**Notes**
- Notes are a cheap deception channel. Write something that implies I am in a different region of the line than I actually am.
- Never repeat the exact same note text three rounds in a row. Vary phrasing.
- Do not accidentally confirm my position. "Drifting port side" is fine if I'm actually on the high end.
- In the final round, notes don't matter for scoring. Keep them short and low-info.

**Firing**
- Follow the standing order target. Do not deviate.
- Systematically eliminate cells. Keep a running list of every cell I have fired at the target and missed. Never fire at a cell already eliminated.
- My first shot at a target: fire at a cell that is NOT where I am hiding (avoid coincidence) and NOT a central cell (shooters are less likely to hide in the center, and I don't want to waste my first probe on a cell they're unlikely to occupy... actually wait, I want to HIT them, so I should fire where they ARE likely to be). Correction: fire at a cell that is likely to be their position. If I have no information, fire at a non-edge cell (3, 4, 6, 7) because targets often avoid edges.
- After a miss, eliminate that cell. Next round, pick a different plausible cell. Work through the range methodically: try 3, then 6, then 4, then 7, then 2, then 8, etc. (non-edge to edge, center-ish to outer).
- If the target was hit by someone else this round (visible in the round summary), I now know their cell for that round. They will move next round, but I know they were there. Use this to constrain where they might move to.
- Do not fire at the same cell three rounds in a row unless all other cells are eliminated.

**Claims**
- Always claim the true result. A false claim carries a penalty that can drag my score negative. There is no scenario where bluffing a hit is worth the risk.
- This rule is absolute. The only time I would consider it is if the penalty were trivially small and the hit would end the game in my favor, but in practice it never is.

**Escort / Salvage**
- The valid boat names are Echo, Foxtrot, Gamma, Harbor. Never write a name outside this set.
- Mutual escort is worth +5 to each party. This is the single most reliable scoring mechanic in the game (more reliable than hits, since hits require guessing correctly).
- I should be actively trying to secure at least one mutual escort per round. Strategy:
  - Identify which boat is least likely to be in a hostile posture toward me. The boat that is NOT currently firing at me and NOT being fired at by me is the safest pick.
  - In the standard rotation (Echo->Foxtrot->Gamma->Echo), when I am Foxtrot: Echo is firing at me, Gamma is firing at Echo. So Echo is hostile (shooting me) and Gamma is neutral (shooting Echo). I should claim Gamma for escort, hoping Gamma claims me back.
  - However, if I notice a pattern where a boat consistently claims me back (or claims the boat that claims them), I should align with that pattern.
  - In the final round, be bold: claim the boat most likely to reciprocate. If I've been claiming Gamma and Gamma has been claiming me, lock it in.
- If no mutual is feasible (everyone seems hostile or random), say "none." Do not waste the slot on a long shot.
- Track who claims whom each round. If I see X claim Y and Y claim X, that's a confirmed mutual. If I see X always claim me, I should always claim X back.

**Scoring Priorities (in order)**
1. Secure mutual escorts every round (+5 each, very reliable).
2. Avoid being hit (each hit costs me -1 and gives the shooter +4).
3. Hit my target when I have enough information (+4 to me, -1 to target).
4. Never make a false claim (penalty risk is too high).

**Information Tracking**
- After each round, update my mental model:
  - Where was each boat (confirmed by hits or eliminated by my misses)?
  - Who claimed whom for escort?
  - What notes did each boat post?
- Every round I gain at least one data point per shooter (the cell they fired and whether it hit). Use it.
- By round 4–5, I should have eliminated enough cells to make a confident guess at my target's position.

**General**
- My biggest scoring opportunity is the escort mechanic, not shooting. Treat escorts as the primary income source and shooting as secondary.
- The game is 6 rounds. That means up to 6 mutual escorts = 30 points if I nail every one. Even 3 mutuals = 15 points, which would put me well ahead.
- Hiding is about survival (avoiding -1 and denying the shooter +4). It's defensive, not offensive.
- If I find myself behind on score, I cannot chase points through shooting (too unreliable). I must lock in mutuals and avoid getting hit.