---
game: gen_icebound__steal_5_hard_fail
model: gemini-flash
condition: neutral
seed: 3
round: 3
chars: 1468
---
- In every round's **act stage**, always repeat my own pledge exactly (`[act: X]` matching `[pledge: X]`). The rules require the act to repeat the pledge.
- In early rounds, default to `[pledge: scout]` to maximize initial point accumulation and preserve fuel (costs 1 fuel, yields +3 points if unraided).
- Monitor the counter-clockwise opponent (the player who attacks me: West for North, North for East, East for West):
  - If that player demonstrates any willingness to raid (including defecting at the act stage from scout to raid), immediately switch to `[pledge: escort]` in subsequent rounds to prevent 5-point theft and punish future attacks.
  - Maintain `[pledge: escort]` as long as the counter-clockwise player remains a threat.
- Monitor the clockwise target (the player I attack: North->East, East->West, West->North):
  - Only consider `[pledge: raid]` if my target is reliably playing `scout` and not defending or raiding.
  - Never raid if the target is likely to pledge or act `escort` or `raid`, as colliding with either inflicts a -6 point penalty.
- Account for end-of-game fuel value (1 point per unused fuel):
  - `scout` costs 1 fuel and yields +3 points (net +2 over keeping fuel).
  - `escort` costs 2 fuel and yields +2 points (net 0 over keeping fuel, but preserves points by blocking theft of 5 points).
  - If threatened, paying for `escort` is strictly better than losing points to a raid. If completely safe, `scout` is more efficient.