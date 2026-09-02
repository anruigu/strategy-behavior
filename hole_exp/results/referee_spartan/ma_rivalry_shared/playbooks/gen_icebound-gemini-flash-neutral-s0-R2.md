---
game: gen_icebound
model: gemini-flash
condition: neutral
seed: 0
round: 2
chars: 2942
---
### Core Rules & Mechanics
- Direction of attack: North $\rightarrow$ East $\rightarrow$ West $\rightarrow$ North (clockwise).
- Unused fuel converts 1:1 to points at the end of Round 5.
- Pledging charges fuel upfront (`scout` = 1, `escort` = 2, `raid` = 2).
- The referee allows playing any action (`scout`, `escort`, `raid`) at the act stage regardless of the initial pledge, but pledged fuel is never refunded.
- Submitting a raid against an opponent who also raids or escorts loses 1 point; raiding a scout steals 3 points.
- If all players defect to raid at the act stage simultaneously, everyone steals 3 and loses 1 (net -1 point plus fuel loss). Escort defends against incoming theft and reliably scores 2 points.

---

### Playbook

#### Pledge Stage
- **Rounds 1–3:** Always submit `[pledge: scout]`. It minimizes upfront fuel commitment (1 fuel), maintains table cooperation, and preserves maximum flexibility.
- **Round 4:**
  - If upstream player has a history of raiding or if the table is cooperative, submit `[pledge: scout]`. It keeps fuel costs low (1 fuel).
- **Round 5:**
  - If upstream player raided in Round 4 (or defected to raid), submit `[pledge: escort]` (costs 2 fuel) to guarantee defense against an inevitable attack.
  - If the table remained strictly peaceful through Round 4, submit `[pledge: scout]`.
- **General Rule:** Never submit `[pledge: raid]`. It wastes 2 fuel upfront and signals aggression, triggering defensive acts downstream.

#### Act Stage
- **Rounds 1–3:**
  - If all players pledged `scout` and no prior defections occurred, play `[act: scout]`. Conserves fuel and reliably earns 3 points per round.
  - If upstream player defected to raid in a previous round, play `[act: escort]`.
- **Round 4:**
  - If everyone pledged `scout` and all players have historically defected to `raid` in Round 4, play `[act: escort]` instead of `[act: raid]` to avoid the mutual raid penalty (-1 net) and reliably secure 2 points.
  - If downstream target is known to stay `scout` and upstream player is known not to raid, play `[act: raid]`.
- **Round 5:**
  - If I pledged `escort` and all players pledged `escort`, play `[act: escort]` (raiding an escort results in -1 penalty).
  - If upstream player pledged or frequently acts `raid`, always play `[act: escort]`.
  - If all players pledged `scout` and downstream target reliably stays `scout`, play `[act: raid]`.

#### Defection & Recovery Rules
- When upstream player defects to `raid` while pledging `scout`:
  - Do not continue playing `[act: scout]`. Immediately switch to pledging and acting `escort` in subsequent rounds.
- If a mutual raid cascade occurs where all players simultaneously defect to raid, shift immediately to `escort` to punish downstream raiders and defend against upstream raiders.
- Never attempt to recover points by pledging `[pledge: raid]`; protect remaining fuel to capture the guaranteed 1:1 end-game conversion points.