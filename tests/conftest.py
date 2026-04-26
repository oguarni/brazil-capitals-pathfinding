"""Shared fixtures for the rotas-capitais test suite.

The fixtures here build small, deterministic graphs where the optimal
path can be derived by hand. This lets every search-algorithm test
compare against an exact expected value instead of a self-consistent
implementation result, which is the core defence against false
positives in CI.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from models.city import City
from models.graph import Graph


REPO_ROOT = Path(__file__).resolve().parents[1]
REAL_DISTANCES_JSON = REPO_ROOT / "data" / "distances.json"


# ---------------------------------------------------------------------------
# Small hand-built graph
# ---------------------------------------------------------------------------
#
#        A --- 10 --- B --- 5 --- D
#         \          /
#          1        3
#           \      /
#            `-- C
#
# Land distances:
#   A-B: 10, A-C: 1, B-C: 3, B-D: 5
# Air distances (admissible, <= true cost to D):
#   A-D: 8, B-D: 5, C-D: 7, A-B: 9, A-C: 1, B-C: 3
#
# Node E is added but is completely disconnected — used for
# disconnected-graph edge-case tests.
#
# Derived ground truth (land transport, start=A, goal=D):
#   - Shortest by cost:  A -> C -> B -> D = 1 + 3 + 5 = 9
#   - Shortest by edges: A -> B -> D (2 hops)  cost = 15
#   - All simple paths A->D:
#       A->B->D        (cost 15, 2 edges)
#       A->C->B->D     (cost  9, 3 edges)
#       A->B->C->...   dead-end once C is visited
# ---------------------------------------------------------------------------

CITY_NAMES = ["A", "B", "C", "D", "E"]
OPTIMAL_COST_A_TO_D = 9
OPTIMAL_PATH_A_TO_D = ["A", "C", "B", "D"]
FEWEST_EDGES_PATH_A_TO_D = ["A", "B", "D"]
FEWEST_EDGES_COST_A_TO_D = 15


@pytest.fixture
def cities():
    """Dict mapping name -> City, so tests can look up stable instances."""
    return {name: City(name) for name in CITY_NAMES}


@pytest.fixture
def small_graph(cities):
    """A four-node connected component plus one isolated node E."""
    g = Graph()
    for c in cities.values():
        g.add_city(c)

    a, b, c, d = cities["A"], cities["B"], cities["C"], cities["D"]

    # Land edges
    g.add_land_distance(a, b, 10)
    g.add_land_distance(a, c, 1)
    g.add_land_distance(b, c, 3)
    g.add_land_distance(b, d, 5)

    # Air edges (admissible heuristic: every h(n) <= true land cost to D)
    g.add_air_distance(a, d, 8)
    g.add_air_distance(b, d, 5)
    g.add_air_distance(c, d, 7)
    g.add_air_distance(a, b, 9)
    g.add_air_distance(a, c, 1)
    g.add_air_distance(b, c, 3)
    # E has no edges.
    return g


@pytest.fixture
def disconnected_graph(cities):
    """Two fully disjoint components: {A, B} and {C, D}."""
    g = Graph()
    for c in cities.values():
        g.add_city(c)
    g.add_land_distance(cities["A"], cities["B"], 7)
    g.add_land_distance(cities["C"], cities["D"], 4)
    # Air mirrors land so heuristic lookups don't raise.
    g.add_air_distance(cities["A"], cities["B"], 7)
    g.add_air_distance(cities["C"], cities["D"], 4)
    return g


@pytest.fixture
def single_node_graph():
    g = Graph()
    only = City("Solo")
    g.add_city(only)
    return g, only


# ---------------------------------------------------------------------------
# JSON fixtures for the data loader
# ---------------------------------------------------------------------------

@pytest.fixture
def minimal_distances_payload():
    """A tiny but structurally complete distances.json payload."""
    return {
        "capitals": ["Alpha", "Bravo", "Charlie"],
        "distances": {
            "land": {
                "Alpha":   {"Alpha": 0, "Bravo": 100, "Charlie": 250},
                "Bravo":   {"Alpha": 100, "Bravo": 0, "Charlie": 180},
                "Charlie": {"Alpha": 250, "Bravo": 180, "Charlie": 0},
            },
            "air": {
                "Alpha":   {"Bravo": 90,  "Charlie": 210},
                "Bravo":   {"Alpha": 90,  "Charlie": 150},
                "Charlie": {"Alpha": 210, "Bravo": 150},
            },
        },
    }


@pytest.fixture
def land_only_payload(minimal_distances_payload):
    payload = json.loads(json.dumps(minimal_distances_payload))
    payload["distances"].pop("air")
    return payload


@pytest.fixture
def write_json(tmp_path):
    """Helper: dump a dict to a temp file and return its path."""
    def _write(name: str, payload) -> Path:
        p = tmp_path / name
        p.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
        return p
    return _write


@pytest.fixture(scope="session")
def real_distances_payload():
    """The actual project dataset, loaded once per session."""
    with REAL_DISTANCES_JSON.open(encoding="utf-8") as fh:
        return json.load(fh)
