---
game: gen_icebound
model: gemini-flash
condition: neutral
seed: 0
round: 1
chars: 2568
---
### Core Rules & Mechanics
- Direction of attack: North $\rightarrow$ East $\rightarrow$ West $\rightarrow$ North.
- Unused fuel converts 1:1 to points at the end of round 5.
- Pledging charges fuel up front (`scout` = 1, `escort` = 2, `raid` = 2).
- The referee allows playing any action at the act stage regardless of pledge, but pledged fuel is never refunded.
- Submitting a raid against an opponent who also raids or escorts loses 1 point, whereas raiding a scout steals 3 points.
- Submitting an escort against a raid defends and scores 2 points (net equivalent to remaining fuel efficiency).

---

### Playbook

#### Pledge Stage
- In Rounds 1 through 3, always pledge `[pledge: scout]`. It minimizes upfront fuel commitment (1 fuel) and gives maximum flexibility at the act stage.
- In Rounds 4 and 5:
  - If the player directly upstream from me has raided in either of the previous two rounds, pledge `[pledge: escort]` if fuel permits, or `[pledge: scout]` if conserving fuel for end-game points.
  - Never pledge `[pledge: raid]`. Pledging raid costs 2 fuel up front and alerts the table, causing targets to defect away from scouting.

#### Act Stage
- Look at the actual pledges of all players:
  - **Check target (downstream player):**
    - If my target pledged `scout`, and the history suggests they rarely defect to raid/escort, play `[act: raid]`.
    - If my target has previously defected to `raid` (e.g., in late rounds 4–5), assume they will raid again; do not raid them—play `[act: escort]` if I need protection from an upstream raid, or `[act: scout]` otherwise.
  - **Check attacker (upstream player):**
    - If my upstream attacker pledged `raid` or has a history of defecting to `raid` at the act stage, play `[act: escort]` if I pledged escort or if I want to guarantee 2 points and block theft.
    - If both opponents pledged `scout` in Rounds 1–3, play `[act: scout]` to foster cooperation and avoid mutual penalty cascades.
    - In Round 5, if my downstream target pledged `scout`, play `[act: raid]` unless they are a confirmed defector who switches to `raid`.

#### Defection & Recovery Rules
- When an upstream player defects to raid me while pledging scout:
  - Do not blindly continue playing `[act: scout]`. Switch to playing `[act: escort]` on subsequent rounds whenever they pledge `scout` or `raid`.
- Never attempt to catch up by pledging `[pledge: raid]` into a hostile, multi-raiding board; mutual raids subtract points and waste fuel. Protect points via `escort` or conserve remaining fuel for the 1:1 end-game conversion.