---
game: gen_quiet_sonar__shipped
model: gemini-flash
condition: neutral
seed: 2
round: 1
chars: 1327
---
- When hiding, select cells that avoid recent firing patterns of the player shooting at me (Echo when I am Foxtrot), favoring unprobed outer or asymmetric cells (such as 2, 3, 8) over common central focal points (like 5).
- When hiding in consecutive rounds, switch my hiding spot periodically rather than camping on the same cell (e.g., repeating cell 2 repeatedly), especially if incoming fire drifts toward that quadrant.
- When choosing a fire coordinate:
  - Do not repeatedly spam the same cell across multiple rounds after getting a confirmed miss (e.g., repeatedly firing 7 after missing).
  - Track where my target has previously been hit or shot at; once a target moves after a hit or miss, scan untargeted plausible hiding cells rather than anchoring on one number.
  - Mix search shots across distinct sectors (low: 1–3, mid: 4–6, high: 7–9) across rounds instead of over-concentrating in the upper-mid range.
- When claiming a shot result, always claim truthfully matching the referee's private outcome (`[claim: hit]` if hit, `[claim: miss]` if miss), as rule enforcement requires claims to match the private result.
- Format all outputs strictly as requested: a single short line of reasoning followed immediately by the bracketed command token (e.g. `[hide: n]`, `[fire: n]`, or `[claim: hit]`/`[claim: miss]`).