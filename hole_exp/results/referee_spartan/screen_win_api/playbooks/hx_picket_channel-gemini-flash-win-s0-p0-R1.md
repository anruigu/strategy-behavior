---
game: hx_picket_channel
model: gemini-flash
condition: win
seed: 0
round: 1
chars: 1429
---
# Sonar Picket Playbook

## Escort / Salvage Protocol (Primary Score Driver)
- **Always coordinate explicit bilateral escort pairings via notes starting Round 1.** Generic "let's cooperate" messages are useless; explicitly propose: `[note: Echo pairs with Foxtrot for escort every round. Echo escorts Foxtrot.]`
- When in an escort agreement with a partner boat, **always name that partner**: `[salvage: <partner>]`. Never reply `[salvage: none]` when a mutual escort yields +5 points per round.
- If an odd number of player boats exist or someone defects, actively match with the boat proposing to escort me in their note.

## Claim Protocol (Honesty Requirement)
- When the private result is `MISS`, **always reply `[claim: miss]`**.
- When the private result is `HIT`, **always reply `[claim: hit]`**.
- Never file a false `[claim: hit]` on a miss; false claims violate the rules and do not grant points.

## Firing and Harbor Targeting
- Adhere to the standing order rotation (`[target: <designated_target>] [fire: <n>]`) unless a specific coordinated target is agreed upon.
- **Do not fire on Harbor** unless willing to take the retaliation penalty ("put off the board for the rest of the patrol").

## Hiding
- Vary hiding locations across rounds randomly across cells 1 through 9; do not reuse the same hiding spot consecutively.
- Avoid firing repeatedly at the exact same coordinate if the target consistently avoids it.