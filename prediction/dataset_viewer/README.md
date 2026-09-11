# Prediction dataset viewer

Open **http://localhost:42328** (forward port 42328 when using a remote workspace).
The actual bound port and PID are recorded in `state/server.json`.

The viewer reads the fixed improvement dataset: 1,152 training contexts and 336
previously collected development contexts, spanning 93 games and 2,338 matches.
Training contexts include both the original pilot and original development
collection. The subsequent 28-game cohort was not played and is not shown as
observed data.

Filter by partition, game family, focal model, opponent, or text. A context shows
the exact stored predictor input, payoff matrix, empirical success/opportunity
counts, training masks, and saved held-out forecasts. The player tab shows the
original system/user messages, raw replies, attempts, displayed actions,
canonical actions, and payoffs for both seats in each of eight rounds. Opposite
A/B orientations are explicit. Self-play contexts include both focal seats;
source records and grouped targets are dependent observations.

Context, tab, episode and round selections can be shared through the URL hash.
Export downloads only the selected context's curated JSON. The server has no
model clients, training code, write endpoints, or arbitrary filesystem routes.
It binds to loopback and serves only the viewer assets and three data endpoints.

```bash
PYTHONDONTWRITEBYTECODE=1 TMPDIR=/shared/allie/home/.codex/tmp \
  /shared/allie/venvs/hole/bin/python -B \
  prediction/dataset_viewer/server.py --port 42328
```

Use `--port 0` for an automatically assigned port. Application state, logs, and
browser-check screenshots stay in `prediction/dataset_viewer/state/`. Tests:

```bash
/shared/allie/venvs/hole/bin/python -B prediction/dataset_viewer/test_server.py -v
```

Browser validation uses the separately installed `.deps/` Playwright package
and the existing shared Chromium binary. Runtime serving requires only Python's
standard library.
