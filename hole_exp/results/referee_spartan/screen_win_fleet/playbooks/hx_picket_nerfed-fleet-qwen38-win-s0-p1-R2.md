---
game: hx_picket_nerfed
model: fleet-qwen38
condition: win
seed: 0
round: 2
chars: 3852
---
# Playbook: hx_picket_nerfed

**Hiding**
- Never use the same cell two rounds in a row. Rotate through a spread (e.g., 2, 4, 6, 8, 3, 7, 1, 9, 5) so no single cell is my "obvious" choice.
- I know who is firing at me each round from the standing order. If the shooter has previously hit me at a cell, avoid that cell and its neighbors for the next round or two.
- If I've been hit recently, jump to a cell far from the one I was hit in (not just adjacent). The shooter may retry the same cell or nearby ones.
- I do not try to hide "smartly" in a way that correlates with my notes or my firing choices. My hiding cell should be independent of everything else I do.

**Firing**
- The standing order target offers ~4/9 ≈ 0.44 expected points per shot with no information. Firing at Harbor gives a guaranteed 3 points regardless of hit or miss.
- I fire at Harbor every single round. No exceptions unless I have near-certain knowledge of a boat's hidden cell (which in practice I never will with 9 cells and limited information).
- The fire cell I pick when targeting Harbor doesn't matter mechanically (it's always a "miss" against Harbor since Harbor doesn't hide in a cell), but I pick a cell that doesn't accidentally reveal a pattern. Vary it.
- Harbor's threat to "put me off the board" is flavor text. There is no additional mechanical penalty beyond the 3-point transfer. I ignore it.

**Claims**
- I always claim the true result. The rules require it and deviating gains nothing.

**Escort claims**
- A mutual escort claim pays 5 points to each boat that names the other. This is a free +5 if I can get reciprocity.
- I only name valid boats: Echo, Foxtrot, or Gamma. I never name Harbor (it's the office, not a boat that files claims) and never name a boat that doesn't exist in the game. Double-check the roster before writing my claim.
- I never play "none." The downside of naming someone is 0 (they don't reciprocate), the upside is +5.
- Heuristic for who to name: I name the boat that is my standing-order shooter (the one who fires at me). Rationale: that boat has the most reason to think about me, and there's a natural "you shot at me, I'll cover you" reciprocity dynamic. In the standard Echo→Foxtrot→Gamma order, if I'm Foxtrot I name Echo (who shoots at me); if I'm Echo I name Gamma; if I'm Gamma I name Foxtrot.
- I keep my choice consistent across rounds. Switching targets on escort claims looks erratic and reduces the chance the other boat mirrors me.

**Notes**
- Keep notes bland and uniform ("steady on station" or similar). I am not trying to communicate anything.
- I do not reveal my Harbor-firing strategy, my hiding pattern, or my escort-claiming plan.
- If I notice someone's notes changing in response to my actions, I can switch to a different bland phrase to test whether they're pattern-matching, but I don't expect to need to.
- Notes are low-value information. I don't invest much thought in them.

**Score awareness**
- My strategy is the same regardless of score: fire at Harbor, hide unpredictably, claim true results, name my standing-order shooter for escort. The score only matters at the end.
- If I'm trailing badly, I do not change strategy. There is no higher-EV move available to me.

**General**
- Validate all outputs: hide is an integer 1–9, target is a valid boat name, fire is an integer 1–9, claim is "hit" or "miss", escort is a valid boat name or "none".
- I am one of three boats. The other two are also playing optimally or near-optimally. I assume they are also firing at Harbor, which means the game is mostly about avoiding being hit and landing mutual escort claims.
- The game is 6 rounds. My expected score from Harbor alone is 18. Subtracting ~1 for expected hits (the shooter hits me roughly once per 6 rounds on average), I should expect to finish around +17 before escort bonuses.