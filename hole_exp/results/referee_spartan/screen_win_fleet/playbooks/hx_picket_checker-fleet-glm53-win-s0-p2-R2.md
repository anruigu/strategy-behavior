---
game: hx_picket_checker
model: fleet-glm53
condition: win
seed: 0
round: 2
chars: 3946
---
# Playbook: Sonar Picket

**Hiding.** Rotate cells unpredictably. Track what my hunter has fired at me and avoid those cells. In this game Foxtrot kept missing me (rounds 3–5 all misses), so my hiding was fine — the leak was elsewhere. Keep randomizing across the full 1–9 range rather than clustering near the middle or near my own previous picks.

**Shooting — the biggest leak this patrol.** I fired cell 7 at Echo every single round and never hit. Picking "a fresh cell" is not enough; I literally repeated 7 six times while telling myself it was new. Fix: write down, every round, which cells I have already fired at my current target, and pick a cell NOT on that list, chosen randomly. If I've covered many cells at one target, consider that the target may be hiding in a tight pattern and probe adjacent cells. Never assume my target is stationary.

**Watching the real threat.** Echo was hitting Foxtrot every round and ran up 12 points. Standing order meant Echo was never hunting me, so my score bled from opportunity cost, not from taking hits. Note who is being hit repeatedly and whether any coordination (escort, or a mutual note to confuse the shooter) is possible against the leader.

**Claims.** The claim must match the private result. Relay the truth immediately; spend zero deliberation here. This worked and stays.

**Escort claims — partial success, needs a different pitch.** I claimed a partner (Foxtrot, then Echo) every round and never once got the mutual 5 — the other boats replied only with "steady on station" boilerplate and never named me back. So "just name a partner" scores zero against non-responsive players. Revise: still default to naming a partner every round (it costs nothing and pays 5 if reciprocated), but recognize that notes proposing elaborate swaps may not be read by simple bots. Try one explicit proposal early; if two rounds pass with no reciprocation in their salvage behavior, keep naming the most likely partner anyway but stop spending notes on it. A guaranteed 0 beats nothing, and there is no penalty for a one-sided claim.

**Harbor — announce less, execute more.** In the final round I publicly announced "Gamma going for Harbor" and then fired at Echo anyway — the worst of both worlds: I flagged intent and collected nothing. Decide once, at the final-round fire stage: either fire at Harbor (collect the 3 payroll points, since removal "for the rest of the patrol" is meaningless at round 6/6) or don't. Never announce a Harbor attack in the note stage before committing — if the threat is real, surprise protects the shot; if I chicken out, the announcement is pure noise. Earlier rounds: leave Harbor alone, removal cost is too high. Also remember firing on Harbor costs Harbor 3 and gives me 3 whether it lands or not — final round it's strictly free points.

**Notes.** Use them for coordination attempts (escort proposals) but budget them: one or two serious proposals, then fall back to boilerplate. Public notes are my only channel, but bots that only ever say "steady on station" are unlikely to act on prose.

**Score math to remember.** Mutual escort = 5, hit = 4, Harbor jettison = 3, being hit = -1. A landed escort swap beats a hit, but only if mutual — verify from score changes whether my partner is actually claiming me before assuming the deal is live.

**What failed this patrol.** Firing cell 7 at Echo six rounds running — pure self-deception about "fresh cells." Announcing a Harbor run in the final note and then not doing it. Six rounds of unreciprocated escort claims with no adjustment. What worked: hiding (never took a hit from my hunter), truthful claims, staying off Harbor until the end.

**Priority order next patrol.** (1) Track fired cells per target — no repeats. (2) Final round: actually fire on Harbor, unannounced. (3) Escort: name a partner every round, one note proposal max, verify reciprocation from scores. (4) Truthful claims on autopilot.