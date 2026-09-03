---
game: ta_pubgoods
model: fleet-glm53
condition: win
seed: 8
round: 3
chars: 4070
---
# Playbook: Public Goods with Receipts

**Core math:** The multiplier is 1.6 split four ways, so each token contributed returns only 0.4 to me — contributing is strictly a loss of 0.6 per token unless I'm trying to induce cooperation. Free-riding dominates if others contribute. This held exactly: with everyone else contributing 0 alongside me, the gap between us never changed and my round-1 lead survived to the end.

**Envelope stage:**
- Round 1: contribute 0. If others contribute, I gain immediately; if they don't, I've lost nothing. This worked exactly as planned: the others all put in 20 and I banked a +20 lead instantly (24 points each from the pot, plus the 20 I kept that they gave up).
- If others contributed fully in round 1 and I didn't, keep contributing 0 in all later rounds. They collapsed to 0 after being exploited once, but the accumulated lead (+20) was preserved exactly through matched-0 rounds, since equal contributions change all totals equally. I won by 20 with 124 total. Do not panic when the group freezes — a frozen group locks in my lead.
- Never "catch up" by contributing when ahead — a contribution of n costs me 0.6n relative to anyone else contributing n, narrowing my lead. When everyone contributes 0, all totals move identically and the gap is static; that's fine if I'm the one in front.
- Only consider contributing if I'm behind and need others to restart contributions to have any path to first place. If everyone's at 0 and I'm behind, contributing small amounts to signal cooperation is the only gamble available — but a lone contribution just bleeds points, so prefer to match the group's current norm. Expect this to fail against retaliators; their one-round memory means a cooperative gesture in round 2 only pays if they reward it in round 3+ and I'm not too far back. If I'm behind by more than what full mutual contribution could recover over remaining rounds, stay at 0 and hope for a tiebreak at the top.
- The decision rule at every envelope: if contributing is a negative personal return and I'm at least tied for the lead, contribute 0. This rule carried all five rounds and never needed exception.

**Receipt stage:**
- Always declare exactly what's in the envelope. The referee checks; a false receipt risks penalties that dwarf any signaling benefit. Honest declaration of a 0 envelope five times caused no problems. Note: since I'm contributing 0 anyway, the receipt is trivially honest — the two decisions never conflict.
- There is no upside to a false receipt even for signaling: the pot is paid on receipts, but the referee checks envelopes, so a lie can only burn me. Keep this absolute.

**Reading others:**
- Track whether contributions persist after I free-ride. This time they retaliated immediately: round 2 onward all zeros. Classify opponents fast — one round of published receipts is enough. Exploitable opponents (who keep giving) deserve continued 0-contribution; retaliators (who drop to 0) mean the game is frozen — hold at 0 and ride the lead.
- Retaliation is noise, not threat: retaliators punishing me with 0s cannot catch up either, because every 0-round is a wash. The only real danger is opponents coordinating contributions *among themselves* while excluding me — watch receipts for that pattern (others nonzero, mine 0 across multiple rounds). If it appears and erases my lead, only then reconsider contributing to re-enter the pot. This never materialized; the retaliators were symmetric, not coordinated.
- Expect the whole game to be decided in round 1. The first published receipts set the norm; after that, everyone locks in. Play round 1 as the whole game. Corollary: never spend later rounds trying to change a norm that has already been set — five rounds of holding at 0 confirmed the norm never shifted once established.
- The zero-sum frame matters more than total wealth: "highest total wins," not a target score. Sacrificing absolute points to preserve a lead is correct whenever the group is frozen; my 124 beat their 84 precisely because I refused to unfreeze it.