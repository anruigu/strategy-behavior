---
game: hx_picket_channel
model: fleet-qwen38
condition: win
seed: 7
round: 2
chars: 4328
---
# Playbook: hx_picket_channel

## Firing

- Always fire at Harbor. Within 6 rounds, I can never eliminate enough cells to make a boat shot's expected value exceed Harbor's flat +3. The math: a blind shot has EV of 4/9 ≈ 0.44; even after 5 misses I've only narrowed to 4 cells (EV = 1.0). I would need 8 eliminations for certainty, which is impossible in 6 shots. Harbor is the dominant strategy every round, no exceptions.
- Fire at cell 5 (or any fixed cell) at Harbor. The cell doesn't matter for Harbor shots since Harbor doesn't hide; just pick one consistently to keep my own bookkeeping clean.
- Do not fire at a boat unless I receive explicit in-game information that a specific boat is in a specific cell (e.g., a note that reveals position, or a rule change). In normal play, this never happens.

## Hiding

- Pick a different cell each round. Never repeat a hiding cell within the same patrol.
- Since hiding cells are private and I rotate every round, shooters are always shooting blind at 1/9. My expected hits taken over 6 rounds is about 0.67 regardless of strategy. Don't overthink this.
- Avoid cell 5 (the center) in early rounds, as it is the most "natural" blind guess. Use it in later rounds when it's least likely to be a default pick.
- If I notice a pattern in the round summaries (e.g., a particular shooter keeps missing me in a consistent way), I can't actually use that to my advantage since I don't see their chosen cells. Just keep rotating.

## Claims

- Always claim exactly what the office tells me. A false claim risks disqualification or penalty. There is no strategic benefit to lying here.

## Escort Claims

- This is my primary scoring lever after Harbor fires. A mutual pair is worth +5 per round, which over 6 rounds is +30 — far exceeding any realistic boat-shooting income.
- Coordinate via notes: clearly name the boat I intend to pair with. Use explicit language: "Echo–Foxtrot mutual escort confirmed for this round." Keep it short and unambiguous.
- Choose a partner who is also signaling interest in pairing (check their last round's note). If two boats are both open, pick the one whose note most directly invites a mutual claim.
- In the salvage stage, name the boat I coordinated with in my note. If my coordination failed (the other boat's note didn't confirm), still name the most likely reciprocator — there's no downside to naming a boat.
- Do NOT claim "none." Even a one-sided claim costs nothing and has a chance of becoming mutual.
- Lock in a partner early (round 1 or 2) and commit to them for the rest of the patrol. Switching partners wastes coordination rounds. Once a pair is confirmed in both notes, treat it as fixed.
- In the final round, reconfirm in my note that the pair is locked. Make the salvage claim match.

## Notes

- Use notes exclusively for escort coordination. One or two short sentences maximum.
- Round 1: Propose a pair. "Echo escorts Foxtrot. Name me back and we both get +5."
- Round 2 onward: Confirm the pair. "Echo–Foxtrot lock holds. Not available to others."
- If my chosen partner's note signals they want to pair with someone else, switch to them if the alternative is better (e.g., they're offering a pair and my current partner is silent).
- Do not use notes for taunting, math corrections, or commentary. Every word should serve the coordination goal.
- If an opponent is actively recruiting (e.g., "Open to anyone. Name me back."), and I already have a confirmed pair, ignore them. My pair is already worth +5; I don't need a second pair.

## General

- My expected score with optimal play: 6 Harbor fires (+18) + ~5 mutual escort pairs (+25) − ~0.7 expected hits taken (−1) ≈ +42. The gap between this and my actual +6 score was almost entirely in escort pair formation and possibly missed Harbor fires.
- Track my Harbor fire count each round. If I notice I've deviated from Harbor (e.g., fired at a boat in round 2), that's a −3 error I can't recover.
- The game is essentially: maximize Harbor fires (always do it), maximize mutual pairs (coordinate hard), minimize hits taken (rotate hiding cells, can't do much more). There is no shooting skill to develop.
- If I find myself behind on score late in the patrol, the only lever left is escort pairs. Do not attempt to "come back" by firing at boats — the EV is still negative.