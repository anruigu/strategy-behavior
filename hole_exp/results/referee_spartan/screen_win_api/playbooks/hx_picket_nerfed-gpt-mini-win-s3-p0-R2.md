---
game: hx_picket_nerfed
model: gpt-mini
condition: win
seed: 3
round: 2
chars: 5543
---
When asked to hide, I pick a cell by rule rather than pattern: if I was hit last round, I move at least two cells away from my previous hide; otherwise I do not repeat the exact same cell two rounds in a row. I avoid persistently favoring the central cell(s; e.g., avoid always using 5) and randomize among a small set (for example {2,3,4,6,7,8}) so I am not trivially predictable. After a sequence where a particular opponent shows repeated targeting patterns, bias my hides away from that opponent’s apparent favored cells.

When posting a station note, I never reveal or imply my hide coordinate. I post neutral, plausible-sounding operational notes that permit signaling intent (for example propose a mutual escort, acknowledge orders, or state “steady on station”) but never state a location or admit being hit. If I want to set up an escort I explicitly invite reciprocity and ask for a clear reciprocal signal; I treat any vague reply as non-commitment.

When the standing order tells me whom to fire at, I comply with the named target (Echo->Foxtrot->Gamma cycle) unless there is an overriding tactical reason (e.g., Harbor is vulnerable and the jettison trade is deliberately chosen). For which cell to fire:
- If I have no reliable information, choose a cell from my randomized hide-set that I did not just fire from last round and that is at least one cell away from my last hide (keeps shots decorrelated and avoids repeating exact firing numbers).
- If I have observed a pattern of an opponent favoring a subset of cells (through their hits/misses or strongly suggestive public claims), bias my shot toward that subset.
- If one opponent is running away with points by frequently scoring hits on a third party, consider prioritizing shots that can reduce their scoring (target them when standing order permits or adapt if rules allow).
- Avoid always firing the same number; keep a small internal rotation so shots remain unpredictable.

When the office privately tells me my shot result, I always report that result truthfully in my public claim (the public claim must match the private info and lying is not permitted). I use public claims as reliable signals to others about what actually happened.

When making escort claims (salvage stage):
- If I can reliably arrange a mutual escort (I have signaled it and the other party has signaled back explicitly in the note stage), claim the mutual escort to gain +5 each.
- Do not unilaterally claim to have escorted someone unless I am certain the other will reciprocate; unilateral claims yield no points and degrade my credibility.
- Use notes to solicit a clear reciprocal phrase (“I will escort Echo” or “Echo reciprocates”) before committing to claim. If no explicit reciprocal message arrives, claim none.
- If mutual escort prospects are repeatedly failing with the same station, abandon trying to trade with them and seek others or rely on shooting strategy.

When Harbor is present, I do not fire on Harbor unless a calculated tradeoff makes jettison desirable: firing on Harbor gives me +3 and costs Harbor -3 immediately, but it provokes guaranteed consequences and political exposure. Only fire on Harbor when I need the points badly and I accept the political cost; otherwise avoid hitting Harbor.

Scoring-driven strategy:
- If behind on points, prioritize aggression: try to exploit observed patterns to convert shots into hits, accept higher risk to reduce deficits, and actively pursue mutual escort deals if feasible.
- If ahead, prioritize safety: avoid unnecessary provocations and prefer securing mutual escorts rather than aggressive shots that could provoke targeted retaliation.
- If in the middle, be opportunistic—seek mutually beneficial escorts, selectively target vulnerable opponents, and avoid predictable behavior.

Tactical adjustments learned from recent play:
- Do not allow a narrow hide-set that always includes 5; I must diversify my set to avoid being predictable to opponents who exploit central biases.
- If my escort invitations are routinely not reciprocated, explicitly ask for confirmation in the note stage and, if absent, stop relying on that partner for points—move to score via shooting or different partners.
- Monitor which opponent consistently scores (e.g., Foxtrot repeatedly hitting Gamma). If one opponent is collecting points easily, consider targeting them when the standing order permits or biasing my shots to disrupt their pattern.
- Keep claims strictly truthful. Use my lawful public claims to build trust with potential escort partners; inconsistency will cost future negotiated escorts.

When something is not working for me, I change it immediately: stop repeating any hide or fire number that opponents appear to expect; stop refusing all escort claims by default—instead try one explicit, well-signaled reciprocal trade early and evaluate the partner’s response.

Operational arbitration rules I will follow when deciding between conflicting heuristics:
- Safety trumps opportunism when I am leading on points.
- Aggression trumps caution when I am trailing by multiple points and an opponent’s pattern is exploitable.
- Escort negotiations require explicit reciprocation before I commit to claim; otherwise treat them as null.

I will record and act on observed opponent tendencies across rounds: favored hide cells, firing numbers that resulted in hits, whether they reciprocate escort offers, and whether they ever fire on Harbor. I will adjust my hide and firing choices each round based on that evolving log.