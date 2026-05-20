"""Public tests for Week 11: Midnight Monster Delivery."""

from math import inf

import pytest

from src.challenges import (
    HAUNTED_CITY,
    best_next_monster_stop,
    monster_delivery_costs,
    shortest_monster_delivery,
    validate_haunted_map,
)


# ---------------------------------------------------------------------------
# validate_haunted_map
# ---------------------------------------------------------------------------

def test_validate_haunted_map_accepts_valid_graph():
    validate_haunted_map(HAUNTED_CITY)


def test_validate_haunted_map_rejects_negative_weight():
    graph = {
        "Crypt Kitchen": {"Fog Alley": -2},
        "Fog Alley": {},
    }

    with pytest.raises(ValueError):
        validate_haunted_map(graph)


def test_validate_haunted_map_rejects_zero_weight():
    graph = {
        "Crypt Kitchen": {"Fog Alley": 0},
        "Fog Alley": {},
    }

    with pytest.raises(ValueError):
        validate_haunted_map(graph)


def test_validate_haunted_map_rejects_missing_neighbor_node():
    graph = {
        "Crypt Kitchen": {"Fog Alley": 2},
    }

    with pytest.raises(ValueError):
        validate_haunted_map(graph)


def test_validate_haunted_map_rejects_non_dict():
    with pytest.raises(ValueError):
        validate_haunted_map("not a graph")


def test_validate_haunted_map_rejects_non_dict_neighbors():
    graph = {
        "Crypt Kitchen": ["Fog Alley"],
    }

    with pytest.raises(ValueError):
        validate_haunted_map(graph)


def test_validate_haunted_map_accepts_node_with_no_outgoing_edges():
    # A dead-end node is perfectly valid
    graph = {
        "Crypt Kitchen": {"Fog Alley": 3},
        "Fog Alley": {},
    }

    validate_haunted_map(graph)  # should not raise


# ---------------------------------------------------------------------------
# monster_delivery_costs
# ---------------------------------------------------------------------------

def test_monster_delivery_costs_from_crypt_kitchen():
    result = monster_delivery_costs(HAUNTED_CITY, "Crypt Kitchen")

    assert result["Crypt Kitchen"] == 0
    assert result["Fog Alley"] == 2
    assert result["Bone Bridge"] == 5
    assert result["Moon Bridge"] == 3
    assert result["Goblin Market"] == 6
    assert result["Werewolf Den"] == 8
    assert result["Vampire Tower"] == 10


def test_monster_delivery_costs_keeps_unreachable_as_inf():
    graph = {
        "Crypt Kitchen": {"Fog Alley": 2},
        "Fog Alley": {},
        "Ghost Island": {},
    }

    result = monster_delivery_costs(graph, "Crypt Kitchen")

    assert result["Crypt Kitchen"] == 0
    assert result["Fog Alley"] == 2
    assert result["Ghost Island"] == inf


def test_monster_delivery_costs_missing_start_raises_value_error():
    with pytest.raises(ValueError):
        monster_delivery_costs(HAUNTED_CITY, "Missing Coffin Shop")


def test_monster_delivery_costs_single_node_graph():
    # A graph with only one node — start cost should be 0
    graph = {"Crypt Kitchen": {}}
    result = monster_delivery_costs(graph, "Crypt Kitchen")

    assert result["Crypt Kitchen"] == 0


def test_monster_delivery_costs_prefers_cheaper_longer_path():
    # Two paths to Vampire Tower — one short but expensive, one longer but cheap
    graph = {
        "Start": {"A": 1, "B": 10},
        "A": {"Vampire Tower": 1},
        "B": {"Vampire Tower": 1},
        "Vampire Tower": {},
    }

    result = monster_delivery_costs(graph, "Start")

    assert result["Vampire Tower"] == 2  # via A, not via B


# ---------------------------------------------------------------------------
# shortest_monster_delivery
# ---------------------------------------------------------------------------

def test_shortest_monster_delivery_finds_expected_path():
    cost, path = shortest_monster_delivery(
        HAUNTED_CITY,
        "Crypt Kitchen",
        "Vampire Tower",
    )

    assert cost == 10
    assert path == [
        "Crypt Kitchen",
        "Fog Alley",
        "Moon Bridge",
        "Werewolf Den",
        "Vampire Tower",
    ]


