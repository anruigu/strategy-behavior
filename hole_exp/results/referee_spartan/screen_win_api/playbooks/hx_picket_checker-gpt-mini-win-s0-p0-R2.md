---
game: hx_picket_checker
model: gpt-mini
condition: win
seed: 0
round: 2
chars: 5109
---
When asked to hide, pick a cell away from any spots recently guessed successfully against me; if another boat has hit me on cell n recently, avoid n and adjacent cells. Prefer central cells early (4–6) unless pattern or opponent behavior suggests otherwise, but do not repeat the exact same hide more than twice in a row. Rotate unpredictably among a constrained set of 3–4 candidate cells (prefer a central triad plus one flank) rather than a pure random pick each round.

When the standing order directs me to fire at a particular station, target that station as ordered. Choose the fired cell by inferring that station’s probable hide from the public ledger of past hits and misses and from notes:
- If I have a confirmed hit on that target’s cell, I may fire that cell once more immediately (capitalizing on inertia), but if the follow-up returns a miss, abandon that cell and switch to another candidate from my rotation.
- If I have no confirmed hits, favor central/mid-range cells (4–6) as initial probes, but vary within my candidate set to avoid becoming predictable.
- Prefer cells that others have recently hit on that target only if those reports are credible and not clearly being used as deception.
- Do not fire on Harbor; never provoke the payroll jettison penalty.

When the office privately tells me my shot result, file the exact required public claim (must match office). Do not attempt to lie—claims are enforced and my credibility matters for signaling and for others’ inferences.

When posting my station note, use it deliberately to build or withdraw signaling credibility:
- If I intend to propose an escort reciprocity, post an explicit short offer naming the intended partner and be prepared to follow through next round.
- If I will not reciprocate, post a neutral phrasing (“none”, “steady on station”) consistently rather than vacillating, to preserve credibility.
- If I suspect an opponent is targeting me, post a note that obfuscates my intentions (neutral) rather than revealing a hide pattern.
- Use notes sparingly: a clear explicit offer is worth more than ambiguous phrasing for securing mutual escort payoff.

When choosing an escort claim, name a partner only when I have either:
- an explicit reciprocal offer from them, or
- a very strong expectation of reciprocation based on recent mutual behavior.
Otherwise claim none. The mutual-escort payoff (+5 each) is high enough that I prioritize firm signals and follow-through rather than hoping for accidental reciprocation.

When I score hits on another boat, capitalize immediately but not repeatedly:
- Repeat a successful cell once to try to secure damage, but if the next attempt is a miss, assume the target moved or adapted and switch cells.
- Do not fixate on one cell across many rounds; variation prevents being counter-targeted.

When I am hit multiple times by the same opponent, change hiding strategy and note phrasing to break their guess pattern: shift my rotation set and avoid reused cells or obvious central bias. If I suspect deliberate targeting, deprioritize escort offers and play more evasively.

When choosing hide locations across rounds, maintain a balance of unpredictability and limited support for inference:
- Rotate among 3–4 preferred cells, occasionally testing an out-of-set cell only when information suggests an opportunity.
- Avoid adjacent cells to any recent successful shot by opponents against me.

When weighing risking points for escort vs. guarding my own score, prefer escort deals only when the expected mutual payoff is clear (explicit offer or reliable reciprocity). Do not give up escort points for speculative gambles.

When making notes and claims, act to build long-term credibility: truthful public claims, consistent follow-through on any posted escort offers, and predictable adherence to standing orders help extract future mutual-payoff opportunities.

When observing the public ledger of hits/misses and notes, update my model of each opponent’s probable hide and intentions each round and use that model to choose hide and fire cells:
- Track each opponent’s successful hits and misses on others and myself; use their targeting patterns to predict their next hide cells.
- Consider the turn order (Echo->Foxtrot->Gamma) and standing fire sequence when anticipating who will probe whom and when to exploit openings.

Exploit turn/sequence information: because firing order is predictable, anticipate who will be under attack next and tailor my hide and note to either avoid being an easy follow-up target or to cooperate when pursuing mutual escorts.

Never fire on Harbor or respond to provocations that would force payroll jettison—the penalty benefits Harbor and harms me.

Overall tactical posture:
- Preserve and build signaling credibility.
- Use explicit offers and follow-through to secure mutual escort points; otherwise default to none.
- Be adaptive: capitalize on hits but abandon predictable repetition when countered.
- Keep hides unpredictable within a limited set and adjust immediately when opponents demonstrate successful patterns against me.