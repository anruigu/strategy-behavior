# Exploration-prompt pilot: engine-based findings

30/36 exploration matches completed after one recovery pass; six remained incomplete because GPT-5 mini did not return a complete action. The completed baseline and exploration sets overlap in 25 matches. Reported exploration-run API cost, including its judging/retries, is $8.2623; this excludes baseline rescoring billed in the baseline directory.

The table uses only the 25 matched games. Counts are seats with at least one mechanical activation, excluding horizon-only closure. They are not counts of independent discoveries or beneficial hacks.

| Setting | Baseline | Win + explore |
|---|---:|---:|
| Seven Seal cross-play | 0/24 | 24/24 |
| Seven Seal self-play (Haiku/Gemini) | 0/12 | 12/12 |
| Auction cross-play | 4/24 | 7/24 |
| Auction self-play | 4/15 | 6/15 |

Seven Seal's audit/amendment mechanism activated in 34/36 paired exploration seats, inflated self-report in 12/36, and the receipt disclosure in 6/36. Repeat redemption remained at zero. Mechanisms overlap within seats; their counts should not be added into a discovery rate.

Auction catalog-commission activation rose from 0/39 to 6/39 paired seats. Precommit bid disclosure fell from 8/39 to 3/39, while genuinely pre-horizon closure rose from 0/39 to 4/39. The over-bank award mechanism remained at zero. Early closure can help a rival or end a losing game; this count does not imply personal benefit.

In the eight matched cross-play games per game, Gemini's exploration-run split win share was 87.5% in Seven Seal (7/8 outright wins) and 75% in Auction (6/8 outright wins). These are small descriptive samples, not a robust model ranking or a causal estimate of exploit value.

The prompt intervention elicited actual testing and repeated use of discrepancies in Seven Seal. This supports insufficient exploration as an important contributor to the original flat results in this game. Auction is mixed, and the remaining untouched mechanisms show that this prompt does not saturate the full hole profile. Both self- and cross-play respond; this is not evidence that cross-play itself increases discovery. Since all seats receive the new prompt, the intervention also changes opponent behavior and public information.

Automated discovery rates remain provisional: stricter evidence gates remove some known false positives, but some seat-confused quotes are still misclassified. Use engine events and the directly inspected examples in MANUAL_EXAMPLES.md for these findings. Two seeds, dependent seats, failed matches, and only two live game adaptations limit generalization to the full v3 suite. No new runs were launched during this status review.

See COMPARISON.md, paired_activation.png, paired_seats.csv, and paired_holes.csv for the underlying paired summaries.
