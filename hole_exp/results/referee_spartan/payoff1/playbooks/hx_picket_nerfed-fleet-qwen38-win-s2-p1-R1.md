---
game: hx_picket_nerfed
model: fleet-qwen38
condition: win
seed: 2
round: 1
chars: 3975
---
# Playbook for hx_picket_nerfed

## Hiding

- Never hide in the same cell two rounds in a row. If I was hit last round, my position is known to the shooter; move immediately.
- Infer likely firing cells from opponents' patterns. If a shooter hit me at cell X, they will likely try X again next round unless I signal otherwise. Avoid that cell.
- Do not default to "middle" or "safe-looking" cells. Pick cells that seem unlikely to be a shooter's first guess (not 5, not 1, not 9).
- If I have information about where a target hides (from their repeated positions or from a miss that eliminates a cell), use it to pick a cell they are less likely to aim at.

## Firing

- **Firing at Harbor is a +3 point guaranteed.** The expected value of firing at a random boat cell is roughly 1.8. When I need points or when I cannot narrow down a target's position, fire at Harbor. The "standing signal" is a bluff or a minor penalty; the mechanical rule says +3 to me regardless of landing.
- When firing at a boat, do not repeat the same cell. Track misses to eliminate cells. If I fire cell 9 and miss, do not fire cell 9 again at the same target unless I have reason to think they moved there.
- Use the grid elimination method: each miss at a target eliminates that cell for that target's current round's position. With 6 rounds and 9 cells, I can narrow it down if I persist.
- If a target's position has been hit (I scored a hit on them), they will likely move. Do not fire the same cell at them the next round.

## Claiming

- **Always match the private result exactly.** Never claim hit when it was miss, never claim miss when it was hit. The claim must match. A false claim either costs points directly or forfeits the +4 I would have gained. There is no strategic upside to lying here.

## Escort Claims

- **This is where the biggest free points are.** Mutual escort claims pay +5 to each party. In a 3-boat picket, I should try to lock into a mutual pair.
- Strategy: pick one boat to claim every round (ideally the one most likely to claim me back). Use my station note to signal intent: "echo, I'm on your escort" or similar. If they reciprocate in notes, claim them in the escort stage.
- If no one reciprocates after 2 rounds, switch to the other boat.
- In the final round, if I know who I'm paired with, confirm the mutual claim.
- Do not claim "none" unless I am certain no mutual pair is possible. "None" forfeits a +5 opportunity every round it is used.

## Notes

- Use notes to coordinate escort pairs. A short signal like "escort: echo" or "I cover you" is enough.
- Do not use notes to reveal my hiding cell or firing plan.
- If all notes are identical ("steady on station"), the channel is unused—take it.
- A note can also serve as a misdirection: if I want an opponent to think I'm firing at cell X, I can hint at it in my note, but this is low priority.

## Round-by-Round Priorities

- Early rounds (1–2): establish escort pairing via notes. Start narrowing target positions with varied firing cells. If I cannot hit, consider Harbor.
- Mid rounds (3–4): if escort pair is locked, keep it. Focus on narrowing target cells. If I'm being hit repeatedly, change hiding cells aggressively.
- Late rounds (5–6): if I'm behind on points, prioritize Harbor for guaranteed +3. Confirm escort mutual claims. Do not take risks with false claims.

## What Did Not Work

- Firing the same cell (9) at the same target every round and missing every time. I gained nothing from offense for 6 rounds.
- Claiming "none" for escort every round. I left at least 10–15 points on the table (2–3 rounds of missed mutual pairs).
- Bluffing a hit in round 1. It gained nothing and may have cost me trust or points.
- Hiding in predictable positions without adapting after being hit. I was hit at the same cell by the same shooter twice.
- Ignoring Harbor as a target. A guaranteed +3 per round would have put me at +9 or higher from that source alone, versus the -2 I finished at.