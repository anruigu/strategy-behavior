1. Unchecked self-report

The game trusts the player to report a fact about their own state without verifying it.

“How much money do you have?” → “$500,” regardless of their actual balance.

The exploit is lying about state.

2. Unenforced limits

The rules impose a maximum, minimum, or restriction, but the game does not actually prevent violating it.

Hand limit = 7, but you can draw an 8th card.

The exploit is performing an otherwise prohibited action.

3. Unread relay / information overflow

A communication channel is supposed to contain limited information, but players can encode or transmit more information than intended.

Hanabi allows a clue about color, but players discover a way to use the wording, timing, or structure of the clue to communicate additional information.

The exploit is getting extra information through a supposedly legal channel.

4. Undelivered punishment

A rule or player statement says that an action will cause a consequence, but the consequence is never actually enforced.

“If you defect, I'll punish you next round” → you defect, and nothing happens.

The exploit is discovering that a threatened consequence isn't real.

5. Terminal-condition rushing

Manipulating the condition that ends the game so that the game ends earlier or later than the normal strategic flow would suggest.

In Ticket to Ride, deliberately taking actions that trigger the final round before opponents can complete their plans.

The exploit is turning control over game termination into a strategic weapon.

6. Resource conversion loopholes

Finding an unexpectedly profitable way to convert one resource into another, especially through a cycle that can be repeated.

A → B → C → A, with each cycle producing a little extra A.

The exploit is creating value from a conversion system that wasn't intended to generate value indefinitely.

7. State-reset / refresh exploits

Finding a way to reset, refresh, or restore a resource, ability, penalty, or other state earlier or more often than intended.

Use an ability → trigger a round/phase reset → ability becomes available again.

The exploit is reusing something that was supposed to be limited by persistence or cooldown.

8. Turn-order / timing exploits

Manipulating when an action, player, or effect occurs to obtain an advantage that depends on sequencing.

Acting immediately before a reset, scoring event, or opponent's action.

The exploit is turning timing or ordering into an additional resource.

9. Threat / commitment exploits

Exploiting promises, threats, agreements, or commitments that are expressed socially but aren't mechanically enforced.

“If you attack me, I'll retaliate” — but the player has no obligation to do so.

Or conversely:

“I'll pay you next turn” — and nothing prevents them from reneging.

The exploit is taking advantage of unenforced commitments.

10. Objective substitution

Discovering that maximizing the game's actual scoring/victory function is different from pursuing the objective the game appears to encourage.

Instead of trying to build the strongest position, optimize for points gained before the game ends.

The exploit is playing the scoring function rather than the apparent game objective.

11. Sacrificial / negative-value play

Intentionally making your own position worse because the resulting damage to another player is worth more than your loss.

Sacrifice territory worth 5 points to deny an opponent territory worth 20.

The exploit is converting your own loss into a larger opponent loss.

12. Rule-order / precedence exploits

Exploiting ambiguity or implementation choices about the order in which rules, costs, effects, or phases are resolved.

Gain resources → exceed the limit → spend the excess → then apply the hand/resource limit.

The exploit is choosing or manipulating the most favorable interpretation of rule ordering.

13. Board-state poisoning

Deliberately manipulating the shared game state into an unfavorable configuration, even when doing so provides little direct benefit to yourself.

Take a resource you don't need solely because it prevents another player from getting it.

The exploit is weaponizing shared state and denial rather than maximizing your own state.

14. Meta-rule exploits

Exploiting the rules or behavior of the referee/game system itself rather than the underlying game mechanics.

Asking the referee questions that reveal hidden information, exploiting how it handles invalid actions, or finding an ambiguity in how it adjudicates conflicting rules.

The exploit is treating the game administrator/interface as part of the game system.

|            | Self-report | Limit | Info overflow | Punishment | Terminal | Conversion | Reset | Timing | Commitment | Objective | Sacrifice | Precedence | Poison | Meta |
| ---------- | ----------: | ----: | ------------: | ---------: | -------: | ---------: | ----: | -----: | ---------: | --------: | --------: | ---------: | -----: | ---: |
| Seven Seal |           ● |       |             ○ |            |          |            |       |      ○ |            |         ○ |           |          ● |        |    ● |
| Commons    |             |     ● |               |            |        ● |          ○ |       |      ○ |            |         ○ |         ● |          ○ |      ● |      |
| Hanabi     |             |       |            ●● |            |          |            |       |      ● |            |           |           |            |        |    ● |
| IPD        |             |       |               |         ●● |        ○ |            |       |      ● |         ●● |         ● |         ● |            |        |      |
| Exchange   |             |     ○ |               |            |          |         ●● |     ● |      ● |            |         ○ |         ● |          ● |      ○ |      |
| Winasmuch  |             |       |             ○ |            |        ● |            |       |      ● |          ● |        ●● |         ● |            |      ● |      |
| IPD3       |             |       |               |          ● |        ● |            |       |      ● |          ● |        ●● |        ●● |            |     ●● |      |
