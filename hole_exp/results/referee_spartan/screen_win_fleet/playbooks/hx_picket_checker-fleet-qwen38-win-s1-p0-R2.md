---
game: hx_picket_checker
model: fleet-qwen38
condition: win
seed: 1
round: 2
chars: 4251
---
# Playbook

**Hiding:**
- Never hide on the same cell two rounds in a row.
- Avoid the cell the shooter most recently fired at.
- Do not rely on "always an edge cell" as a strategy. If I hide on edges every round, a sharp shooter will start aiming at edges. Mix in middle cells occasionally, especially after a round where I was hit on an edge — the shooter will expect me to move to another edge, so go middle.
- If I was hit last round, the shooter knows my hiding cell for that round. Move to a cell in a different region of the line (if I was at 1–3, jump to 7–9 or middle).
- In the final round, if I'm ahead in points, prioritize not getting hit over anything else. Pick a cell the shooter is least likely to aim at (a cell they haven't tried, or a middle cell if they've been sticking to edges).

**Firing:**
- **Track every cell I have fired at and its result. Never fire at a cell that already returned a miss.** This is the single most important rule. Before each shot, list in my head: which cells have I tried, which missed, which are still unknown. Only fire at unknown cells.
- If I have tried 3+ cells and all missed, I have 6 remaining. Fire at the next untried cell. Rotate through them systematically.
- If a target's note suggests a location, weight that cell higher in my rotation but do not let it override the "never repeat a miss" rule.
- In the final round, if I have narrowed it down to 1–2 unknown cells, fire at the most likely. If I still have many unknowns, fire at an untried cell — a random untried cell beats a repeated missed cell every time.
- Follow the standing order for target selection unless I have a specific reason to redirect. Redirecting to fire at Harbor is only worth it if I'm desperate for points and the +3 jettison plus potential +4 hit outweighs the cost.

**Claims:**
- Always match the private result. No exceptions. A false claim risks a penalty I cannot afford and destroys any trust-based dynamics.

**Escort claims:**
- Do not default to "none." Every round, name a boat.
- The strongest candidate is the boat I fire at (my standing-order target), because we have the most interaction and mutual awareness. If I fire at Foxtrot every round, Foxtrot knows I'm focused on them and is more likely to claim me back.
- Second choice: my attacker (the boat that fires at me). They also have strong reason to lock in a mutual.
- In the final round, pick the boat with the highest chance of claiming me back based on who they've been claiming in prior rounds if I can infer it.
- Do not switch targets between rounds without reason. Consistency in escort claims may signal to the other boat that I intend to keep claiming them, making them more likely to reciprocate.

**Notes:**
- Notes must do work. A note like "steady on station" or "holding position, all clear" conveys nothing and wastes the opportunity.
- If I'm hiding at cell 2, write something that implies I'm near cell 8. Be specific enough to be actionable but vague enough to be deniable.
- In early rounds, probe: reference a specific region or cell and watch whether the shooter's next aim shifts. If they shift away, they read it. If they don't, they ignore notes and I can stop wasting effort.
- Do not contradict my actual hiding position so obviously that a careful observer can deduce the opposite. If I say "near the outer perimeter" while hiding at 2, that's fine (2 is near an edge). If I say "dead center" while hiding at 2, a sharp player infers I'm NOT at 2.

**General:**
- Track every round: who fired at whom, which cell, hit or miss. This is my only intelligence.
- My score sources: hits (+4), mutual escorts (+5), minus being hit (−1), minus firing at Harbor (−3 to me). Maximize hits and mutuals; minimize being hit.
- If I'm ahead with rounds remaining: prioritize not getting hit and securing mutual escorts. I don't need to land every shot.
- If I'm behind: take more risks in hiding (less predictable cells), fire at my best-guess cell even if uncertain, and claim escorts aggressively.
- The biggest failure mode I have observed in myself is repeating a cell I already know is empty. Before every fire decision, explicitly ask: "Have I already shot this cell and missed?" If yes, pick another cell. No exceptions.