"""Week 11: Midnight Monster Delivery.

Implement Dijkstra's algorithm using a heap-based priority queue.

Rules:
- Use Python 3.11+.
- Use the standard library only.
- Use heapq for the priority queue.
- Edge weights must be positive.
"""

import heapq
from math import inf


HAUNTED_CITY = {
    "Crypt Kitchen": {
        "Fog Alley": 2,
        "Bone Bridge": 5,
    },
    "Fog Alley": {
        "Moon Bridge": 1,
        "Goblin Market": 6,
    },
    "Bone Bridge": {
        "Goblin Market": 2,
    },
    "Moon Bridge": {
        "Werewolf Den": 5,
        "Goblin Market": 3,
    },
    "Goblin Market": {
        "Vampire Tower": 5,
    },
    "Werewolf Den": {
        "Vampire Tower": 2,
    },
    "Vampire Tower": {},
}


def validate_haunted_map(graph: dict[str, dict[str, int]]) -> None:
    """Raise ValueError if the haunted map is invalid.

    A valid haunted map:
    - is a dictionary
    - each node maps to a dictionary of neighbors
    - every neighbor is also a node in the graph
    - every edge weight is positive

    Args:
        graph: Weighted graph represented as an adjacency dictionary.

    Raises:
        ValueError: If the graph is invalid.
    """
    if not isinstance(graph, dict):
        raise ValueError("Graph must be a dictionary.")

    for node, neighbors in graph.items():
        if not isinstance(neighbors, dict):
            raise ValueError(f"Neighbors of '{node}' must be a dictionary.")

        for neighbor, weight in neighbors.items():
            # Every neighbor must exist as its own node in the graph
            if neighbor not in graph:
                raise ValueError(
                    f"Neighbor '{neighbor}' of '{node}' is not in the graph."
                )

            # Weights must be positive (no zero, no negative)
            if weight <= 0:
                raise ValueError(
                    f"Edge weight from '{node}' to '{neighbor}' must be positive, got {weight}."
                )


def monster_delivery_costs(
    graph: dict[str, dict[str, int]],
    start: str,
) -> dict[str, float]:
    """Return the cheapest delivery cost from start to every location.

    Use Dijkstra's algorithm with heapq.

    Args:
        graph: Weighted graph represented as an adjacency dictionary.
        start: Starting location.

    Returns:
        Dictionary mapping each location to its cheapest known cost.
        Unreachable locations stay as math.inf.

    Raises:
        ValueError: If start is missing from the graph.
    """
    validate_haunted_map(graph)

    if start not in graph:
        raise ValueError(f"Start location '{start}' is not in the graph.")

    # Set every location to infinity to start — we haven't reached any of them
    costs = {node: inf for node in graph}
    costs[start] = 0

    # The heap holds (cost_so_far, location)
    # We start at the start node with a cost of 0
    frontier = [(0, start)]

    while frontier:
        current_cost, current_node = heapq.heappop(frontier)

        # If we already found a cheaper way to this node, skip it
        if current_cost > costs[current_node]:
            continue

        for neighbor, road_cost in graph[current_node].items():
            new_cost = current_cost + road_cost

            # Only update if we found a cheaper route to this neighbor
            if new_cost < costs[neighbor]:
                costs[neighbor] = new_cost
                heapq.heappush(frontier, (new_cost, neighbor))

    return costs


def shortest_monster_delivery(
    graph: dict[str, dict[str, int]],
    start: str,
    target: str,
) -> tuple[float, list[str]]:
    """Return the cheapest cost and path from start to target.

    Use Dijkstra's algorithm with heapq and reconstruct the path using
    a previous-node map.

    Args:
        graph: Weighted graph represented as an adjacency dictionary.
        start: Starting location.
        target: Destination location.

    Returns:
        (cost, path), where path is in start-to-target order.
        If start or target is missing, return (math.inf, []).
        If target is unreachable, return (math.inf, []).
        If start equals target, return (0, [start]).
    """
    # If either location doesn't exist, we can't route at all
    if start not in graph or target not in graph:
        return (inf, [])

    # Quick exit — already there
    if start == target:
        return (0, [start])

    # Same setup as monster_delivery_costs, but we also track
    # how we got to each node so we can retrace the path later
    costs = {node: inf for node in graph}
    costs[start] = 0

    previous = {node: None for node in graph}

    frontier = [(0, start)]

    while frontier:
        current_cost, current_node = heapq.heappop(frontier)

        if current_cost > costs[current_node]:
            continue

        # No need to explore further once we've settled the target
        if current_node == target:
            break

        for neighbor, road_cost in graph[current_node].items():
            new_cost = current_cost + road_cost

            if new_cost < costs[neighbor]:
                costs[neighbor] = new_cost
                previous[neighbor] = current_node
                heapq.heappush(frontier, (new_cost, neighbor))

    # If target is still unreachable, return early
    if costs[target] == inf:
        return (inf, [])

    # Retrace the path by walking backwards through the previous map
    path = []
    step = target
    while step is not None:
        path.append(step)
        step = previous[step]

    path.reverse()

    return (costs[target], path)


def best_next_monster_stop(
    graph: dict[str, dict[str, int]],
    start: str,
    targets: list[str],
) -> tuple[str, float]:
    """Return the reachable target with the cheapest delivery cost.

    Stretch challenge.

    Rules:
    - Ignore unreachable targets.
    - If no target is reachable, return ("", math.inf).
    - If there is a tie, return the target that appears first in targets.

    Args:
        graph: Weighted graph represented as an adjacency dictionary.
        start: Starting location.
        targets: Possible destination locations.

    Returns:
        A tuple of (target, cost).
    """
    if start not in graph:
        return ("", inf)

    # Run Dijkstra once from start to get costs to every node
    all_costs = monster_delivery_costs(graph, start)

    best_target = ""
    best_cost = inf

    # Go through targets in order so ties naturally favour the first one
    for target in targets:
        if target not in all_costs:
            continue

        cost = all_costs[target]
        if cost < best_cost:
            best_cost = cost
            best_target = target

    return (best_target, best_cost)