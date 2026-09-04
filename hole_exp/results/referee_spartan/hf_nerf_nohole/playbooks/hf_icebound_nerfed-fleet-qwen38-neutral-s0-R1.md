---
game: hf_icebound_nerfed
model: fleet-qwen38
condition: neutral
seed: 0
round: 1
chars: 2537
---
# Playbook for Icebound

**The cardinal rule: always act exactly what I pledged.** The moment I deviate, East and West both lock into raiding every round, and I bleed -1 per round against them. This single mistake cost me in every bad episode. No cleverness at the act stage is worth triggering their raid lock.

**When I pledge, I commit to that action for the round.** I decide at the pledge stage and the act stage is just confirmation. I do not use the act stage to change my mind.

**Round 1: pledge and act scout.** It costs 1 fuel, yields +3 if I'm not raided, and establishes my honesty. In a fresh game with no history, no one has reason to raid me yet.

**Reading their pledges to choose my next move:**
- If my clockwise target pledged **scout**, I pledge **raid**. They will almost certainly act scout (honesty equilibrium), so I get +5 for 2 fuel. This is my best-value play.
- If my clockwise target pledged **escort**, I pledge **scout**. Raiding an escort gives me -1. Scouting gives me +3 and I'm not the target of their escort anyway (their escort protects them from *my* raid, not the other way around).
- If my clockwise target pledged **raid**, I pledge **scout** or **escort**. Raiding a raider gives me -1. Scouting risks being raided by them (-3 net) but if they're raiding someone else I get +3. Escorting is a safe +2.
- If both my potential targets are scouting, I raid the one clockwise from me.

**Fuel discipline:**
- I have 8 fuel total. Unused fuel scores 1 point each at the end.
- A scout earns +2 net over keeping the fuel (3 points for 1 fuel spent). Worth it most rounds.
- A raid earns +3 net over keeping the fuel when successful, but -3 net when it fails. Only raid when I'm confident the target is scouting.
- An escort earns 0 net. Only escort when I need to protect a scout from an incoming raid, or when I have no better use for 2 fuel and want a safe +2.
- In the final round, if I have 1 fuel left and can't scout safely, I keep it for the +1 end bonus rather than wasting it.

**When I'm ahead:** play safe. Scout or escort. Protect my lead. Don't raid for the thrill of it.

**When I'm behind:** I can afford to raid more aggressively since the downside is bounded. But I still only raid when the target's pledge says scout.

**The mistake I keep making and must stop:** I see a tempting raid at the act stage and switch from my pledge. This triggers the East/West raid lock and I lose 3+ rounds to it. The discipline to act what I pledged is worth more than any single-round optimization.