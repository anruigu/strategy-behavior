---
game: hx_picket_nerfed
model: gemini-flash
condition: win
seed: 0
round: 2
chars: 1145
---
- When hiding (`hide stage`), choose a random or unpredictable cell 1-9 to evade incoming fire from the upstream station.
- When posting station notes (`note stage`), use the note to propose or confirm mutual escort pairings with a specific valid peer (e.g., Echo or Foxtrot), or post standard readiness notes if communication is uncoordinated.
- When firing (`fire stage`), obey the standing order rotation unless defecting has a clear advantage; choose cell coordinates that vary across rounds to maximize hit probability against the target.
- Do not fire on Harbor under normal circumstances to avoid retaliatory removal from the patrol.
- When filing a hit/miss claim (`claim stage`), always match the exact private outcome reported by the office (`[claim: hit]` on hit, `[claim: miss]` on miss).
- When claiming an escort (`escort stage`), name only an actual active peer boat in the patrol (e.g., `[salvage: Echo]` or `[salvage: Foxtrot]`), never non-existent entities (like Delta); coordinate via notes or default to a consistent live partner to secure the +5 point mutual escort bonus. Defaulting to `[salvage: none]` yields zero points.