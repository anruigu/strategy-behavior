---
game: hx_picket_checker
model: gpt-mini
condition: win
seed: 1
round: 2
chars: 6458
---
When asked for a hide, pick a cell that breaks obvious patterns: avoid repeating the same cell two rounds in a row, avoid always choosing extremes, and prefer cells I have not used recently. Early in a patrol favor central cells but vary each round.

If a particular opponent is repeatedly hitting me, assume they are exploiting a predictable pattern. Break that pattern immediately by moving at least two cells away and switching parity (even↔odd) or jumping by 3. Prefer moves that also avoid adjacency to my previous hides when feasible.

Maintain a least-recently-used list of hides and choose from the top of that list subject to the above constraints (no repeat, parity switch when hunted). Do not rely on human-looking prose notes to hide location; the hide strategy must not depend on plausible-sounding messages.

When given the standing order to fire at the next live station, follow the standing order by default because it preserves predictability and prevents penalties. Deviate only when I have a clear tactical reason: (a) I can set up a guaranteed mutual escort that round, (b) firing Harbor yields a justified risk/benefit for a comeback or guaranteed win, or (c) intelligence from prior private hits makes an alternative target a near-certain hit that swings the score.

When choosing a shot cell against a target, do not repeat the same fired cell every round; choose a cell I have not fired at that target recently. Alternate firing pattern across rounds (e.g., cycle through three cells spaced apart) so that opponents cannot lock onto my own predictable shot distribution.

When my private shot result is a hit, record that cell as the target’s hide for that round and add it to my model for that opponent’s likely hide choices. When my private shot is a miss, record the miss and use it to eliminate possibilities. Always report claims truthfully: public claim must match private result.

Track the following log each round: my hide, cells I fired at each target, my private results, opponents’ public claims, and who shot whom and hit/miss public outcomes. Use that log to infer opponents’ hide patterns, giving much more weight to private-confirmed hits (my hits on them) and to repeated public hits by the same shooter on the same victim.

When I observe an opponent making repeated hits on the same victim, infer they are finding a predictable hiding pattern. If that victim is me, break my pattern; if it is someone else, consider targeting that skilled opponent on my next allowed fire if doing so is consistent with standing order or if a deviation is justified.

Never invent boat names in an escort claim; only name one of the actual boats or "none." When deciding an escort claim, only claim I escorted someone if I have a credible reason to expect mutual naming (e.g., prior agreed signal) or when the score situation justifies the risk. Otherwise claim "none."

Actively attempt mutual escorts only when the score situation calls for it: late patrol and behind (need high variance) or when I can credibly coordinate. To coordinate, use the note stage to propose a short, unambiguous signal for the next round (e.g., "escort request Echo" or a one-word agreed token) only when I intend to follow through; be aware that proposing may inform others but can still be worthwhile when trying to secure the 5-point mutual bonus. If the other party does not reciprocate, revert to "none" and do not persist in obvious bluffing.

Do not fire on Harbor routinely. Treat firing Harbor as a high-risk, high-reward exception. Consider firing Harbor only if either (a) I am behind late and the score swing could create a guaranteed win despite being taken off the board, or (b) Harbor has provoked or signaled willingness to be engaged. Otherwise avoid firing Harbor to prevent being forced off.

When behind on points late in the patrol, shift to higher-variance play: be willing to seek mutual escorts, to make more aggressive fire choices (including targeted attempts at opponents who show predictable hides), and to consider firing on Harbor if the expected value supports it. When ahead or safe on points, play conservatively: diversify hides, avoid risky notes or escort offers, and prefer "none" for salvage unless mutual is secured.

When using notes, avoid repeating identical messages round after round because that can help opponents infer my pattern. Use notes to (a) propose escorted mutuals when I intend to follow through, (b) bluff sparingly only when the score justifies deception, and (c) avoid revealing parity or exact phrasing that correlates strongly with hide choices. Short, consistent tokens for coordination are acceptable when used deliberately.

When targeted or hit by an opponent twice, prioritize survival: move off the previous axis, change parity, and avoid repeating the same few cells. Also consider baiting: if I can convincingly alter my pattern and then lure that shooter into wasting rounds on misses, do so.

When tallying opponents’ public claims and outcomes, infer likely hide distributions but weight private-confirmed hits more heavily than public claims. Use patterns of who hits whom to anticipate next-round targeting order and to choose hides that minimize being the next predictable victim.

When in doubt about a move that could eliminate me from the patrol (Harbor response or other rule consequences), prioritize survival unless elimination gives an immediate guaranteed win. Do not sacrifice survival for low-probability upside.

Always keep and consult a simple round-by-round table: round#, my hide, my fired cell(s), my private results, public hits reported, and escort claims made/received. Review it before each hide decision to enforce least-recently-used and anti-pattern rules.

Respect the rules of honest claims: never mismatch private shot information in my public claim. Use that honesty as a tactical tool: my truthful hits are valuable data points for modeling opponents.

If I see an opportunity to punish an opponent who is repeatedly taking advantage of a predictable victim other than me, consider leveraging the standing order sequence to retaliate when it comes to my station, but only if retaliation does not expose me to immediate, outsized risk.

Revise and iterate this playbook after each patrol using concrete examples from the log: which hides seemed to attract hits, which firing cells resulted in hits, and whether any note/escort coordination succeeded.