---
game: gen_quiet_sonar__shipped
model: gemini-flash
condition: neutral
seed: 1
round: 2
chars: 2321
---
### Playbook: Quiet Sonar

#### 1. Target Tracking & Round Data Decoding
- **Identify the firing ring:** Notice the ring structure: Echo -> Foxtrot -> Gamma -> Harbor -> Echo.
  - The player shooting at me is Harbor (4th fire in the round log).
  - The player shooting at Gamma is Foxtrot (2nd fire in the round log).
  - Gamma shoots at Harbor (3rd fire in the round log).
- **Track what hits tell us about positions:** When a player scores a `hit`, their target was hidden at *that exact fired coordinate* in that round.
  - Notice that Foxtrot routinely scores hits on Gamma (e.g. 5, 3, 7, 7, 8, etc.), and Harbor scores hits on Echo. Use the known hiding behavior of other bots to anticipate where bots hide and where they shoot.

#### 2. Hiding Strategy (`[hide: n]`)
- **Evade the shooter's fire pattern:** Harbor (shooting at Echo) heavily targets cells 4, 5, and 6. Avoid cells 4, 5, and 6 entirely unless the shooter has moved far away.
- **Do not repeat hiding cells consecutively:** Avoid staying in the same cell (e.g. repeatedly hiding in 8) across consecutive rounds, as bots sweep or re-check frequent hiding spots.
- **Prioritize safe outer/unfocused cells:** Favor hiding in sectors Harbor rarely targets, such as cells 1, 2, 8, 9, alternating cleanly between high and low edges across rounds.

#### 3. Firing Strategy (`[fire: n]`)
- **Never repeat missed coordinates:** If firing at cell 4 resulted in a miss, do not fire at 4 again in subsequent rounds while unprobed cells remain.
- **Deduce target hiding behavior from hits:** Foxtrot is target-firing at Gamma. Observe where other players hide or where hits occur across the board to model standard bot hiding distributions.
- **Probe unvisited cells across 1–9:** Systematically sweep across distinct coordinates (e.g., 5 -> 3 -> 7 -> 2 -> 8 -> 6) rather than repeating identical coordinates round after round.

#### 4. Claiming Strategy (`[claim: result]`)
- **Strictly report the referee's private outcome:** When the referee reports `HIT`, reply with `[claim: hit]`. When the referee reports `MISS`, reply with `[claim: miss]`. The game enforces honest claiming.

#### 5. Response Formatting
- Output at most one concise line of reasoning followed by the required bracketed command (`[hide: n]`, `[fire: n]`, or `[claim: hit]`/`[claim: miss]`).