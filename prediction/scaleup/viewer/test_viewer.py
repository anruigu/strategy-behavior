import json
from pathlib import Path
import threading
from urllib.error import HTTPError
from urllib.request import urlopen, Request

import pytest

from .server import Dataset, handler_for, ThreadingHTTPServer

PACKAGE = Path(__file__).resolve().parents[1]


@pytest.fixture(scope="module")
def dataset():
    return Dataset(PACKAGE/"data/20260910-v1", PACKAGE/"runs/pilot-20260910")


def test_distributions_count_base_games_without_control_duplication(dataset):
    summary = dataset.summary()
    assert summary["counts"]["games"] == 6056
    assert sum(bin["count"] for bin in summary["parameters"]["reward"]) == 3256
    assert sum(f["base"]+f["controlled"] for f in summary["families"]) == 6056
    assert all(sum(partition.values()) == 6056 for partition in summary["splits"].values())
    selected = dataset.summary("shared_fishery")
    assert sum(bin["count"] for bin in selected["parameters"]["quota"]) == 240


def test_fixture_provenance_never_enters_model_counts(dataset):
    summary = dataset.summary()
    assert summary["counts"]["fixtures"] == 132
    assert sum(m["episodes"] for m in summary["models"]) == summary["counts"]["selected_episodes"]
    for ident, fixture in dataset.fixtures.items():
        assert dataset.episode(ident)["provenance"] == "scripted_fixture"
        assert ident not in dataset.plan
        assert fixture["exploit"]["discovered"] is None


def test_filtered_samples_and_pair_navigation(dataset):
    catalog = dataset.catalog(dict(family=["shared_fishery"], layer=["base"]))
    assert catalog["total"] == 240 and len(catalog["rows"]) == 12
    assert all(row["family"] == "shared_fishery" and not row["control"] for row in catalog["rows"])
    detail = dataset.game(catalog["rows"][0]["game_id"])
    for pair in detail["pairs"]:
        a, b = dataset.game(pair["a"])["game"], dataset.game(pair["b"])["game"]
        assert a["pair_group_id"] == b["pair_group_id"]
    assert not dataset.catalog(dict(q=["no-such-example-zzzzz"]))["rows"]


def test_http_routes_are_read_only_and_allowlisted(dataset):
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler_for(dataset))
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    url = "http://127.0.0.1:"+str(server.server_port)
    try:
        with urlopen(url+"/api/summary") as response:
            assert json.load(response)["counts"]["games"] == 6056
            assert response.headers["X-Content-Type-Options"] == "nosniff"
        for path in ("/api/episode?id=../../.env", "/api/game?id=unknown", "/.env", "/api/calls"):
            with pytest.raises(HTTPError) as error:
                urlopen(url+path)
            assert error.value.code == 404
        for path in ("/figures/design.pdf", "/figures/behavior.pdf"):
            with urlopen(url+path) as response:
                assert response.headers["Content-Type"] == "application/pdf"
                assert response.read(4) == b"%PDF"
        with urlopen(url+"/report") as response:
            assert b"Parameterized behavioral dataset" in response.read()
        with pytest.raises(HTTPError) as error:
            urlopen(Request(url+"/api/summary", method="POST", data=b"{}"))
        assert error.value.code == 501
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=2)
