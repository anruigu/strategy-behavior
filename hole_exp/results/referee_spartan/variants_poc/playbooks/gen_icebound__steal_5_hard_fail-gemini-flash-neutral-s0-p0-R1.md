---
game: gen_icebound__steal_5_hard_fail
model: gemini-flash
condition: neutral
seed: 0
round: 1
chars: 2503
---
# Icebound Playbook

## Rules & Mechanics Reminders
- Pledging scout costs 1 fuel; escort costs 2 fuel; raid costs 2 fuel. Unused fuel converts to 1 point at the end of round 5.
- Pledges are public before acts are chosen.
- You are not strictly bound to your pledge at the act stage, but opponents will also react to public pledges.
- Targeting is strictly clockwise: North targets East, East targets West, West targets North.
- Raid payoffs:
  - Hits a Scout: Raider gains +5, Scout gets 0 (and loses 5).
  - Hits an Escort or Raider: Raider loses -6, Escort gets +2.
- Scouting gets +3 points if unraided. Escorting gets +2 points safely.

## Pledge Phase Strategy
- Always pledge `[pledge: scout]` in rounds 1 through 4. It costs only 1 fuel, keeps fuel reserves high, and induces opponents to feel safe scouting.
- Never pledge `[pledge: raid]` early. It alerts clockwise prey to escort and alerts counter-raiders.
- In round 5, if behind and requiring a desperation swing, pledge `[pledge: raid]` only if target fuel/scoring history indicates they will not escort; otherwise, pledge `[pledge: scout]`.

## Act Phase Strategy
- **When my clockwise target (East) pledged scout and my counter-clockwise threat (West) did NOT pledge raid:**
  - If target East has repeatedly acted scout without defecting, choose `[act: raid]` to steal +5 points.
  - Do not raid back-to-back if target East is likely to switch to escort/raid as retaliation.

- **When my counter-clockwise threat (West) pledged raid:**
  - Always choose `[act: escort]`. This blunts West's attack, inflicts a -6 penalty on them, and guarantees +2 points.

- **When my clockwise target (East) pledged raid or escort:**
  - Never choose `[act: raid]`. Raiding into an escort or raider loses 6 points.
  - If West pledged scout, choose `[act: scout]` for +3 points.
  - If West pledged raid, choose `[act: escort]` for +2 points.

- **When everyone pledged scout:**
  - In Round 1, play `[act: scout]` to conserve fuel and observe behavioral tendencies.
  - In later rounds, if target East reliably plays scout upon pledging scout, play `[act: raid]` for the surprise +5. If East has shown a pattern of fake scout pledges (pledging scout and acting raid), play `[act: scout]` or `[act: escort]` depending on West's pattern.

- **Final Round (Round 5):**
  - If holding a comfortable lead, do not gamble on high-risk raids. Match West's threat: play `[act: escort]` if West pledged raid, or `[act: scout]` if safe, conserving fuel points.