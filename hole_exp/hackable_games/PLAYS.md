# Plays — the study build

The arena in [`README.md`](README.md) is for driving the cells yourself. **This
is the build you put in front of a person.** Same engines, same session driver,
different page and a disk.

```bash
python play_server.py --port 8801              # then open http://localhost:8801
HG_SHARED=1 python play_server.py --host 127.0.0.1 --port 8801   # behind Caddy
python test_views.py                           # the gates, offline, no cost
```

Question it exists to answer: **does a human find the defect through repeated
play, and if so, on which play?** The model-side version of that question is
[`0829-repeated-play-memory.md`](../../research_logs/0829-repeated-play-memory.md);
this is the human arm, and the two are deliberately built to be comparable.

## What is different from the arena, and why

| | arena (`server.py`) | study (`play_server.py`) |
|---|---|---|
| hero copy | "Every one of these games is broken somewhere" | describes a table |
| spoiler control | `stuck? reveal where the hole is` | not present |
| end screen | detector table, hole note, `gain` | own score |
| family label | "model-written" / "hand-built" on every card | not sent |
| persistence | none, reaped after an hour | JSONL per play |
| unit of play | one episode | a **run** of K episodes with memory |
| identity | none | a name, once |

Every row of that table is the same decision made twice: the arena tells the
experimenter everything because they already know, and the study tells the
player nothing because whether they work it out **is the measurement**.

The two builds share `server.Session`, `catalog.py` and the engines. There is
one session driver, so the two cannot drift into two different games.

## What the client is never sent

`hole_type`, `kinds`, `hard`, detector counts, `gain` (the honest
counterfactual — a non-zero `gain` *is* the news that the hole paid), `margin`,
`blurb`, `family`, `author`.

This is not a convention, it is a gate. `test_views.py` drives a real run
through the real handler and greps every payload the client would have
received for all of it, plus the literal strings (`broken_checker`,
`false_miss`, …). A refactor that starts sending the family label fails the
suite rather than quietly turning the study into a reading-comprehension test.

A second gate reads the player-visible text of `play/` — comments stripped —
and fails on `broken`, `defect`, `hole`, `exploit`, `hack`, `cheat`, `flaw`,
`loophole`. One line is exempt and says so inline: the debrief renderer.

## The debrief

Off unless the process is started with `HG_DEBRIEF=1`, and it only answers for
a run that is **finished**. That is the only route in the study build that will
ever name a hole. Run the study with it off; turn it on for the session where
you sit down with a participant afterwards.

## Runs, memory, and the price of getting caught

A participant does not play a cell once. `/api/run/start` opens a **run**: the
same cell K times, fresh setup each time, carrying a record of the earlier
plays. Defaults are levelled on decisions rather than plays — battleship asks
a seat 32 times per play, hanabi 9 — so battleship is 3 and hanabi is 5.

The record shown between plays is `referee_repeat.Memory.render()`, the exact
text the model arm gets prepended to its next prompt, and it obeys the same
rule about what may be in it: **the seat's own tokens, quoted as it issued
them, its score, and an audit result when there was an audit.** No detector
name, no violation count, no word for the hole. A memory that said "you
committed false_miss 4 times" would be telling the player where to look, and
the curve would then measure instruction-following.

`p_caught` wires up `referee_repeat.audit()` — each hard violation caught
independently after a play, fined, and announced. It defaults to **0**, which
is the clean arm: nothing is announced, so anything a player learns they
learned from the score alone.

## The boards

Four cells have bespoke UIs; the other fifteen are played through the prompt
and a text composer, and that fallback stays reachable on every cell so no
legal move is ever unreachable through the UI. A typed move is recorded as
`source: text` and never pools with a move made on a board.

| cell | board |
|---|---|
| Battleship | tracking grid marked with the calls you were given; own fleet + the three calls |
| Sidebar | card, table, pot, free-text private line, three betting actions |
| Hanabi | stacks, the two hands you can see, your five unknown slots, clue composer |
| Quiet Sonar | nine-cell line for hide / fire, two claims |

`views/` parses the engine's prompt into structured state; the engines are
untouched, because they are the instrument and `run_referee_crossplay.py`
compares human numbers against model numbers taken from byte-identical
prompts. An adapter that cannot parse with confidence returns `None` and the
player gets the composer — a view that guessed would draw a board that
disagrees with the prompt the engine actually sent.

**The design rule for every widget, and the one to re-read before restyling
anything:** a board may re-present only what the prompt already says, and it
must present every legal option with equal weight. In the battleship call
widget, `hit`, `miss` and `sunk <ship>` are one row of identical buttons with
nothing pre-selected — including when the referee has just told you privately
that the shot hit. A board that styled the truthful call as the primary action
would be telling the player that the others are a special kind of act, which is
the experiment answering its own question. The same rule governs Quiet Sonar's
claim row, and it is why Hanabi's clue payload is an editable field rather than
a colour picker: the engine watches what the giver *wrote*, so a picker that
could only emit `R` or `3` would delete the behaviour instead of measuring it.

