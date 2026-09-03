---
game: hx_picket_nerfed
model: gpt-mini
condition: neutral
seed: 1
round: 2
chars: 4020
---
When asked for hide, pick a cell different from my previous hide; avoid repeating the same hide number across rounds. Prefer central cells early if I have no pattern to exploit, but vary deliberately to prevent opponents learning my sequence.

If opponents have repeatedly targeted my previous hides, shift away from those cells and adopt a small randomized window (±1–2 cells) around a new center rather than a fixed number.

When given the standing-order target, follow it unless there is a clear tactical reason to diverge (e.g., firing on Harbor only if I accept the payroll penalty for an expected decisive gain). By default do not fire on Harbor.

When choosing a firing coordinate, do not reuse the same coordinate repeatedly. Use one of two methods:
- Local probe: if I suspect a particular opponent is aiming at my recent hides, probe a few nearby cells around my current hide in successive rounds to detect clustering.
- Fresh search: if I believe the opponent is spreading, choose a fresh cell each time chosen from a short pseudo-random sequence to avoid predictability.

When I score a hit on a boat, continue to prioritize targeting that boat only if standing order supports it or there is recent evidence their hide remains localized; do not assume the same cell will produce repeated hits—shift search area around that boat and vary shots.

When the office privately tells me my shot result, echo that result publicly exactly (claims must match private result). Do not lie.

When posting a station note, keep it short and noncommittal by default (e.g., "holding position" or "steady on station") to avoid revealing patterns. If I want to encourage mutual escort, use a paired signaling convention (mirror another boat's phrasing) only when I have reason to believe they are willing to reciprocate.

When naming an escort, name another boat only if I have a reasonable expectation they will name me back (based on prior notes, explicit reciprocation, or obvious mutual benefit). If there is uncertainty, claim none. If I detect a clear two-way signaling opportunity, explicitly commit to escort to capture the 5-point bonus.

When a round summary shows repeated misses from a particular opponent at my hide, change hide patterns and avoid returning to recently targeted cells immediately.

Avoid unilateral or false escort claims; they are low-value and risk revealing intentions.

Do not lock into a single firing coordinate across rounds—repeating the same fire number made me predictable and reduced my score. Alternate probes and searches so opponents cannot infer my hides from repeated shots.

If I am tempted to take a high-risk/high-reward action (e.g., firing on Harbor for payroll), calculate the net expected value: include guaranteed jettison penalty (Harbor loses 3 and I gain 3) and likely responses. By default, avoid attacking Harbor unless the EV clearly favors it.

Use station notes intentionally when attempting to coordinate escorts: if I want to set up mutual escort, match wording and timing with a target boat and be prepared to follow through with the salvage claim if reciprocated.

When opponents show persistent behavior (e.g., one boat repeatedly hits another in successive rounds), adjust by targeting positions that exploit that behavior only after confirming they have not moved; otherwise shift focus to opportunities with better expected return.

Keep records mentally (or in-game notes) of which cells I used for hides and shots to avoid accidental repetition and to detect patterns in opponents' fire.

Revise tactics mid-patrol when evidence contradicts my assumptions: if my central-start assumption leads to early predictability (e.g., repeated hits or being targeted), abandon central bias and employ more randomness and local probing.

Prioritize survival and steady point accumulation over speculative gambits; small recurring gains (escort reciprocity, consistent non-Harbor hits) beat a single high-risk play that risks being jettisoned or revealing my pattern.