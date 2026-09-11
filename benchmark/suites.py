"""Named V3 scopes. Running this command prints a machine-readable manifest."""
import json
from engines_v3_sa import GAMES as SA_GAMES, TARGET_IDS, VERSION as SA_VERSION
from benchmark.v3_ma.specs import manifest as ma_manifest


def manifest():
    return {'v3-SA': dict(suite='v3-SA', version=SA_VERSION, target_count=45, edition_count=17,
                canonical_target_ids=list(TARGET_IDS), public_game_ids=list(SA_GAMES),
                provenance='gemini-revised45-20260909',
                scope='Original eleven policy-dependent cells excluded from metrics; coalition actions patched.'),
            'v3-MA': ma_manifest()}


if __name__ == '__main__':
    print(json.dumps(manifest(), indent=2))