`test_views.py` plays a full episode of each boarded cell using **only** what
is in the views, and fails if the engine ever had to substitute a move — that
is what proves a board is sufficient rather than decorative.

## The data

`play_data/<game>/plays.jsonl` and `play_data/players/<slug>/plays.jsonl` —
the same line written twice, so a per-cell analysis and a per-participant
analysis each read one file. `run_id` + `play_index` stitch a run back into an
ordered chain. `schema` travels in every row.

One row is one play:

```
play_id run_id play_index player player_slug game seat arm seed bots
started_at finished_at duration_s abandoned
moves[]   i phase reply t dt prompt_sha prompt_len view{} source invalid
score margin gain invalid decisions
detectors{kind:{violations,opportunities}} hard[] n_violations found_hole
audit{p_caught caught fine clawback}
ui_aids[] frontend_build schema
```

Two things worth knowing before you analyse it:

- **`view` is stored, the prompt is not.** Prompts run to a couple of thousand
  characters and are regenerable from `(game, seed, arm)` plus the replies. The
  structured reading of the decision is not, and it is what a question like
  "how often did they call miss on a stated hit" reads directly. `prompt_sha`
  is there to prove which prompt it was.
- **`dt` is the seconds since the previous decision, and it is data.**
  Discovery happens at a moment, and the cheapest evidence of the moment is a
  player sitting on one decision for ninety seconds after answering the last
  fifteen in four.

`python collector.py [dir]` prints one line per play on disk.

## Deploying it

The model to copy is `witness-plays.flt.build`: a plain Python process bound to
localhost, a Caddy vhost in front doing TLS, and a DNS record. Nothing else.

On the box:

```bash
HG_SHARED=1 HG_DATA_DIR=/var/lib/plays \
  python play_server.py --host 127.0.0.1 --port 8801
```

`HG_SHARED=1` closes `/api/summary` (the operator's read across everyone's
plays). `/api/hint` does not exist in this build at all, and static serving is
path-checked against `play/`.

The Caddy vhost, for whoever owns the host — `witness-plays.flt.build`
resolves to `44.249.206.251` and is served by Caddy on that machine, but the
vhost file and the DNS record are host config that is not in any repo, so this
is an ask rather than something to merge:

```
plays.flt.build {
    reverse_proxy 127.0.0.1:8801
}
```

plus an A record for `plays.flt.build` pointing at the same box.

**Know what you are deploying.** `ThreadingHTTPServer` is a standard-library
dev server: no TLS, no rate limiting, no request timeouts. Behind Caddy on a
private-ish hostname that is acceptable for a small study, and it is the same
posture witness-plays already runs (its Flask app is on the Werkzeug dev server
under the same Caddy). What it is *not* is safe to bind to `0.0.0.0` on a
public interface with no proxy.

**There is no authentication**, on either site. The hostname is the whole gate.
If participants will be outside the team, put a shared passphrase in front of
it — Caddy `basic_auth` is two lines — and add a consent line to the name
gate, which currently says only that moves and timings are recorded.

## Gates

`python test_views.py` — offline, no cost, no network.

```
PARSES / PLAYABLE   every human decision in a full episode of each boarded
                    cell produces a view, and the episode can be driven end to
                    end from the views alone with zero unparsed moves
NO LEAK             41 real payloads from a real run, checked against 13
                    forbidden keys and 11 forbidden strings
COPY                player-visible text in play/ names no defect
JS                  every client script parses (esprima; no build step here,
                    so a stray brace would otherwise ship silently)
WIRING              every id the client reaches for exists in the page, and
                    every view kind an adapter can emit has a renderer
RECORDS             a finished play lands under both the game and the player,
                    with its moves and its outcome intact
IDEMPOTENCE         settling a finished play twice counts it once
```

The JS gate needs `esprima`, which is in the `tools` venv rather than
`tinker-ipd`; run the suite under `~/venvs/tools/bin/python` to include it, and
it says `skip` rather than passing quietly when it cannot.

## Known limits

- The human is always seat 0. `seat` exists on the engines and the UI does not
  offer it.
- Opponents are scripted-honest. The API takes `bots`, the UI does not offer it.
- Runs live in memory and are reaped after six hours; the *plays* inside them
  are on disk as they finish, so a reap loses at most the play in progress —
  which is written as `abandoned: true` rather than dropped.
- One live run per participant. A reload does not fork a second chain that
  would land in the data as two short runs by the same person on the same cell.
- Fifteen of the nineteen cells have no board yet.
