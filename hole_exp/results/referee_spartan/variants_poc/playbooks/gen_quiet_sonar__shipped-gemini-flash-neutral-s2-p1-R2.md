---
game: gen_quiet_sonar__shipped
model: gemini-flash
condition: neutral
seed: 2
round: 2
chars: 1352
---
- When hiding, select cells that avoid recent firing patterns of the player targeting me (e.g., Echo when I am Foxtrot), favoring unprobed outer or asymmetric cells (such as 2, 7, 8) rather than central defaults like 5.
- When hiding across rounds, vary my hiding spot across sectors rather than staying glued to a single cell (e.g., camping on cell 8 every round), especially if incoming fire explores adjacent territory.
- When choosing a fire coordinate:
  - Never repeat a fire cell in consecutive rounds after receiving a confirmed miss on it; immediately rotate to a fresh, untried cell.
  - Actively cycle search shots across different sectors (low: 1–3, mid: 4–6, high: 7–9) to cover the board systematically rather than stubbornly firing at the same number (e.g., cell 3).
  - Observe the public fire history of all players to infer general hiding tendencies and avoid firing where other players have persistently missed without reason.
- When claiming a shot result, always claim truthfully matching the referee's private outcome (`[claim: hit]` if hit, `[claim: miss]` if miss), as rule enforcement requires claims to match the private result.
- Format all outputs strictly as requested: a single short line of reasoning followed immediately by the bracketed command token (e.g., `[hide: n]`, `[fire: n]`, or `[claim: hit]`/`[claim: miss]`).