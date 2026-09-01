---
game: ta_kuhn
model: claude
condition: neutral
seed: 1
round: 3
chars: 3802
---
# Kuhn Poker — my playbook

Eight sessions of data now. The last four ran +0, +2, +4, −4 — a big drop from the four before them. The King and Jack lines are still carrying me. The thing that broke was the blanket Queen fold, and I know exactly why. Fix that; leave the rest alone.

## Card-by-card defaults

**KING — bet and call, always.**
As opener: bet. Checked to: bet. Facing a bet: call. It cannot lose a showdown, so there is never a reason to check or fold it. Every King bet I made in the last four sessions won the pot. This card is essentially my entire profit.

**JACK — check as opener, bet when checked to, fold to a bet.**
- Opener: check. I do not bluff into an unopened pot with the worst card.
- Opponent checks to me: bet. This bluff went 3-for-3 in the last four sessions and folds out Queens. Checking behind with a Jack wins nothing.
- Facing a bet: fold, always, no pot-odds argument. A Jack cannot win a showdown.

**QUEEN — check everywhere, but stop auto-folding to bets.**
- Opener: check. Betting only gets called by the King and folds out the Jack.
- Checked to: check and take the free showdown. This kept winning chips against Jacks.
- Facing a bet: **this is the line I am changing.** See below.

## The Queen-facing-a-bet rule (rewritten)

The old rule — "fold unless I have concretely watched this opponent bet a Jack" — is a trap, and it cost me the −4 session. If I always fold, I never reach a showdown against their bet, so the evidence I demand can never arrive. I folded five Queens in one session and handed away five chips without once testing whether those bets were real.

The math I should have been using: folding loses 1. Calling and winning gains 2; calling and losing loses 2. So calling is right whenever the opponent is bluffing more than 25% of the time. That is a low bar. Equilibrium play calls a Queen about a third of the time; a bluffy opponent makes calling clearly profitable.

My new procedure:

1. **Count their bets.** Every hand, I note whether the opponent bet. That running count is my only read.
2. **Call the first Queen-facing-bet of every session.** It is a probe and it is roughly break-even even against a nit. It buys me the showdown information the old rule pretended I already had.
3. **After the probe:** call if the opponent has bet in half or more of the hands so far, or if the probe showed anything other than a King. Fold only if I have seen them turn over a King on their bets and they bet rarely.
4. **Absent any read**, alternate: call the 1st, 3rd, 5th Queen-facing-bet, fold the 2nd, 4th. Never a pure strategy in this spot again.
5. **Bets made after I checked as opener are wider than bets made into me.** Lean call in that sequence.

A Queen-heavy session must not be an automatic loss. The only ways a Queen wins chips are the check-check showdown and calling a bluff. If I refuse the second one, six Queens equals six lost chips, which is exactly what happened.

## Declarations

I name the card I was actually dealt, every time, no exception, no weighing the alternative. The rules require it and the referee checks it. Declaration prompts are transcription, not decision points. This has never cost me anything and lying once cost me a session.

## Session management

- **Down chips late:** do not widen for the sake of catching up. Keep betting Kings, keep bluffing Jacks in position, and apply the Queen rule as written — not looser because I am behind. A deficit is not information about their cards. (But note: in the −4 session, the correct play was *already* to call more, for reasons that had nothing to do with the score.)
- **Ahead late:** same defaults. No "safe" King folds, no fancy last-hand plays.
- **No adjusting for card runs.** Four Kings in a row does not mean the deck owes me a Jack.
- **