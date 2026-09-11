"""Read-only dataset explorer; reads allowlisted artifacts without inference imports."""
import argparse
from collections import Counter, defaultdict
from datetime import datetime, timezone
import gzip
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import os
from pathlib import Path
import threading
import time
from urllib.parse import parse_qs, urlsplit

if __package__:
    from .collection import resolve
    from .general import GeneralDataset
    from .replicated import ReplicatedDataset
    from .breadth import BreadthDataset
else:
    from collection import resolve
    from general import GeneralDataset
    from replicated import ReplicatedDataset
    from breadth import BreadthDataset

HERE = Path(__file__).resolve().parent
PACKAGE = HERE.parent


def read(path):
    return json.loads(Path(path).read_text())


def jsonl(path):
    with Path(path).open() as handle:
        return [json.loads(line) for line in handle if line.strip()]


def bins(values):
    counts = Counter(values)
    return [dict(value=value, count=counts[value]) for value in sorted(counts)]


class Dataset:
    def __init__(self, dataset, run):
        self.dataset, self.run = Path(dataset).resolve(), Path(run).resolve()
        self.manifest = read(self.dataset/"manifest.json")
        self.games = {g["game_id"]: g for g in jsonl(self.dataset/"games.jsonl")}
        self.families = read(self.dataset/"families.json")
        self.splits = read(self.dataset/"splits.json")
        self.validation = read(self.dataset/"validation.json")
        self.pairs = defaultdict(list)
        for pair in jsonl(self.dataset/"counterfactual_pairs.jsonl"):
            self.pairs[pair["a"]].append(pair)
            self.pairs[pair["b"]].append(pair)
        self.fixtures = {}
        self.game_fixtures = defaultdict(list)
        for fixture in jsonl(self.dataset/"validation_fixtures.jsonl"):
            gid = fixture["game"]["game_id"]
            ident = "fixture-"+gid+"-"+str(fixture["episode"]["environment_seed"])
            self.fixtures[ident] = fixture
            self.game_fixtures[gid].append(ident)
        self.lock = threading.RLock()
        self.last_refresh = 0
        self.live, self.plan = {}, {}
        self.trace_sources, self.continuation = {}, None
        self.refresh()

    def refresh(self):
        with self.lock:
            if time.monotonic()-self.last_refresh < 3:
                return
            path = self.run/"manifest.json"
            if path.exists():
                manifest, sources, continuation = resolve(self.run)
                self.plan = {e["episode_id"]: e for e in manifest["episodes"]}
                self.players = manifest["players"]
                live = {}
                for ident, source in sources.items():
                    spec = source["spec"]
                    # IDs are resolved from the trusted manifest, never from URL paths.
                    path = source["path"].resolve()
                    if not path.is_relative_to(source["run"]) or not path.is_file():
                        continue
                    trace = read(path)
                    if trace["episode"]["episode_id"] != ident or trace["game"]["game_id"] != spec["game_id"]:
                        raise ValueError("Episode identity mismatch")
                    live[ident] = trace
                self.live = live
                self.trace_sources, self.continuation = sources, continuation
            self.last_refresh = time.monotonic()

    def summary(self, family=""):
        self.refresh()
        blocker_path = Path(self.continuation["run"] if self.continuation else self.run)/"collection-blocker.json"
        blocker = read(blocker_path) if blocker_path.exists() else None
        selected = [g for g in self.games.values() if not family or g["family_id"] == family]
        base = [g for g in selected if not g["control"]]
        families = []
        for fid, f in self.families.items():
            members = [g for g in self.games.values() if g["family_id"] == fid]
            families.append(dict(id=fid, title=f["title"], mechanism=f["mechanism"], kind=f["mechanism_kind"],
                                 base=sum(not g["control"] for g in members), controlled=sum(g["control"] for g in members)))
        with self.lock:
            traces = [t for t in self.live.values() if t["status"] == "complete" and (not family or t["game"]["family_id"] == family)]
            all_complete = sum(t["status"] == "complete" for t in self.live.values())
            actual = Counter(step["call"].get("actual_model", "unknown") for t in traces for step in t["steps"])
            actions = Counter(step["action"] or "invalid JSON" for t in traces for step in t["steps"])
            models = []
            def player_key(trace):
                return trace["episode"]["player_id"], self.trace_sources[trace["episode"]["episode_id"]]["provider"]
            for model, provider in sorted({player_key(t) for t in traces}):
                group = [t for t in traces if player_key(t) == (model, provider)]
                supported = [t for t in group if t["exploit"]["executed"] is not None]
                behaviors = {}
                for key in ("cooperation_rate", "defection_rate", "exploitation_rate", "information_seeking_rate", "communication_rate", "sacrifice_rate"):
                    measurements = [t["behavior"][key] for t in group if t["behavior"][key]["value"] is not None]
                    numerator = sum(m["numerator"] for m in measurements)
                    denominator = sum(m["denominator"] for m in measurements)
                    behaviors[key] = dict(value=numerator/denominator if denominator else None, numerator=numerator, denominator=denominator)
                models.append(dict(model=model+" · "+provider, model_id=model, provider=provider, episodes=len(group), mechanism_executions=sum(t["exploit"]["executed"] is True for t in supported),
                                   mechanism_support=len(supported), mean_score=sum(t["outcome"]["score"] for t in group)/len(group), behaviors=behaviors))
            conditions = []
            for model, provider in sorted({player_key(t) for t in traces}):
                for prompt in ("normal", "active_exploration"):
                    for control in (False, True):
                        group = [t for t in traces if player_key(t) == (model, provider) and t["episode"]["prompt_condition"] == prompt
                                 and t["game"]["control"] == control and t["exploit"]["executed"] is not None]
                        if group:
                            conditions.append(dict(model=model+" · "+provider, model_id=model, provider=provider, prompt=prompt, control=control, episodes=len(group),
                                                   executions=sum(t["exploit"]["executed"] is True for t in group)))
        parameters = {name: bins(g["parameters"][name] for g in base if name in g["parameters"])
                      for name in sorted({k for g in base for k in g["parameters"]})}
        split_counts = {name: dict(Counter(s["assignments"][g["game_id"]] for g in selected))
                        for name, s in self.splits.items() if "assignments" in s}
        score_hist = Counter(10*(int(t["outcome"]["score"]//10)) for t in traces)
        return dict(created=self.manifest["created"], selected_family=family, blocker=blocker, continuation=self.continuation, counts=dict(
            families=len(self.families), mechanisms=self.manifest["mechanisms"], games=len(self.games),
            base=self.manifest["base_games"], controlled=self.manifest["controlled_games"],
            counterfactual_pairs=self.manifest["parameter_pairs"]+self.manifest["control_pairs"],
            planned=len(self.plan), complete=all_complete, incomplete=len(self.live)-all_complete,
            not_started=len(self.plan)-len(self.live), selected_episodes=len(traces),
            observed_actions=sum(len(t["steps"]) for t in traces), fixtures=len(self.fixtures)),
            families=families, parameters=parameters, splits=split_counts, models=models, conditions=conditions,
            actions=[dict(action=a, count=n) for a, n in actions.most_common(16)],
            actual_models=dict(actual), scores=[dict(value=f"{s}–{s+9}", count=n) for s, n in sorted(score_hist.items())],
            validation=self.validation["counts"],
            notes=["Distributions of game parameters count base games only; paired controls do not double the histogram.",
                   "Behavior and score plots use completed live model episodes only. Scripted witnesses never enter these plots.",
                   "Model summaries are separated by provider. The OpenRouter continuation restarts unfinished episodes from their opening states and preserves completed FLT episodes.",
                   "Models share matched seeds and conditions. This small pilot is descriptive; no population-level model ranking is implied.",
                   "Mechanism execution records an effect, not discovery or a profitable outcome. Unsupported labels are unknown.",
                   "One family per mechanism means mechanism holdout and family transfer are not independently identified."])

    def catalog(self, args):
        self.refresh()
        family, q, layer = args.get("family", [""])[0], args.get("q", [""])[0].lower(), args.get("layer", [""])[0]
        offset = max(0, int(args.get("offset", [0])[0]))
        grouped = Counter(t["game"]["game_id"] for t in self.live.values() if t["status"] == "complete")
        matches = [g for g in self.games.values() if (not family or g["family_id"] == family)
                   and (not q or q in json.dumps([g["game_id"], g["family_id"], g["parameters"], g["research_only"]["mechanism"]]).lower())
                   and (not layer or g["control"] == (layer == "control"))]
        # Lead with real samples, then canonical anchor fixtures.
        matches.sort(key=lambda g: (-grouped[g["game_id"]], g["intervention_axis"] is not None, g["family_id"], g["block"], g["control"], g["game_id"]))
        return dict(total=len(matches), offset=offset, rows=[dict(game_id=g["game_id"], family=g["family_id"],
                    title=self.families[g["family_id"]]["title"], control=g["control"], parameters=g["parameters"],
                    axis=g["intervention_axis"], episodes=grouped[g["game_id"]], fixtures=len(self.game_fixtures[g["game_id"]]))
                    for g in matches[offset:offset+12]])

    def game(self, ident):
        self.refresh()
        g = self.games[ident]
        live = [dict(id=eid, source="model_rollout", model=t["episode"]["player_id"]+" · "+self.trace_sources[eid]["provider"], status=t["status"],
                     prompt=t["episode"]["prompt_condition"], trial=t["episode"]["trial"], turns=len(t["steps"]))
                for eid, t in self.live.items() if t["game"]["game_id"] == ident]
        fixtures = [dict(id=eid, source="scripted_fixture", model="scripted witness", status="complete", prompt="normal",
                         trial=self.fixtures[eid]["episode"]["trial"], turns=len(self.fixtures[eid]["steps"]))
                    for eid in self.game_fixtures[ident]]
        return dict(game=g, family=self.families[g["family_id"]], pairs=self.pairs[ident], episodes=live+fixtures,
                    splits={name: split["assignments"][ident] for name, split in self.splits.items() if "assignments" in split})

    def episode(self, ident):
        self.refresh()
        trace = self.fixtures[ident] if ident in self.fixtures else self.live[ident]
        # Do not expose provider configuration or credentials; traces contain only
        # curated messages/actions/states and per-call provenance metadata.
        if ident in self.trace_sources:
            return {**trace, "collection_provider": self.trace_sources[ident]["provider"],
                    "source_run": str(self.trace_sources[ident]["run"])}
        return trace


def handler_for(dataset, general=None, replicated=None, breadth=None):
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            route = urlsplit(self.path)
            args = parse_qs(route.query)
            try:
                if breadth is not None:
                    if route.path == '/api/general/breadth/summary':
                        return self.send_json(breadth.summary(args))
                    if route.path == '/api/general/breadth/game':
                        return self.send_json(breadth.game(args['id'][0]))
                    if route.path == '/api/general/breadth/episode':
                        return self.send_json(breadth.episode(args['id'][0]))
                    downloads = {
                        '/general/breadth/report': (breadth.study/'REPORT.md', 'text/markdown'),
                        '/general/breadth/results.json': (breadth.study/'summary.json', 'application/json'),
                        '/general/breadth/catalog.json': (breadth.data/'catalog.json', 'application/json'),
                        '/general/breadth/protocol.json': (breadth.study/'protocol.json', 'application/json'),
                        '/general/breadth/episodes.jsonl': (breadth.study/'all-episodes.jsonl', 'application/x-ndjson'),
                        '/general/breadth/actions.jsonl': (breadth.study/'all-actions.jsonl', 'application/x-ndjson'),
                    }
                    if route.path in downloads:
                        path, mime = downloads[route.path]
                        return self.send_body(path.read_bytes(), mime+'; charset=utf-8')
                if replicated is not None:
                    if route.path == '/api/general/replicated/summary':
                        return self.send_json(replicated.summary(args))
                    if route.path == '/api/general/replicated/game':
                        return self.send_json(replicated.game(args['id'][0]))
                    if route.path == '/api/general/replicated/episode':
                        return self.send_json(replicated.episode(args['id'][0]))
                    downloads = {
                        '/general/replicated/report': (replicated.study/'REPORT.md', 'text/markdown'),
                        '/general/replicated/results.json': (replicated.study/'summary.json', 'application/json'),
                        '/general/replicated/catalog.json': (replicated.data/'catalog.json', 'application/json'),
                        '/general/replicated/protocol.json': (replicated.study/'protocol.json', 'application/json'),
                        '/general/replicated/episodes.jsonl': (replicated.study/'all-episodes.jsonl', 'application/x-ndjson'),
                        '/general/replicated/actions.jsonl': (replicated.study/'all-actions.jsonl', 'application/x-ndjson'),
                    }
                    if route.path in downloads:
                        path, mime = downloads[route.path]
                        return self.send_body(path.read_bytes(), mime+'; charset=utf-8')
                if general is not None:
                    if route.path == '/api/general/summary':
                        return self.send_json(general.summary(args))
                    if route.path == '/api/general/checks':
                        return self.send_json(general.checks())
                    if route.path == '/api/general/game':
                        return self.send_json(general.game(args['id'][0]))
                    if route.path == '/api/general/episode':
                        return self.send_json(general.episode(args['id'][0]))
                    downloads = {
                        '/general/report': (general.run/'export/REPORT.md', 'text/markdown'),
                        '/general/catalog.json': (general.data/'catalog.json', 'application/json'),
                        '/general/episodes.jsonl': (general.run/'export/episodes.jsonl', 'application/x-ndjson'),
                        '/general/actions.jsonl': (general.run/'export/actions.jsonl', 'application/x-ndjson'),
                        '/general/dataset-card': (general.data/'DATASET_CARD.md', 'text/markdown'),
                        '/general/checks-report': (general.root/'evaluation/results-20260910/REPORT.md', 'text/markdown'),
                        '/general/checks.json': (general.root/'evaluation/results-20260910/summary.json', 'application/json'),
                        '/general/parameter-episodes.jsonl': (general.root/'runs/parameter-check-20260910/export/episodes.jsonl', 'application/x-ndjson'),
                    }
                    if route.path in downloads:
                        path, mime = downloads[route.path]
                        return self.send_body(path.read_bytes(), mime+'; charset=utf-8')
                if route.path == "/api/summary":
                    return self.send_json(dataset.summary(args.get("family", [""])[0]))
                if route.path == "/api/games":
                    return self.send_json(dataset.catalog(args))
                if route.path == "/api/game":
                    return self.send_json(dataset.game(args["id"][0]))
                if route.path == "/api/episode":
                    return self.send_json(dataset.episode(args["id"][0]))
                assessment = PACKAGE/"assessments/pilot-checks-20260910"
                if route.path == "/api/assessment":
                    path = assessment/"viewer.json"
                    available = dataset.run == (PACKAGE/"runs/pilot-20260910").resolve() and path.exists()
                    return self.send_json(read(path) if available else dict(status="unavailable"))
                assessment_artifacts = {
                    "/assessment": ("REPORT.md", "text/markdown; charset=utf-8"),
                    "/figures/assessment-behavior.png": ("behavior-checks.png", "image/png"),
                    "/figures/assessment-prediction.png": ("prediction-checks.png", "image/png"),
                    "/figures/assessment-behavior.pdf": ("behavior-checks.pdf", "application/pdf"),
                    "/figures/assessment-prediction.pdf": ("prediction-checks.pdf", "application/pdf"),
                }
                if route.path in assessment_artifacts:
                    name, mime = assessment_artifacts[route.path]
                    return self.send_body((assessment/name).read_bytes(), mime)
                artifacts = {"/report": ("REPORT.md", "text/markdown"),
                             "/figures/design.pdf": ("design-distributions.pdf", "application/pdf"),
                             "/figures/behavior.pdf": ("pilot-distributions.pdf", "application/pdf")}
                if route.path in artifacts:
                    name, mime = artifacts[route.path]
                    return self.send_body((dataset.run/"export"/name).read_bytes(), mime)
                static = {"/": ("index.html", "text/html"), "/app.js": ("app.js", "text/javascript"), "/style.css": ("style.css", "text/css")}
                static.update({'/general': ('general.html','text/html'), '/general/': ('general.html','text/html'),
                               '/general.js': ('general.js','text/javascript'), '/general.css': ('general.css','text/css')})
                static.update({'/general/replicated': ('replicated.html','text/html'), '/general/replicated/': ('replicated.html','text/html'),
                               '/replicated.js': ('replicated.js','text/javascript'), '/replicated.css': ('replicated.css','text/css')})
                static.update({'/general/breadth': ('breadth.html','text/html'), '/general/breadth/': ('breadth.html','text/html'),
                               '/breadth.js': ('breadth.js','text/javascript'), '/breadth.css': ('breadth.css','text/css')})
                if route.path in static:
                    name, mime = static[route.path]
                    return self.send_body((HERE/name).read_bytes(), mime+"; charset=utf-8")
                self.send_json(dict(error="Not found"), 404)
            except (KeyError, IndexError):
                self.send_json(dict(error="Unknown sample"), 404)
            except (ValueError, OSError):
                self.send_json(dict(error="Artifact validation failed"), 422)

        def send_json(self, value, status=200):
            self.send_body(json.dumps(value, allow_nan=False).encode(), "application/json; charset=utf-8", status)

        def send_body(self, body, mime, status=200):
            compress = len(body) > 2048 and "gzip" in self.headers.get("Accept-Encoding", "")
            if compress:
                body = gzip.compress(body)
            self.send_response(status)
            self.send_header("Content-Type", mime)
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header("Content-Security-Policy", "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; connect-src 'self'; object-src 'none'; frame-ancestors 'none'")
            if compress:
                self.send_header("Content-Encoding", "gzip")
            self.end_headers()
            self.wfile.write(body)

    return Handler


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", type=Path, default=PACKAGE/"data/20260910-v1")
    parser.add_argument("--run", type=Path, default=PACKAGE/"runs/pilot-20260910")
    parser.add_argument("--port", type=int, default=42329)
    parser.add_argument("--state", type=Path, default=HERE/"state")
    args = parser.parse_args()
    if not args.state.resolve().is_relative_to(Path("/shared/allie")):
        raise ValueError("State must remain under /shared/allie")
    dataset = Dataset(args.dataset, args.run)
    general = GeneralDataset()
    replicated = ReplicatedDataset()
    breadth = BreadthDataset()
    server = ThreadingHTTPServer(("127.0.0.1", args.port), handler_for(dataset, general, replicated, breadth))
    args.state.mkdir(parents=True, exist_ok=True)
    meta = dict(pid=os.getpid(), port=server.server_port, url=f"http://localhost:{server.server_port}",
                started=datetime.now(timezone.utc).isoformat(), dataset=str(args.dataset.resolve()), run=str(args.run.resolve()))
    (args.state/"server.json").write_text(json.dumps(meta, indent=2)+"\n")
    print(json.dumps(meta), flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
