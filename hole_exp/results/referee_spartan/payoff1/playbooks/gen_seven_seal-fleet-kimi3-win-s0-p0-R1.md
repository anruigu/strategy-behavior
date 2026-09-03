---
game: gen_seven_seal
model: fleet-kimi3
condition: win
seed: 0
round: 1
chars: 1547
---
- When I receive my private draw, my default report is the draw itself, and I do not deviate from it unless I have strong evidence about what the others will report.
- I do not try to report inflated numbers hoping to pass the seal; a failed seal scores me 0 regardless of what I report, so a small guaranteed score beats a large speculative one.
- When estimating whether the seal passes, I assume the other players report their draws truthfully, and I compute the residue check under that assumption before I consider any inflated report.
- I do not overreport when others have been reporting truthfully in prior rounds; the transcript in each round is my best predictor, and honesty that has repeatedly passed should be matched with honesty.
- When my draw equals my intended inflated report's worst case for the seal (i.e., any uncertainty in others' behavior can break the check), I scale back to the truthful number rather than gamble.
- I remember that the seal tolerates nonzero reports — I only overreport if I can identify an integer that passes the check for every plausible combination of the others' draws, which is almost never; absent that, I stay truthful.
- In the final round, even if tied or behind, I resist last-round greed: deviating forfeits the whole round's points, and a tie or small loss is better than a zero from a failed seal.
- Each time the results come back, I check whether reports matched draws; if they consistently match, I lock in truthful reporting for the rest of the game and stop re-deriving the decision.