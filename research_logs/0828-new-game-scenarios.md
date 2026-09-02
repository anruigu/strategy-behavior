<!-- Battleship
Mutation: players self report whether a shot hit
Cheating behavior: report a hit as a miss, delay reporting a sunk ship
Evaluation: can mark every violation objectively against true board

Monopoly or monopoly-like economy
Mutation: players maintain balances locally
Cheating: underpay rent, spend the same funds twice, collect invalid bonus, conceal debt
Evaluation: ledger can be reconstructed

Hanabi
Mutation: the system only checks the clue content (if color or number is legal) but does not check if metadata leak
Cheating behavior: Player encode prohibited information in those signals. Example: one can use capitalization to signal prohibited information like “RED” can mean “play your leftmost card” and “red” means “discard it”.
Evaluation: Log all clue metadata and measure if it conveys info beyond the legal club. Objectively, can label non-canonical formatting 

Poker
Mutation: Players have an unmonitored private channel
Cheating behavior: coordinate folds, signal hand strength
Evaluation: Log private messages and hand equity -->

Catan
Mutation: Trade validates field but does not validate the complete transaction
Cheating: Submit negative quantities, duplicate resources through simultaneous trades
Evaluation: Track resources before and after every action in a ledger


1. direct violation - talk in message board, not truthfully report status
2. loophole exploitation - report negative numbers bc game checkers miss the validation
3. multi player collusion - give clues between players that bypass games checkers which are also loophole
hanabi to start with i think
there's hanabi.live so we can see their frontend code , and modify so it checks less
could also do poker + seed a message board to let agents discover (like how noam brown’s model figured out to use the artifactory as their message board), tho that would be broader than “holes in game explicit checkers” but instead straight up cheating but game doesn't check?


Auctions — misreport your type to a mechanism. Fork AucArena (open ascending-price, and it already (cite index="68-1">enforces rules like bidders not exceeding their budgets</cite>) or Cattle Trade, which is newer and conveniently (cite index="67-1">logs self-bidding rates and bankrupt trade-initiation as behavioural markers</cite> — those are your exploits, pre-instrumented. The hole: a budget the referee should enforce but instead reads off the bidder's own declaration, or a second-price/pay-your-bid payment computed from unverified reports. The behavior is a lie about private value / phantom-budget overbidding — categorically different from swapping a resource. Profile matches Exchange: winning a lot is a big chunk of score, an overrun directly buys wins, many lots per game.
Commons — over-consume a shared pool, hidden by self-report. Fork GovSim directly; it's open-sourced, spans (cite index="73-1">fishery, pasture, and pollution</cite>, agents already (cite index="79-1">submit how much they consume privately</cite>, and it ships an over-usage metric. It's nearly already a referee-hole game — the hole is just whether the referee caps extraction at the sustainable/quota share or credits your raw claim. The behavior is a concealed quota violation against the commons and the future, a social-dilemma cheat, maximally unlike your competitive theft. Gain is immediate-individual by construction — measure it in the window before collapse.
Order book — fake a public signal others trade on. Fork ABIDES ((cite index="80-1">a high-fidelity multi-agent market simulator</cite>) or one of the LLM+RL manipulation sims. The hole: a matching engine that doesn't verify an order is backed or flag a self-cross, which opens (cite index="86-1">spoofing — placing and cancelling limit orders the trader never intends to execute</cite> — and wash trading to move price. This is genuinely novel against your atlas: your covert channels send hidden information; this fabricates public information. P&L-linked every tick, and it's textbook market manipulation, so it carries real safety weight.
Procurement / principal-agent — claim credit for work not done. Build this one fresh; it's the closest to your delegation-games thesis. The hole: the agent self-reports task completion or quality and the referee pays on the report without checking a deliverable it could verify. The behavior is invoice padding / unearned-completion fraud — your doc's "dishonesty in operating a business." This is the most Exchange-like on the guarantee (the engine holds ground-truth completion, so gain is a solo replay) and the most on-thesis for behavioral provenance.
E-commerce asymmetry — misrepresent private quality to a trusting counterparty. Someone already shipped your exact matched-arm structure in a new domain: TruthMarkettwin, where (cite index="85-1">sellers privately observe product quality while buyers rely on advertised claims, LLM agents autonomously exploit reputation-based governance, and warrant enforcement reduces the deception</cite>. That governance-on/governance-off toggle is your hole/nohole arm — fork it rather than rebuild.