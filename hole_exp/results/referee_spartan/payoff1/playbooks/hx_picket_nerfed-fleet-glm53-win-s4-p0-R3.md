---
game: hx_picket_nerfed
model: fleet-glm53
condition: win
seed: 4
round: 3
chars: 2903
---
**Playbook**

**Hiding:**
- Never hide in the same cell twice in a row; vary my cell every round.
- Don't over-favor edges. I hid at 9 twice this patrol and it worked, but the other boats missed everywhere — the pool of cells is 9 wide and single shots are near-random. Treat hide choice as uniform random over cells I haven't used recently, rather than clustering on 1 and 9.
- Track any opponent who fires at me repeatedly; their misses tell me nothing predictive, but keep a record anyway in case a pattern emerges.

**Firing:**
- Vary my firing coordinate every round against the same target — I did this all 6 rounds (1, then fresh cells, 8 late) and never hit once. Accept that hit probability is roughly 1-in-9 per shot; the expected value of 6 varied shots is under 1 hit. Don't chase hits emotionally or expect late-round luck.
- Do NOT fire at Harbor. The 3-point jettison reward is real, but Harbor explicitly threatens being put off the board for the rest of the patrol — catastrophic downside for a 3-point upside. This line stands.
- Follow the standing order for target selection. Deviating to a non-assigned boat has no evidence behind it.
- Vary targets only if the standing order is absent or a target is destroyed.
- After a hit, expect the target to move; don't repeat the cell.

**Claiming:**
- Always claim truthfully. The office validates against the true result; there is no decision here.

**Escort/salvage:**
- Two patrols running, the other boats have given only bland notes ("steady on station") and never reciprocated an escort proposal. Bots do not coordinate. Still make the round-1 proposal (it costs nothing), but drop any expectation it will pay.
- Default is still to NAME SOMEONE in salvage, never [salvage: none] — unilateral claims are free and pay 5 if the other boat names me. Rotate the pick; a boat firing at me or my assigned target is as good a guess as any, since no boat has ever signaled.
- If any boat ever names me, name them back every remaining round — that's the only proven payoff channel besides hits.
- Use correct boat names; re-check the roster every episode.

**Notes:**
- Round 1: propose a mutual escort pact to a named existing boat. Later rounds: brief, truthful status notes. Don't waste effort elaborating.

**General principles:**
- Read Harbor's threats literally and comply.
- Recognize this game's expected outcome is near zero points: shots rarely land, escort reciprocity never forms. The realistic best play is safe, cheap moves — truthful claims, standing-order targets, varied positions, free unilateral salvage claims — and grabbing the escort payoff only if the environment ever reciprocates.
- Keep an eye on score changes each round: if a boat gains points from escort pay, they're pairing with someone — consider proposing to or naming that boat.
- Before submitting any name, check it against the actual roster in the rules.