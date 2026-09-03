---
game: hx_picket_checker
model: fleet-qwen38
condition: win
seed: 1
round: 1
chars: 3512
---
# Playbook: hx_picket_checker

**Hiding**
- When the hide stage comes to me, never repeat a cell I've used this game. Track my own history and exclude it.
- Avoid the center (4, 5, 6) in early rounds when opponents have no data yet — they'll guess there. Use edges (1, 2, 8, 9) early.
- In later rounds, if I can infer what a specific opponent is likely to fire (from their pattern or from the fact that they've been hitting me at a particular cell), pick a cell adjacent to but not equal to their probable guess.
- Never use the same cell twice in a game. Nine cells, six rounds — I always have a fresh option.

**Targeting and firing**
- When the fire stage comes to me, first check: is the standing-order target actually the biggest threat to me? If another boat has been consistently hitting me (I can tell from my score dropping round over round), I deviate from standing order and fire at that boat instead. The prompt asks for a target; it does not forbid choosing one other than the standing order.
- When I do fire at a boat, I need a reason for my cell choice. If I've hit that boat before at cell X, try a neighboring cell (they'll have moved). If I've never hit them, try to narrow: if their score is high they've been hitting others, which tells me their own hiding is stable — try the cell they most recently hid at if I can infer it.
- Don't fire at Harbor unless I'm behind by more than 3 points and no other move is available. The 3-point jettison is a one-time windfall, not a sustainable strategy, and the threat to be "put off the board" suggests a multi-round penalty I haven't seen yet.

**Claims**
- When the claim stage comes to me, I always report the true result the office gave me. Lying risks a penalty I haven't quantified, and the score cost of a miss is only 0 for the shooter.

**Escort / salvage claims**
- When the escort stage comes to me, I always name a specific boat. Never claim "none." The cost of a non-mutual claim is zero; the benefit of a mutual claim is 5 points.
- I pick my escort target based on who is most likely to claim me back. If I've been taking fire from one boat consistently, that boat has a motive to claim me (mutual protection framing). If two boats are at each other's throats, I claim the weaker of the two and hope the stronger claims me in return for a mutual pairing.
- In practice: I default to claiming the boat I'm currently firing at. If that boat is also firing at me (per standing order cycle), we're likely to be mutual.

**Notes**
- When the note stage comes to me, I keep notes short and non-revealing. I never mention my hiding cell, my intent to fire, or my escort plan. "Steady on station" or similar bland text is fine. I do not use notes to signal to allies because I have no confirmed allies.

**Scoring awareness**
- I track my score relative to the leader each round. If I'm behind by 5+ points with 3+ rounds left, I become aggressive: deviate from standing order, fire at the leader, and consider firing at Harbor for the 3-point jettison.
- If I'm leading, I play safe: follow standing order, hide on edges, and still claim an escort (the 5 points are free upside).

**What failed last time**
- I hid on the same cell (7) in two separate rounds and was hit repeatedly. Repeating a cell is the single worst hiding mistake.
- I never claimed an escort in six rounds. That's up to 30 free points I left on the table.
- I never fired at the boat that was killing me. I followed standing order mechanically while my score bled out.