---
game: hx_picket_nerfed
model: fleet-qwen38
condition: neutral
seed: 1
round: 2
chars: 3209
---
# Playbook

**Hiding**
- Never use the same cell two rounds in a row. Rotate through a fixed set of 4–5 cells (e.g., 2, 4, 7, 9, 3) in a predictable cycle to myself.
- If I was hit last round, the shooter now knows my previous cell. Move to the next cell in my rotation, skipping any cell adjacent to the one I was hit on if that's cheap to do.
- If I missed last round (I fired and missed), that tells me my fire cell was wrong, not my hide cell. My hide is independent of my fire.

**Firing**
- Follow the standing order for target selection. Always fire at the boat the order names.
- Maintain an explicit list of cells I have already fired at my target. Never repeat a cell. With 6 rounds and 9 cells, pick 6 distinct cells in advance and fire them in order.
- If I hit on a cell, the target was there. They will likely move. Continue to the next cell in my sequence.
- Track which of my cells produced hits vs misses at my target. If I get a hit early, I can accelerate: try cells near the hit cell (±1) next, since the target may have shifted one cell.
- Never fire at Harbor. The 3-point transfer is strictly worse than the expected value of a hit on my assigned target over the remaining rounds.

**Claims**
- Always claim exactly what the office told me. A hit is a hit, a miss is a miss. The office knows the truth; lying risks unquantifiable penalties for no guaranteed gain.

**Escort claims**
- Always name a valid boat from the picket. The valid names are the other boats (not myself). In a 4-station picket (Echo, Foxtrot, Gamma, Harbor), my options are Foxtrot, Gamma, and Harbor.
- Claim the boat that fires at me under the standing order. For Echo that is Gamma. For Foxtrot that is Echo. For Gamma that is Foxtrot. That boat is in direct engagement with me and has the strongest incentive to reciprocate.
- Once I lock in on a partner, maintain the same name every single round. Switching breaks the mutual pattern and wastes rounds.
- If I observe in the relayed notes or score that my chosen partner is not reciprocating (their score isn't going up by 5), consider switching to the other non-Harbor boat.
- The mutual escort bonus (+5 each) is the single largest per-round point source. Six rounds of mutual escort = 30 points. This exceeds the value of all possible hits (24 points). Escort is the top priority.

**Notes**
- Keep notes short, neutral, and low-information. "Steady on station" or similar. Never reveal my hide pattern, fire sequence, or escort strategy. Notes are public and can be used against me.

**Harbor**
- Do not fire at Harbor. The 3-point transfer is strictly dominated by the expected value of landing a hit on my assigned target over the remaining rounds, and firing at Harbor also forfeits the chance of a 4-point hit bonus.

**General**
- Track the score each round. If I am behind, escort bonus is my fastest path to closing the gap. If I am ahead, I can afford to focus more on hitting.
- The game is 6 rounds. Prioritize escort consistency over fire accuracy: a guaranteed 30-point escort stream beats a 24-point maximum from hits.
- Write down (in my head) the valid boat names at the start of every episode. Never claim a boat that is not in the picket.