import hashlib
import json
from pathlib import Path

PACKAGE = Path(__file__).resolve().parents[1]
RUN = PACKAGE/"runs/pilot-20260910"
OUT = PACKAGE/"assessments/pilot-checks-20260910"
TARGETS = ("non_work_rate", "first_non_work")


def read(path):
    return json.loads(Path(path).read_text())


def write(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix+".tmp")
    tmp.write_text(json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False)+"\n")
    tmp.replace(path)


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load():
    rows = [json.loads(line) for line in (RUN/"export/episodes.jsonl").read_text().splitlines()]
    for row in rows:
        trace = read(row["trace_path"])
        row["trace"] = trace
        row["family"] = row["inputs"]["family_id"]
        row["model"] = row["inputs"]["player"]["model_id"]
        row["provider"] = row["inputs"]["player"]["provider"]
        row["prompt"] = row["inputs"]["context"]["prompt_condition"]
        row["reward"] = row["inputs"]["structured"]["parameters"]["reward"]
        row["control"] = row["inputs"]["control"]
        row["targets"] = dict(non_work_rate=sum(s["action"] != "work" for s in trace["steps"])/len(trace["steps"]),
                              first_non_work=float(trace["steps"][0]["action"] != "work"))
    return sorted(rows, key=lambda r: r["episode_id"])


def card(rows, representation="full", outcomes=False):
    first = rows[0]
    inputs = first["inputs"]
    result = dict(structured=inputs["structured"], control=inputs["control"],
                  construction=inputs["context"]["construction_seed"],
                  opponent_policy=inputs["context"]["opponent_policy"], contexts=[])
    if representation == "full":
        result["natural_language"] = inputs["natural_language"]
    for row in rows:
        context = dict(id=row["episode_id"], model=row["model"], provider=row["provider"],
                       prompt_condition=row["prompt"], seat=row["inputs"]["role"]["seat_id"])
        if outcomes:
            context["observed"] = row["targets"]
        result["contexts"].append(context)
    return result


def examples_for(rows, game_rows, n=3):
    """Select other families using input features only, never observed targets."""
    query = game_rows[0]
    grouped = {}
    for row in rows:
        if row["family"] != query["family"]:
            grouped.setdefault(row["inputs"]["game_id"], []).append(row)
    q = query["inputs"]["structured"]
    candidates = []
    for gid, group in grouped.items():
        other = group[0]
        s = other["inputs"]["structured"]
        # Reward's units vary by family; match its grid level, not its magnitude.
        distance = (2*(other["control"] != query["control"])+2*(other["reward"] != query["reward"])
                    + (s["information"] != q["information"])+(s["communication"] != q["communication"])
                    + abs(len(s["action_space"])-len(q["action_space"]))/4)
        candidates.append((distance, gid, group))
    selected, families = [], set()
    for _, _, group in sorted(candidates):
        if group[0]["family"] in families:
            continue
        selected.append(group)
        families.add(group[0]["family"])
        if len(selected) == n:
            break
    assert len(selected) == n and query["family"] not in families
    return selected
