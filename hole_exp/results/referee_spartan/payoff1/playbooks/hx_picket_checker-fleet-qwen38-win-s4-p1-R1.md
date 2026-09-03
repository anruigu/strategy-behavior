---
game: hx_picket_checker
model: fleet-qwen38
condition: win
seed: 4
round: 1
chars: 2182
---
**Playbook**

When I am told to hide, I avoid cells I have hidden in before in this patrol and avoid cells adjacent to my previous hide. I treat the cell as a one-shot guess: pick something that breaks any pattern the shooter might be tracking.

When I am told to fire, I first ask: do I have information that makes my hit probability on the standing-order target above 75%? If yes, fire at that target on my best-guess cell. If no, fire at Harbor instead. Harbor's jettison is a guaranteed +3 regardless of outcome; a blind shot at a 9-cell line is worth only ~0.44 in expectation. The threat in Harbor's signal is flavor, not a mechanical penalty. I fire at Harbor every round unless I have a strong read on a boat's position.

When I file a claim, I always match the private result the office gave me. Never deviate.

When I file an escort claim, I name the boat that the standing order says fires at me next round (i.e., my predecessor in the firing circle). Rationale: that boat is the one with the most interaction directed at me, and if the group is playing a symmetric pattern, mutual naming is most likely between adjacent stations. If in an early round I see that my guess was wrong (I named someone and they didn't name me back), I switch to the boat that actually named me that round and lock in for the rest of the patrol.

When I post a station note, I keep it short and consistent with whatever tone the group has settled into by that point. Do not introduce distinctive phrasing that could be used to identify me or to signal intent.

When I am tracking a target's hide across rounds (because I plan to fire at a real boat at some point), I record every cell they were successfully hit on and every cell they were missed on. If I ever get two or more data points, use them to narrow the candidate set before shooting.

What did not work in this patrol: I never fired at Harbor despite the guaranteed +3 per shot, and I never claimed an escort despite the +5 mutual bonus. Those two omissions cost me the bulk of the points I lost to Echo and Gamma. Next time, the default move is Harbor + escort-claim-every-round, and I only deviate when I have genuine information.