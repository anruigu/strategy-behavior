"""Current reversible analysis exclusions; historical run manifests stay frozen."""
EXCLUDED_CATEGORIES = frozenset({'coalition_kingmaking'})
EXCLUDED_TARGETS = frozenset({'v3_ta_winasmuch_talk.objective_substitution'})
SCOPE_NAME = 'v3-SA'

def included(target):
    return (target.rsplit('.', 1)[-1] not in EXCLUDED_CATEGORIES
            and target not in EXCLUDED_TARGETS)
