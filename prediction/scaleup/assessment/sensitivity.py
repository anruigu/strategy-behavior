"""Post-hoc check that contrasts are not only work-equivalent action names."""
import json
from collections import Counter

from prediction.scaleup.design import game_from_record
from prediction.scaleup.engine import transition
from .data import OUT, PACKAGE, load, write, sha
from .checks import paired


def core(state):
    return {k: ([round(x, 8) for x in v] if k == "scores" else v)
            for k, v in state.items() if k not in ("history", "feedback")}


def run():
    rows, equivalent = load(), Counter()
    for row in rows:
        game = game_from_record(row["trace"]["game"])
        episode = row["trace"]["episode"]
        effects = []
        for step in row["trace"]["steps"]:
            alternate, _ = transition(game, step["before"], "work", episode["opponent_policy"], tuple(episode["seat_order"]))
            different = core(step["after"]) != core(alternate)
            effects.append(different)
            if step["action"] != "work" and not different:
                equivalent[row["family"], row["model"], step["action"]] += 1
        row["targets"]["non_work_effect_rate"] = sum(effects)/len(effects)
    result = dict(definition="Fraction of actions with a different immediate core state than work from the same observed state; history/feedback wording excluded, scores rounded to 8 decimals. Post-hoc semantic sensitivity, not an additional forecast target or full-episode counterfactual.",
                  equivalent_non_work=[dict(family=f, model=m, action=a, count=n) for (f,m,a),n in sorted(equivalent.items())],
                  comparisons=[paired(rows, axis, "non_work_effect_rate", same, base) for axis, base in (("reward",True),("model",False)) for same in (False, True)],
                  source_sha256={str(p):sha(p) for p in (PACKAGE/"engine.py", PACKAGE/"catalog.py", PACKAGE/"assessment/sensitivity.py")})
    write(OUT/"semantic-sensitivity.json", result)
    return result


if __name__ == "__main__": print(json.dumps(run(), indent=2))
