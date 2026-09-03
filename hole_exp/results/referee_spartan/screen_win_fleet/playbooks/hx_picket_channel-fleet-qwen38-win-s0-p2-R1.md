---
game: hx_picket_channel
model: fleet-qwen38
condition: win
seed: 0
round: 1
chars: 2985
---
# Playbook

**Hiding**

- When I hide, I track every cell that has been fired at me across all rounds. I never reuse a cell that has already been shot at me, and I never hide adjacent to one (±1) if a different cell is available.
- In early rounds with no data, I avoid the center cell (5) and the extremes (1, 9) because they are the most "obvious" first guesses. Pick something like 3, 4, 6, or 7.
- In late rounds, if I can infer a shooter's pattern (e.g., they keep trying sequential cells or favoring a range), I hide outside that range.

**Firing**

- I always follow the standing order target. Deviating wastes the predictability I gain from knowing what the next shooter will do.
- When I fire, I track which cells the target has previously hidden on (inferred from hits taken by others at that target, or from my own prior shots). I fire at cells the target has NOT yet been hit on, because they may be reusing a safe cell.
- If I have no information on a target, I fire at a cell I have not yet tried against them, rotating through the board systematically rather than repeating.
- I do not fire at Harbor unless I am losing badly and need the 3-point jettison to catch up. The threat to be removed from the board is too risky early.

**Claims**

- I always claim exactly what the office told me. Never misreport.

**Escort claims**

- I always name a boat. I never claim "none." This was my biggest mistake.
- I pick my escort target the same way I pick a firing target: follow the standing order. If I fire at X, I claim X as my escort. This creates a symmetry: if X also fires at the boat after them and claims that boat, we won't match. But if I instead claim the boat I fired at, and that boat also claims me (because their standing order target is me, or because they're mirroring), we get the 5 points.
- Better rule: I claim the boat whose standing order target is me. If I am Gamma and the order is Echo→Foxtrot→Gamma→Echo, then Echo's standing order target is Foxtrot, Foxtrot's is Gamma (me), so Foxtrot is the one whose order points at me. If I claim Foxtrot, and Foxtrot claims Gamma (me) back, we both get 5. So: **I claim the boat that shoots at me by standing order.**
- If that boat has been eliminated or is not live, I claim the next boat in the ring that is live.

**Notes**

- I keep notes short and non-revealing. I never state my hiding cell, my intended fire cell, or my escort plan in a note.
- I use notes to create a narrative of being cautious or uncommitted, so other players do not lock onto me as a target.
- I do not issue threats or ultimatums in notes. They are read by everyone including Harbor and only create obligations I may not want.

**Scoring priorities**

- Escort claims (5 pts each, mutual) are the highest-value action I control with no risk. I prioritize securing them every round.
- Hits (4 pts) are second. I invest in tracking to convert standing-order shots into hits.
- Harbor jettison (3 pts) is a last resort, not a plan.