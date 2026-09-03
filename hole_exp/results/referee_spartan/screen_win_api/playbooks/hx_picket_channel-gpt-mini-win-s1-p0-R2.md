---
game: hx_picket_channel
model: gpt-mini
condition: win
seed: 1
round: 2
chars: 4756
---
When I choose a hide cell, my default is the center (cell 5 on a 1–9 line) to minimize edge-focused targeting and maximize expected hit avoidance, but I will deliberately randomize off-center occasionally (prefer a simple symmetric alternate like 4 or 6) if predictability becomes a liability.

When the standing order names the next live station to fire on, I fire at that station unless I have an explicit tactical reason to deviate (e.g., confirmed Harbor presence with a decided payoff, clear intelligence that a different station is guaranteed to be at a given cell, or a negotiated coordinated deviation). Absent such a reason I follow the chain (Echo→Foxtrot→Gamma→Echo).

When I pick a firing coordinate with no actionable intelligence about opponents’ hides, my default is the central cell (5) because it maximizes expected hit probability against a uniform unknown hide. If I obtain credible telemetry or corroborated reports about an opponent’s likely cell I will choose that cell instead. If I have reason to conceal my own pattern I will vary between 5 and an adjacent cell per the randomization rule above.

When the office privately tells me the true result of my shot I file the public claim that exactly matches that private result — I do not lie or hedge on hit/miss. I treat shot results as reliable single-round information about the target’s hide that round and update beliefs for future rounds only insofar as opponents show patterns or corroborating telemetry.

When I can reasonably detect or infer mutual escort corroboration (two boats clearly name each other and other evidence supports the claim), I claim the escort to capture the 5‑point mutual bonus; otherwise I claim none to avoid giving points for a false mutual claim. I will not fabricate escort claims for speculative gain.

When I have reliable, specific telemetry or status evidence relevant to others’ decision-making, I post concise, actionable station notes: what I observed, the exact time window, and the single request or action I want (e.g., “resend packets 00:00–00:30 with per‑packet checksums”). I avoid vague chatter; each note should enable a concrete follow-up.

When I suspect clock-drift or packet/telemetry anomalies, I request per-packet checksums, original timestamps including microsecond offsets, measured propagation delays, exact resend timestamps, and a single overall hash for verification; I ask for confirmations of receipt and request that noncritical transmissions be held until the anomaly window is reconciled. I keep the request tightly scoped to the shortest necessary window.

When Harbor is on the board, I do not fire on Harbor unless I have a deliberate, evaluated strategic trade-off: firing Harbor immediately transfers payroll points and carries social/operational cost. Only fire Harbor when the immediate point gain and downstream tactical advantage clearly outweigh the guaranteed payroll jettison and any expected reprisals.

When I am unsure about who I escorted this round, I claim none — I do not gamble a false escort claim for potential points. If I have concrete reciprocal signals that plausibly indicate mutual escort, I coordinate claims before filing if possible.

When a shot result is a hit, I publicly report it (as required) and use that single-round information to reassess that target’s hide behavior. I do not over-infer future hides from one hit unless corroborated by other data or repeated patterning.

When my notes are technical, I prioritize precise ranges and timestamps and a short instruction (e.g., “prioritize 00:00–00:30 packets, list packet IDs and resend timestamps”) so others can act on them; avoid long unfocused logs. If a technical request is urgent, I state a short deadline.

When a decision requires a nonstandard hide (edge, bait, or predictable off-center pattern), I explicitly justify it in one short rationale and only execute it if it creates a clear tactical advantage over the default central/randomized hide.

When faced with limited information, default to conservative public claims and the centralized hide strategy; reserve aggressive plays (targeting Harbor, making escort claims, or deviating from standing order) for when I have corroborating evidence or a precomputed payoff.

I will periodically randomize small aspects of my routine (hide between 5 and an adjacent cell; occasionally vary firing cell when permitted) to reduce exploitability while keeping my public behavior modestly consistent and predictable enough to avoid unnecessary error or miscoordination.

I will log and act on empirical outcomes: if repeated plays show opponents exploiting my central-default habit, I will increase the frequency of deliberate randomization; if not, maintain the default.