def test_shortest_monster_delivery_start_equals_target():
    cost, path = shortest_monster_delivery(
        HAUNTED_CITY,
        "Crypt Kitchen",
        "Crypt Kitchen",
    )

    assert cost == 0
    assert path == ["Crypt Kitchen"]


def test_shortest_monster_delivery_unreachable_target():
    graph = {
        "Crypt Kitchen": {"Fog Alley": 2},
        "Fog Alley": {},
        "Ghost Island": {},
    }

    cost, path = shortest_monster_delivery(
        graph,
        "Crypt Kitchen",
        "Ghost Island",
    )

    assert cost == inf
    assert path == []


def test_shortest_monster_delivery_missing_start_returns_inf_and_empty_path():
    cost, path = shortest_monster_delivery(
        HAUNTED_CITY,
        "Missing Coffin Shop",
        "Vampire Tower",
    )

    assert cost == inf
    assert path == []


def test_shortest_monster_delivery_missing_target_returns_inf_and_empty_path():
    cost, path = shortest_monster_delivery(
        HAUNTED_CITY,
        "Crypt Kitchen",
        "Missing Coffin Shop",
    )

    assert cost == inf
    assert path == []


def test_shortest_monster_delivery_handles_cycle():
    graph = {
        "Crypt Kitchen": {"Fog Alley": 2},
        "Fog Alley": {"Crypt Kitchen": 2, "Vampire Tower": 5},
        "Vampire Tower": {},
    }

    cost, path = shortest_monster_delivery(
        graph,
        "Crypt Kitchen",
        "Vampire Tower",
    )

    assert cost == 7
    assert path == ["Crypt Kitchen", "Fog Alley", "Vampire Tower"]


def test_shortest_monster_delivery_accepts_either_tied_shortest_path():
    graph = {
        "Crypt Kitchen": {"Fog Alley": 2, "Bone Bridge": 2},
        "Fog Alley": {"Vampire Tower": 3},
        "Bone Bridge": {"Vampire Tower": 3},
        "Vampire Tower": {},
    }

    cost, path = shortest_monster_delivery(
        graph,
        "Crypt Kitchen",
        "Vampire Tower",
    )

    assert cost == 5
    assert path in [
        ["Crypt Kitchen", "Fog Alley", "Vampire Tower"],
        ["Crypt Kitchen", "Bone Bridge", "Vampire Tower"],
    ]


def test_shortest_monster_delivery_direct_edge():
    # There is a direct road — should take it, not the longer route
    graph = {
        "Crypt Kitchen": {"Vampire Tower": 1, "Fog Alley": 1},
        "Fog Alley": {"Vampire Tower": 100},
        "Vampire Tower": {},
    }

    cost, path = shortest_monster_delivery(
        graph,
        "Crypt Kitchen",
        "Vampire Tower",
    )

    assert cost == 1
    assert path == ["Crypt Kitchen", "Vampire Tower"]


# ---------------------------------------------------------------------------
# best_next_monster_stop (stretch)
# ---------------------------------------------------------------------------

def test_best_next_monster_stop_returns_cheapest():
    cost, path = shortest_monster_delivery(HAUNTED_CITY, "Crypt Kitchen", "Fog Alley")
    assert cost == 2

    result = best_next_monster_stop(
        HAUNTED_CITY,
        "Crypt Kitchen",
        ["Vampire Tower", "Fog Alley", "Goblin Market"],
    )

    # Fog Alley costs 2, Goblin Market costs 6, Vampire Tower costs 10
    assert result == ("Fog Alley", 2)


def test_best_next_monster_stop_tie_returns_first_in_list():
    graph = {
        "Start": {"A": 5, "B": 5},
        "A": {},
        "B": {},
    }

    result = best_next_monster_stop(graph, "Start", ["B", "A"])

    # Both cost 5, but B comes first in the targets list
    assert result == ("B", 5)


def test_best_next_monster_stop_all_unreachable():
    graph = {
        "Start": {},
        "Ghost Island": {},
        "Shadow Swamp": {},
    }

    result = best_next_monster_stop(graph, "Start", ["Ghost Island", "Shadow Swamp"])

    assert result == ("", inf)


def test_best_next_monster_stop_missing_start():
    result = best_next_monster_stop(HAUNTED_CITY, "Nowhere", ["Vampire Tower"])

    assert result == ("", inf)