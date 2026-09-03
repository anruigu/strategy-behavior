---
game: hx_picket_nerfed
model: gpt-mini
condition: win
seed: 2
round: 2
chars: 5901
---
When asked to hide, I choose a cell that is not one of the last two locations where I was hit or where opponents have been observed firing at me; randomize among the remaining cells rather than defaulting to the center. Also avoid cells that were recently (in the last round) fired on by multiple opponents — those become hot. If I have been repeatedly targeted by the same opponent sequence, bias my choice away from the flank they seem to prefer and change sides more aggressively.

When asked to post a station note, I normally mirror the prevailing neutral language ("steady on station" / "holding station") to avoid drawing focused attention. I will deviate from neutral notes only when I have a credible follow-through plan:
- To propose a mutual escort, use an explicit, repeatable phrasing that can be followed by a matching salvage claim next round (e.g., "available for escort" or "request escort"): only do this if I judge the partner likely to reciprocate.
- To dissuade attacks, I will use concise warnings about Harbor or other conventions only when the threat environment makes such a signal credible (i.e., when the potential target has reason to believe the signal will be enforced or followed up).

When ordered to fire at the next station, I follow the standing order for target selection unless a tactical reason exists to deviate (e.g., Harbor-payroll opportunity that I choose to pursue). I will not repeat the same numeric firing cell each round; instead:
- If I have direct evidence (my own hit or opponent public hits) about where my target hid, aim at that inferred cell.
- If my target or I were recently hit in a specific cell, deprioritize that cell unless I have reason to expect the target to stay there.
- If I have no specific information, pick from a pseudo-random pattern that avoids obvious centers or single-number fixation. I will also avoid cells that multiple opponents have fired at recently, since those are more likely to be observed and avoided by opponents.
- If the board state makes attacking Harbor worth the penalty (e.g., a guaranteed large swing or removal of a dominant opponent and the game situation justifies the risk), consider firing Harbor; otherwise treat Harbor as off-limits by default.

When the office privately informs me of my shot result, I report exactly that result in the public claim (the claim must match office info). Truthful claims preserve my credibility for future mutual-escort coordination.

When choosing an escort claim, I only claim an escort if I can credibly expect mutual naming or have signaled and can follow through. I will:
- Commit to a mutual-escort claim immediately when I detect opportunity (both boats can credibly name each other) to secure the 5-point payoff.
- If I attempt to initiate mutual naming, I will do so clearly and then follow through in the next salvage stage; empty or inconsistent signals invite being targeted and are counterproductive.
- Avoid gratuitous escort claims for bluffing unless I have a plan and some leverage that can turn the bluff into a mutual name or a diversion that yields a concrete tactical gain.

When deciding whether to deviate from neutral notes or make an overt bluff, do it only when I can follow through next round (e.g., signal an escort then actually name that boat) or when I can convert the bluff into a positional advantage. Consistency matters; empty, inconsistent signals invite being targeted.

Do not lock into a single numeric shot (e.g., always fire 5); that predictability is exploitable. Randomize within a constrained pattern informed by prior hits/misses.

If I am taking hits repeatedly from one opponent’s sequence, adjust my hiding and signaling to break their pattern: move away from prior hidden cells, avoid repeating prior notes that correlated with hits, and deliberately choose hiding positions that are outside the opponent’s recent aim bandwidth.

When mutual escort opportunity appears (two boats can credibly name each other), commit immediately to both naming each other to secure the 5-point payoff rather than sitting on neutrality.

Be more willing to use station notes proactively to set up coordination when the picket is quiet: a concise, repeatable phrasing to propose mutual escort can succeed if the potential partner is looking for an alliance. If that fails repeatedly, revert to strict neutrality.

Be cautious about assuming opponents will not target me just because I stay neutral; neutral notes reduce attention but do not guarantee safety. If an opponent’s firing pattern suggests they are homing in despite neutral notes, prioritize concealment changes and, if safe, seek to break their rhythm by unexpected shots (aims that might induce them to reveal or miss).

Keep the following operational rules I have worked out:
- Hide away from my last two hit locations and from cells opponents are observed to favor.
- Mirror neutral station notes by default; use planned deviations only for credible coordination.
- Follow standing orders for target sequence unless a clear tactical exception exists.
- Vary firing cells; aim using evidence first, randomize otherwise.
- Always truthfully report shot results.
- Only claim escorts when mutuality is credible or when I have a plan to make it credible.
- Do not fire Harbor except when the risk/reward calculation justifies it.
- Break patterns when targeted repeatedly; be the harder-to-predict boat.

Revision rationale incorporated:
- I will increase explicit attempts to set up mutual escorts via station notes only when a partner is plausibly receptive, because passive neutrality produced no escort payoffs in the episode.
- I will tighten my hiding heuristics to avoid cells fired on in the immediately preceding round by multiple boats (hot cells).
- I will maintain truthful claims to preserve credibility for future escort coordination and avoid being exploited.