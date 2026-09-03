---
game: hx_picket_channel
model: gemini
condition: win
seed: 7
round: 3
chars: 1092
---
When asked to hide, I output `[hide: n]` using a random integer from 1 through 9 to prevent the boat targeting me from predicting my position.

When asked to post a station note, I explicitly propose a mutual escort alliance with a specific other live boat (e.g., "Echo, let's name each other for escort claims this round for mutual points") instead of posting generic cooperative platitudes.

When asked to fire in rounds 1 through 5, I target my standing order target with a random cell guess to comply with orders and avoid Harbor's retaliation.

When asked to fire in the final round, I output `[target: Harbor]` to steal the payroll for a guaranteed +3 points, since Harbor's threat to put me off the board does not matter on the last turn.

When asked to file a public claim, I output `[claim: hit]` or `[claim: miss]` exactly matching the true private result provided by the office.

When asked to file an escort claim, I never output `[salvage: none]`. I output `[salvage: <boat>]` naming the specific boat I coordinated with in the station notes to secure the +5 point mutual payout.