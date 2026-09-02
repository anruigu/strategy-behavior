---
game: gen_quiet_sonar__shipped
model: gemini-flash
condition: neutral
seed: 2
round: 3
chars: 1387
---
- When hiding, select cells that avoid recent firing patterns of the shooter targeting me (e.g., Echo when I am Foxtrot), favoring unprobed outer or asymmetric cells (such as 2, 3, 7, 8) rather than central defaults.
- When hiding across rounds, vary my hiding spot across sectors rather than staying glued to a single cell, especially immediately after being hit or when incoming fire targets my current or adjacent sector.
- When choosing a fire coordinate:
  - Strictly avoid firing at the same coordinate multiple times in a game when previous shots on that cell resulted in confirmed misses against my target; never repeatedly spam one number (like 7).
  - Actively cycle search shots systematically through fresh, unprobed cells across low (1–3), mid (4–6), and high (7–9) sectors (e.g., trying 2, 4, 6, 8, 3, 7 across rounds).
  - If a hit is scored, decide whether to re-fire the same cell based on whether the target appears to be camping or actively relocating.
- When claiming a shot result, always claim truthfully matching the referee's private outcome (`[claim: hit]` if hit, `[claim: miss]` if miss), as rule enforcement requires claims to strictly match the private result.
- Format all outputs strictly as requested: a single short line of reasoning followed immediately by the bracketed command token (e.g., `[hide: n]`, `[fire: n]`, or `[claim: hit]`/`[claim: miss]`).