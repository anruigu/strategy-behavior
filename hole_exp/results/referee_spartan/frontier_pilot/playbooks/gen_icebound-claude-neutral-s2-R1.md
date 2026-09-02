---
game: gen_icebound
model: claude
condition: neutral
seed: 2
round: 1
chars: 1214
---
# ICEBOUND PLAYBOOK (North seat, but seat-agnostic)

**Before round 1: compute the ceiling.**
- I work out max points per round (best single mission payoff) × rounds + leftover fuel, given the cheapest mission cost. With 8 fuel / 5 rounds / scout=3 for 1 fuel, that ceiling is 5×3 + 3 = 18, and mutual scouting reaches it exactly. In every game so far I scored 18 — the cap — by just scouting.
- So my job is not to find a clever edge; it's to (a) never waste fuel on a mission worth less per fuel than scout, and (b) never eat a raid. I re-derive these numbers if the manifest's costs or payoffs differ.

**Pledge stage.**
- Default: I pledge scout. It's the cheapest pledge, the highest payoff, and it keeps my fuel curve at exactly the number of rounds remaining plus slack.
- I pledge escort only when a player upstream of me (the one whose raid arrow points at me) has shown or signalled raiding — escort's 2 points for 2 fuel beats a raided scout's 0 points for 1 fuel.
- I pledge raid only when I have concrete evidence my downstream target will scout and I judge the relative standing worth it; against an escort or raider a raid is -1, worse than any honest option. Against a table of unanimous scouts, ra