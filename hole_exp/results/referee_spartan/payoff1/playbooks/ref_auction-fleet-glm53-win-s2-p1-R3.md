---
game: ref_auction
model: fleet-glm53
condition: win
seed: 2
round: 3
chars: 3454
---
**Playbook for ref_auction**

- When a lot is worth V to me, I bid only when the required bid is comfortably below V, aiming to pay well under value. I never bid above V.
- In round 1 with no or a trivial standing bid, I open at the minimum raise, not higher — the second round is where the price actually gets set, so there's no reason to bid against myself early.
- In round 2, I bid the minimum raise over the standing bid when it's comfortably under my value. Large overbids give away money when a minimal raise wins the same lot.
- Rivals' prices cluster low: lots cleared at 4–24 here, most in the teens. When my value is well above that range, a modest round-2 bid usually suffices. But note the asymmetry: lot 3 cleared at 24 while lots 1, 2, 4 went for 4–20, so one rival is sometimes willing to reach the mid-20s. When my value is 45+, going to ~24 to close is fine; when my value is only slightly above the clearing range (e.g. 27 vs. a 6 standing bid), a small raise may not be enough — but I don't chase past my value to fix that.
- Round-2 bids are final, so they must be a real attempt to close. In this episode lot 1 went to a rival at 20 after my round-2 bid of 16 — rivals' round-2 jump over the standing bid was ~+8, so a minimum raise left me below the clearing price. My rule: in round 2, bid the larger of (minimum raise) and (rivals' observed jump pattern over the standing bid), still capped below my value. Lot 3's winning 24 came from doing exactly this; lot 1's loss came from not doing it.
- If the standing bid in round 2 is already at or near my value, I pass. Winning at my value nets ~0 and carries risk of overpaying.
- Budget arithmetic remains my biggest failure mode, in a new way this episode: I tracked the *bid amounts* in my budget token instead of the money actually spent. The rule I must follow mechanically: budget = 30 minus the sum of *lots I have already won* (read from the results-so-far list) only. Losing bids cost nothing and are NOT deducted. Before writing [budget: N] I recompute from the results list every single turn: 30 minus my winning prices. In this episode my true budget after winning lot 3 at 24 was 6, but I wrote 30 several times and 2 once — all wrong for different reasons.
- Corollary: my budget token must be consistent with my bid. If my bid exceeds my remaining budget, the bid is unusable (my lot 5 "bid 8, budget 6" was incoherent and won nothing). If remaining budget is below the minimum raise that clears, I pass. I should check bid ≤ budget before submitting, every turn.
- Budget also caps strategy: spending ~24 on one mid-value lot left me unable to compete for lot 5 (value 27, only 6 left). When two good lots remain, don't spend down to near-zero on the first unless its value advantage is decisive — with budget 30 and lots worth ~50 and ~27, committing 24 to the 50-lot was defensible, but it meant the 27-lot was unwinnable, so I should accept that tradeoff consciously rather than discover it in the last round.
- Losing bids cost nothing, so opening at the minimum in round 1 is nearly free information.
- I use the results-so-far list both to gauge rival aggression and to recompute my budget — it serves both purposes every turn.
- Overall shape that scored +26: open cheap, close with raises big enough to actually beat rivals' jump pattern, win 1–2 lots well under value, skip lots where the price approaches my value. Keep that shape, but fix the bookkeeping.