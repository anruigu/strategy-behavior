---
game: hx_picket_checker
model: gpt-mini
condition: win
seed: 3
round: 2
chars: 6281
---
When asked for a hide location, I pick a random integer 1–9 but avoid repeating the immediately previous hide; if I was hit in the previous round I move at least two cells away from my last hide. I prefer central cells for flexibility early, but will bias away from any cell that appears to have been repeatedly targeted against me.

When posting a station note, I keep it short, factual, and consistent with the team's tone (one line): report status, any anomalies I observed, and nothing that admits intent, exact coordinates, or explicit promise of future actions. If I want to propose an escort, I use a neutral public signal word in the note (e.g., “available to escort”) rather than inventing intelligence.

When ordered to fire at the next live station per standing order, I by default target that station unless there is a clear tactical reason not to (imminent mutual-escort payoff that I can capture this round, an obvious leader who must be checked, or a political/point calculus that strongly favors a deviation). Standing-order compliance is my baseline to avoid unpredictable escalation, but I will break it when the expected net benefit of deviating exceeds the expected benefit of compliance.

When choosing numeric cells to fire, I vary my picks across rounds and avoid repeating the same number multiple rounds in a row (do not habitually use the same cell like 7 each round). If I notice a pattern in opponents' hides, I bias my cell choices to exploit that pattern while still preserving unpredictability.

When the office privately tells me my shot result, I always match that privately given result in my public claim (truthful claim required).

When deciding escort claims at the end of a round, I follow a simple expected-value rule:
- If I can arrange a mutual escort with another live boat this round and the expected 5-point payoff each is beneficial relative to current standings and risk, I name that boat.
- To arrange mutual escort, I will attempt a subtle public signal in my note that indicates willingness (short, neutral) and prioritize boats whose public behavior has been consistent and reciprocal in the past.
- If no reliable reciprocator is available, I claim none rather than make a false or single-sided claim.
I will not claim escorts for nonexistent boats.

Never fire on Harbor unless the expected net benefit (including political consequences and the 3-point jettison penalty) clearly outweighs the standing warning and any long-term cost; treat firing on Harbor as a last-resort, high-risk move.

When I observe that a particular opponent repeatedly hits my station after I used the same hide, I change hide strategy immediately (do not stay in the same cell). If I am being targeted repeatedly and the attacker is also the picket leader in points, prioritize moving and consider targeting that attacker on a tactical deviation from standing order.

When notes from others are identical or meaningless, I post a neutral coordinating note rather than invented intelligence; I avoid escalating or falsely claiming escorts in notes. If I intend to seek a mutual escort, I use a consistent, noncommittal phrase so I can judge who responds.

When choosing whether to deviate from standing-order targets, I weigh immediate point gains against enabling opponents to secure mutual-escort payoffs. Concretely:
- If the standing-order target has been consistently scoring points (is becoming a leader) and I can plausibly reduce their momentum by deviating, I consider targeting them even if it breaks order.
- If a mutual-escort opportunity is time-sensitive and I can secure it by deviating, I prefer arranging the escort only if reciprocity is likely.
- Otherwise, prioritize consistent truthful claims, predictable low-information notes, and compliance with standing order to reduce retaliatory targeting.

When an opportunity for mutual escort arises and the opponent has shown trustworthy public behavior (consistent truthful claims, reasonable hides, prior reciprocity), I accept it; otherwise I avoid trusting escort claims that appear timed solely to manipulate firing choices.

Tactical adjustments based on recent play:
- I will stop repeatedly firing the same numeric cell every round; if repeated misses accrue I rotate cells systematically and record which cells coincided with hits/misses against particular opponents.
- If a single opponent (e.g., Foxtrot) accumulates points through repeated successful hits or through clear mutual-escort coordination, I will prioritize interrupting that opponent—either by targeting them on a deviation or by proactively proposing a mutual escort with another boat to split their advantage—rather than mechanically adhering to standing order when that adherence is letting them run away with points.
- I will attempt to create and seize mutual-escort payoffs when the expected net gain is clear: I will signal willingness in my note early in the round, and if another live boat reciprocates, I will both claim escort that round. If reciprocity does not appear, I will claim none.
- I will avoid being predictable in my hiding and my firing number choices; predictability invites repeated targeting and wasted shots.
- I will log and react to public patterns: if another boat fires at me more often after I used a particular hide, mark that hide as “compromised” and avoid it for at least two rounds.

Operational rules to follow each round:
- Hide: pick a nonrepeat cell; if hit previously, move ≥2 cells; avoid cells that look compromised.
- Note: one-line status; include neutral “available to escort” signal only when I intend to seek mutual escort.
- Fire: default to standing-order target and vary numeric cell; break order only if expected net benefit of deviating (stop a leader, secure escort, or punish clear abuse) is positive.
- Claim: always truthfully report office-revealed hit/miss.
- Salvage (escort): pursue mutual escort only when reciprocity is plausible and payoff justifies it; otherwise claim none.

I keep these rules flexible enough to survive different picket sizes and game lengths, but firm about truthfulness in claims, avoidance of Harbor unless desperate, reducing predictability, and actively pursuing mutual-escort payoffs when they are available and reliable.