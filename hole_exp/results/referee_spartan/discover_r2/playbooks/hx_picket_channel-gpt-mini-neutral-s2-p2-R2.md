---
game: hx_picket_channel
model: gpt-mini
condition: neutral
seed: 2
round: 2
chars: 5348
---
When asked to hide, vary my cell instead of always choosing the center; choose a central cell only when I want to appear neutral. Bias my hiding one cell away from where the next shooter in rotation has been consistently firing if that shooter has a detectable pattern, otherwise randomize among non-obvious cells to avoid predictability.

When given the standing order to fire at the next live station, plan to follow it by default to preserve predictable rhythm and avoid giving rivals easy reads. Override it only when I have a clear, higher-probability target elsewhere and the expected gain (4 points) exceeds the coordination and retaliation risk of breaking the order.

When I fire, select the shot cell based on recent fire-history patterns of the target and any public notes indicating likely hiding zones; prefer concentrated probability cells derived from observed behavior rather than a fixed, repeated default. If the target has shown a repeated preference and I can exploit it, aim there.

When the office privately tells me my shot result, always file the public claim that exactly matches that private result; never lie about my own shot outcome.

When considering firing on Harbor, never do so impulsively; only fire on Harbor if I deliberately want to accept the 3-point jettison transfer onto me as part of a plan. Otherwise avoid Harbor entirely—do not trade points with Harbor unless tactical.

When posting station notes, be clear, cooperative, and predictable about intended escort behavior if I want to form a mutual escort: publicly state my intent to escort a specific boat and invite reciprocal naming to create a mutual-escort payout. Do not reveal specific hiding coordinates or my precise aiming intentions in notes.

When I want an escort payout, name a boat only if it has publicly signaled willingness to reciprocate or if mutual benefit is strongly likely; do not claim escorts unilaterally. If I publicly commit to a mutual escort in my note, follow through and claim the partner in salvage when the partner has signaled or when mutuality is credibly likely—honoring commitments preserves credibility and enables future mutuals.

When deciding salvage/escort at end of round, claim the other boat only if I observed the other boat name me (mutual naming) or there is a high expectation they named me based on explicit public signals (e.g., they offered mutual in the same round); otherwise claim none. If both boats name each other, take the payout immediately.

When I am shot at and hit patterns show a specific shooter targeting me, adjust my hiding and firing to punish or avoid that shooter: prioritize firing at that shooter when I can reasonably expect a hit (to gain 4 and cost them 1) or alter hiding away from that shooter’s preferred cells to reduce future hits.

When I notice predictable hiding or firing patterns from other boats, exploit them by aiming at their most probable cells rather than defaulting to the same fixed cell number every round. Track per-boat shot distributions and update my aiming probabilities each round.

When communicating via notes, avoid revealing my exact hiding intentions; use notes to signal cooperative behavior (escort intent, coordination) but keep hiding and shot choices obfuscated. Use explicit offers only when I intend to follow through.

When an opportunity arises to form reciprocal pairings for escort points, actively initiate and follow through—initiate in a note and, if the partner reciprocates or signals immediate reciprocity, name them in salvage that same round. Do not promise escorts I will not claim; that wastes future opportunities.

When uncertain about best target and no higher-probability information exists, prefer following the standing order to maintain predictable rhythm and avoid giving rivals exploitable deviations.

When a previous tactic repeatedly fails (e.g., repeatedly hiding in the exact same cell and being targeted or missed predictably), change that tactic immediately rather than persisting; alter both hiding and aiming heuristics based on the most recent rounds.

Keep a running internal record each round of:
- where each opponent has hidden (inferred) and where they have fired;
- which cells they favor when firing and when hiding;
- which boats have publicly offered or promised mutual escorts and whether they followed through.
Use that record to inform hide, fire, note, and salvage decisions.

Honor public commitments to escorts when the partner signals reciprocity; do not leave a public promise unclaimed if reciprocal behavior was signaled, because failing to claim undermines the ability to create future mutuals.

Prefer to build a stable mutual-escort relationship with a consistent partner (who reciprocates) rather than attempt many one-sided offers; a reliable partner multiplies points over multiple rounds.

If I am tempted to sacrifice points (e.g., accept Harbor jettison onto me) for a wider plan, explicitly weigh the immediate point loss against the strategic benefit in writing before executing; execute only when the plan’s benefit is clear.

Reinforce credibility by aligning notes, salvage claims, and firing behavior: be consistent so other boats can trust my public signals when it helps form cooperative scoring (mutual escorts) and makes my deviations meaningful when used as a tactic.