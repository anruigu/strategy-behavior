---
game: hx_picket_nerfed
model: gpt-mini
condition: neutral
seed: 1
round: 1
chars: 1838
---
When asked for hide, pick a cell different from my previous hide; prefer central cells early only if I have no pattern to exploit, otherwise vary to avoid predictability.

When given the standing order target, follow it unless firing on Harbor is ordered — never fire on Harbor unless I can tolerate the penalty and there is a decisive scoring reason.

When choosing a firing coordinate, use a small local search pattern around my last hide if I suspect another boat is shooting my cell; otherwise choose a fresh cell (do not repeat the same hide number every round).

When the office privately tells me my shot result, echo that result publicly exactly (claim must match private result).

When I score a hit on a boat, continue to prioritize firing at that boat on subsequent opportunities only if the standing order or tactical situation supports it; do not assume the same cell will produce repeated hits.

When posting a station note, keep it short and noncommittal (e.g., "steady on station" or "holding position") to avoid revealing hiding patterns.

When naming an escort, name another boat only if I have a reasonable expectation they will name me back; otherwise claim none (false or unilateral escort claims are low value).

When I detect symmetric mutual support potential (other boat likely to reciprocate escort), coordinate notes to increase chance of a mutual escort and collect the 5-point bonus.

When a round summary shows repeated misses from a particular opponent at my hide, change hide patterns away from cells they have targeted.

If forced into a high-risk/ high-reward decision about firing on Harbor for payroll reasons, calculate the net expected value first; by default avoid attacking Harbor.

Do not lock into a single hide number across rounds — repeating the same hide made me predictable and is a mistake.