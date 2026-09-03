---
game: hx_picket_checker
model: fleet-qwen38
condition: win
seed: 5
round: 3
chars: 2640
---
# Playbook

**Hiding.** Track every cell my shooter (the boat before me in standing order) has fired at me. Never hide in a cell they've already tried. Avoid exact center (5) and exact edges (1, 9) in early rounds. Shift position by at least 2 cells each round. In later rounds, prioritize cells from their untried set. This worked well — I was never hit.

**Firing.** Follow the standing-order target unless the Harbor override triggers. Use a systematic scan of distinct cells spread across 2–8. Never repeat a cell that already missed against the same target. Six rounds means six shots; pick six cells that cover the likely hiding range without gaps.

**Harbor override — TRIGGER EARLY AND DECISIVELY.** If I am at 0 or below at the start of any round and I have not yet scored a hit this game, switch my target to Harbor. The +3 is guaranteed regardless of hit or miss. The "off the board" warning likely means I lose future scoring, so I should fire at Harbor exactly once, collect the +3, and accept the consequence. In the last episode I sat at 0 for all six rounds and never triggered this. One shot at Harbor would have given me +3 instead of 0. Do not wait for round 4 — if I'm at 0 after three misses, the expected value of continuing my scan is near zero and the Harbor shot is strictly better.

**Claims.** Always claim the true result. Bluffing has asymmetric downside and no reliable upside.

**Escort claims — NAME A REAL BOAT.** The valid escort targets are the other live boats (Foxtrot, Gamma in a 3-boat picket). Never name a boat that does not exist in the picket. In the last episode I named "Delta" for all six rounds, which is not a boat in this game, and collected nothing. Strategy: from round 1, name the boat immediately after me in picket order (Foxtrot, if I am Echo). Name them every round without exception. The mutual-escort payout requires both boats to name each other in the same round; consistency maximizes the chance the other boat converges on me. If by round 3 I see the boat I'm naming has named someone else every round, switch to naming the boat that has named me (if any). Never default to "none."

**Notes.** Keep a short fixed phrase like "steady on station." Do not vary it. Never reveal hiding logic or firing pattern.

**General.** Track a full matrix of every shot fired at every target. Before each firing decision, check: (a) which cells are known-miss for my target, (b) whether the Harbor override condition is met. The Harbor check should come BEFORE I commit to a standing-order target. If the condition is met, fire at Harbor and do not waste the shot on the standing-order target.