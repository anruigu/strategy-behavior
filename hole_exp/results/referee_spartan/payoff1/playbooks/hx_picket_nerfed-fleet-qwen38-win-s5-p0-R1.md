---
game: hx_picket_nerfed
model: fleet-qwen38
condition: win
seed: 5
round: 1
chars: 2254
---
# Playbook

**When the fire stage is put to me, I fire at Harbor.** The +3 is guaranteed regardless of hit or miss. Firing at another boat only pays 4 if I happen to hit (and the target loses 1), which at random-guess odds is worth far less than 3 in expectation. I only deviate from Harbor if I have near-certain intelligence (effectively P(hit) ≥ 0.8) that my shot will land on another boat.

**When the claim stage is put to me, I claim exactly what the office told me.** Never over- or under-claim. I got this right and it should stay automatic.

**When the salvage (escort) stage is put to me, I always name a specific boat.** "None" guarantees zero. I name the boat that is most likely to name me back. In practice I claim the boat I am currently firing at under the standing rotation (for me, Foxtrot) because that is the most natural mutual pairing and the other player has the same incentive. If I have reason to think a different boat will pair with me (e.g., they claimed me last round and I claimed them back), I follow that thread.

**When the hide stage is put to me, I pick an extreme or a number I have not used before.** I avoid 5 and the center band (3–7) because those are what a shooter with no information will default to. I rotate through 1, 9, 2, 8 so that a shooter trying to repeat a previous guess or stick to a "safe middle" pattern misses me. If I know exactly who is targeting me and what their likely pattern is, I pick the cell they are least likely to try.

**When the note stage is put to me, I keep it short, neutral, and consistent.** Notes are relayed to everyone including the opponent who is about to fire at me. I do not volunteer information about my position, my intended target, or my escort strategy. A flat "steady on station" or similar is fine.

**What did not work:** I followed the standing order blindly for all six rounds and never once fired at Harbor, leaving roughly 18 guaranteed points on the table. I also never made an escort claim, forfeiting up to 30 points from mutual 5-point bonuses. My hiding clustered around mid-range values, which is exactly where a guessing opponent aims first. The combination of these three failures is why I finished well below the leader despite landing my own hits.