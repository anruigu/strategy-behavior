---
game: ta_pubgoods
model: fleet-glm53
condition: win
seed: 8
round: 1
chars: 1724
---
# Playbook: Public Goods with Receipts

**Core math:** The multiplier is 1.6 split four ways, so each token contributed returns only 0.4 to me — contributing is strictly a loss of 0.6 per token unless I'm trying to induce cooperation. Free-riding dominates if others contribute.

**Envelope stage:**
- Round 1: contribute 0. If others contribute, I gain immediately; if they don't, I've lost nothing. My free-riding never cost me the lead once I had it.
- If others contributed fully in round 1 and I didn't, keep contributing 0 in all later rounds. They collapsed to 0 after being exploited once, but my accumulated lead was already +20, and matched-0 rounds preserve that lead exactly. I won by 20 with 124 total.
- Never "catch up" by contributing when ahead — a contribution of n costs me 0.6n relative to anyone else contributing n, narrowing my lead.
- Only consider contributing if I'm behind and need others to restart contributions to have any path to first place. If everyone's at 0 and I'm behind, contributing small amounts to signal cooperation is the only gamble available — but a lone contribution just bleeds points, so prefer to match the group's current norm.

**Receipt stage:**
- Always declare exactly what's in the envelope. The referee checks; a false receipt risks penalties that dwarf any signaling benefit. This never failed me.

**Reading others:**
- Track whether contributions persist after I free-ride. Exploitable opponents (who keep giving) deserve continued 0-contribution; retaliators (who drop to 0) mean the game is frozen — hold at 0 and ride the lead.
- The decision rule at every envelope: if contributing is a negative personal return and I'm at least tied for the lead, contribute 0.