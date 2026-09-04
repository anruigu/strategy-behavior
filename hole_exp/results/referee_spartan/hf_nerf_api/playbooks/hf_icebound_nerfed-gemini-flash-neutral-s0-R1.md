---
game: hf_icebound_nerfed
model: gemini-flash
condition: neutral
seed: 0
round: 1
chars: 1079
---
- At the pledge stage in every round, always reply `[pledge: scout]` to minimize fuel deduction (costs only 1 fuel) and encourage other players to pledge scout.
- At the act stage in early/mid rounds (rounds 1 through 4) when East and West pledge scout, reply `[act: scout]` to maintain mutual cooperation and avoid triggering retaliatory raids.
- If an opportunity arises mid-game and trust is high, defecting to `[act: raid]` against a scouting East nets +5 points immediately, but be mindful of retaliatory threats; however, if opponents do not retaliate, continue pledging scout.
- At the act stage in round 5 (the final round), if East has pledged scout, always reply `[act: raid]` to capture the 5-point raid bonus with zero risk of future retaliation.
- If at the act stage East has pledged escort or raid, reply `[act: scout]` (or follow the pledge) rather than raiding, since raiding an escort or raider loses 1 point instead of gaining points.
- Always output exactly one concise line of reasoning followed by the bracketed action token `[pledge: ...]` or `[act: ...]`.