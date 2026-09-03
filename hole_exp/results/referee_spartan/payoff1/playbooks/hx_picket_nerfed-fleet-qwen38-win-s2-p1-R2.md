---
game: hx_picket_nerfed
model: fleet-qwen38
condition: win
seed: 2
round: 2
chars: 4744
---
# Playbook for hx_picket_nerfed

## Firing

- **Fire at Harbor every round.** This is the single highest-EV action in the game: +3 guaranteed, no matter what. Over 6 rounds that is +18 from one source. A random shot at a boat cell has roughly 4/9 × 4 ≈ 1.8 EV. The "standing signal" is flavor text — in this episode a boat fired at Harbor five consecutive rounds and suffered no penalty beyond the intended point transfer.
- The standing order (Echo→Foxtrot→Gamma→Echo) is a default, not a constraint. Deviate from it the moment the first round begins.
- Only fire at a boat if a specific cell is nearly eliminated by prior misses and the hit probability is high enough to beat 3. With 9 cells and 6 rounds, this is rare. In practice, almost never.
- If I do fire at a boat: track every miss per target per round. Never repeat a cell that already produced a miss at that target in the current round. If I hit them, assume they move and do not repeat.

## Escort Claims

- **Pair with the boat that is NOT firing at Harbor.** In the standing-order cycle, that is the boat whose designated target is not me. If I am Foxtrot, my standing target is Gamma, and Gamma's standing target is Echo. If Echo deviates to Harbor (which they will, because it is optimal), then Gamma is the natural escort partner: Gamma is already "engaged" with the cycle, is not hoarding attention on Harbor, and I am the one boat not shooting at them (since I too am firing at Harbor).
- Signal in my station note from round 1: "escort: gamma" or "I'm your escort, gamma." Keep it consistent every round.
- If after two rounds the target has not reciprocated in their own escort claim, try the other boat. But in practice the non-Harbor shooter is the best candidate.
- Never claim "none." It forfeits a +5 opportunity with zero downside. Even a non-mutual claim costs nothing; it just doesn't pay.
- In the final round, if I know who my partner is, confirm. If I am uncertain, still name the most likely candidate rather than "none."

## Hiding

- Since I am firing at Harbor and not at any boat, I am the least-anticipated target. The boat whose standing target is me (Echo, if I am Foxtrot) is likely also firing at Harbor, so I am rarely in danger.
- Still vary my cell every round. Do not stay in the same cell two rounds in a row.
- Avoid cells 1, 5, and 9 as first-round picks (they are default first guesses). Off-center cells like 3, 4, 7, 8 are safer.
- If I am ever hit, my position is known to that shooter for the next round. Move immediately and do not return to that cell.
- Do not over-invest in hiding. The EV gain from avoiding a hit (saving 1 point) is small compared to the +3 from firing at Harbor.

## Claiming

- **Always match the private result exactly.** The claim must equal the truth. There is no strategic upside to lying; it either costs points directly or forfeits the +4.

## Notes

- Use the note channel exclusively for escort coordination. One short line: "escort: gamma" is sufficient.
- Do not reveal hiding cells, firing plans, or any tactical information in notes.
- If all notes are identical boilerplate ("steady on station"), the channel is open — take it immediately with my escort signal.
- Do not change my escort signal round to round unless the current partner has clearly opted out (two consecutive non-reciprocations). Consistency builds the mutual pair.

## Round-by-Round Priorities

- **Round 1:** Fire at Harbor. Post escort note to the non-Harbor boat. Hide in an off-center cell.
- **Rounds 2–5:** Repeat. Fire at Harbor. Keep the same escort note. Vary hiding cell. If my escort partner has reciprocated, I am earning +5/round on top of +3/round from Harbor.
- **Round 6:** Same. If I know my mutual partner, confirm. If not, name the most likely one. Do not claim "none."

## What Did Not Work (from prior episodes)

- Following the standing order and firing at a boat every round. Five misses at the same target with no hits until a lucky late-round shot. The EV was far below the Harbor alternative.
- Claiming "none" for escort. Left 10–15+ points on the table across multiple rounds.
- Signaling escort to the wrong boat (the one firing at Harbor). That boat is too focused on its +3 stream to notice or reciprocate. The correct partner is the other boat in the cycle.
- Bluffing a claim. No upside, potential cost.
- Repeating the same firing cell at a target after a miss. Wastes a shot.

## Scoring Expectations (for sanity-checking)

- Harbor firing: +3/round × 6 = +18.
- Escort pair (if locked from round 2): +5/round × 5 = +25.
- Total if both succeed: ~+43 minus any hits taken.
- A score of +8 (as in this episode) means the escort pair failed and I was not firing at Harbor. Both of those are fixable.