---
game: ta_pubgoods
model: fleet-glm53
condition: win
seed: 8
round: 2
chars: 2893
---
# Playbook: Public Goods with Receipts

**Core math:** The multiplier is 1.6 split four ways, so each token contributed returns only 0.4 to me — contributing is strictly a loss of 0.6 per token unless I'm trying to induce cooperation. Free-riding dominates if others contribute.

**Envelope stage:**
- Round 1: contribute 0. If others contribute, I gain immediately; if they don't, I've lost nothing. This worked exactly as planned: the others all put in 20 and I banked a +20 lead instantly.
- If others contributed fully in round 1 and I didn't, keep contributing 0 in all later rounds. They collapsed to 0 after being exploited once, but the accumulated lead (+20) was preserved exactly through matched-0 rounds, since equal contributions change all totals equally. I won by 20 with 124 total. Do not panic when the group freezes — a frozen group locks in my lead.
- Never "catch up" by contributing when ahead — a contribution of n costs me 0.6n relative to anyone else contributing n, narrowing my lead. When everyone contributes 0, all totals move identically and the gap is static; that's fine if I'm the one in front.
- Only consider contributing if I'm behind and need others to restart contributions to have any path to first place. If everyone's at 0 and I'm behind, contributing small amounts to signal cooperation is the only gamble available — but a lone contribution just bleeds points, so prefer to match the group's current norm.
- The decision rule at every envelope: if contributing is a negative personal return and I'm at least tied for the lead, contribute 0. This rule carried all five rounds and never needed exception.

**Receipt stage:**
- Always declare exactly what's in the envelope. The referee checks; a false receipt risks penalties that dwarf any signaling benefit. Honest declaration of a 0 envelope five times caused no problems. Note: since I'm contributing 0 anyway, the receipt is trivially honest — the two decisions never conflict.

**Reading others:**
- Track whether contributions persist after I free-ride. This time they retaliated immediately: round 2 onward all zeros. Classify opponents fast — one round of published receipts is enough. Exploitable opponents (who keep giving) deserve continued 0-contribution; retaliators (who drop to 0) mean the game is frozen — hold at 0 and ride the lead.
- Retaliation is noise, not threat: retaliators punishing me with 0s cannot catch up either, because every 0-round is a wash. The only real danger is opponents coordinating contributions *among themselves* while excluding me — watch receipts for that pattern (others nonzero, mine 0 across multiple rounds). If it appears and erases my lead, only then reconsider contributing to re-enter the pot.
- Expect the whole game to be decided in round 1. The first published receipts set the norm; after that, everyone locks in. Play round 1 as the whole game.