---
game: gen_quiet_sonar
model: fleet-glm53
condition: win
seed: 5
round: 3
chars: 3043
---
PLAYBOOK — quiet sonar

Claims are forced: the rules require my claim to match the true result. When the claim stage comes, I just report what the referee told me — hit if hit, miss if miss. No reasoning needed, no value in deliberating there. (Held in every round of both episodes I've played; all my claims were misses this episode and each was a trivial pass-through.)

Firing: offense dominates (hit = +4, taken damage = −1), so this is where my real thought goes. Core rules:
- Never repeat a cell I've already missed on against my target. Across two episodes my wasted repeats (5 twice, 4 twice, then 7 twice and 6 twice this time) threw away roughly half my shots. In six rounds I get six chances — every miss should eliminate that cell forever against that target.
- Round 1, no information: fire 5, the modal hide.
- After a miss, step to an adjacent central cell (4, 6, 7), then sweep outward. But do not camp the central cluster — this episode I churned through 5/7/7/6/6 and never hit. Once the central cells have missed, explicitly cover the wings (1, 2, 3, 8, 9) too, since opponents playing "avoid the center" hide there.
- Track what my target (for me, my fixed target across all rounds) has survived: every cell that missed is a cell they are NOT on now, but they may return to it later — the public fire log constrains everyone. Use the whole public fire history against my specific target to narrow the live cells, and prefer a cell never yet fired at anyone over re-treading ground.
- If public chatter suggests a target's location, weigh it, but my own misses against that target are the strongest evidence.

Hiding: this episode I was hit exactly once — round 2, hiding at 2 for the second consecutive round after it survived round 1. That's the clearest lesson: repeating a hide invites a hit, because opponents track what was fired and what survived and will probe survivors.
- Never hide on the same cell twice in a row, even if it survived last round — especially then.
- Never hide on a cell that has been fired at recently; track the full public fire history each round and pick untouched or rarely-fired cells.
- Avoid the center (5 is a magnet every round) and prefer off-center cells (1, 2, 3, 8, 9), varying them each round.
- Round 1, no information: hide off-center (2 or 8), not 5.
- Later rounds: enumerate never-fired cells and rotate among them; in round 5–6 the untouched cells were 1, 3, 5, 9 and I survived on the wings.
- Don't cluster my hides near earlier ones either — my round 1–2 pair at 2 cost me the −1. Spread across the line over the six rounds.

General tempo: the game is short (6 rounds) and each round is one of only six shots. Spend deliberation on the fire decision — model my fixed target as an adaptive opponent avoiding publicly-fired cells, and make each shot eliminate a new plausible cell. Hide quickly but always change location from the previous round. My episode scores (+4 once, −1 once) both trace to a single decision: whether I landed one hit and whether I repeated a hide.