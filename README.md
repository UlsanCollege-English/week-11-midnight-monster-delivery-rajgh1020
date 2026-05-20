[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/ulyILqqB)
# Weekly Coding #9: Midnight Monster Delivery

## Summary

This program finds the cheapest delivery routes through a haunted city full of supernatural customers. Each location is a node in a weighted graph, and each haunted road between them has a positive travel cost. The program uses Dijkstra's algorithm with a heap-based priority queue to always expand the cheapest known route first. It can return either the cost to every location at once, or the cost and full path to a specific destination.

## Approach

- **Graph representation:** The graph is an adjacency dictionary where each key is a location and each value is a dictionary of neighbors with their road costs.
- **Priority queue / frontier:** A min-heap (`heapq`) holds tuples of `(cost_so_far, location)`. The heap always gives us the cheapest unvisited location next, which is the core idea of Dijkstra's.
- **Relaxation:** For each node we pop off the heap, we check every neighbor. If the cost to reach that neighbor through the current node is cheaper than what we already know, we update the cost and push the neighbor onto the heap.
- **Path reconstruction:** In `shortest_monster_delivery`, a `previous` dictionary tracks how we arrived at each node. Once we reach the target, we walk backwards through `previous` from target to start, then reverse the list to get the correct order.

## Complexity

```text
Time complexity: O((V + E) log V), where V is the number of locations and E is the number of roads.

Space complexity: O(V) extra space for distances, previous nodes, and the frontier.
If we include graph storage, the total is O(V + E).
```

- **`monster_delivery_costs`:**
  - Time: O((V + E) log V) — every node is pushed to the heap at most once per incoming edge, and each heap operation costs O(log V).
  - Space: O(V) — we store one cost entry per node plus the heap itself, which holds at most V entries at a time.
  - Why: We visit every node and every edge at most once. Each time we find a cheaper path we push to the heap, so heap size is bounded by the number of edges.

- **`shortest_monster_delivery`:**
  - Time: O((V + E) log V) — same as above. We stop early once the target is popped, but worst case is the same.
  - Space: O(V) — same costs dictionary plus an additional `previous` dictionary, both of size V.
  - Why: The `previous` map adds one extra entry per node but doesn't change the overall space class.

## Edge-Case Checklist

- [x] start equals target — returns `(0, [start])` immediately
- [x] target is unreachable — returns `(inf, [])`
- [x] start node is missing — raises `ValueError` in `monster_delivery_costs`, returns `(inf, [])` in `shortest_monster_delivery`
- [x] target node is missing — returns `(inf, [])`
- [x] node has no outgoing edges — treated as a dead end; costs stay `inf` for nodes only reachable through it
- [x] graph contains cycles — the `current_cost > costs[node]` guard prevents re-processing already-settled nodes
- [x] tied shortest paths — either valid path is accepted
- [x] negative edge weight — caught by `validate_haunted_map`, raises `ValueError`
- [x] zero edge weight — caught by `validate_haunted_map`, raises `ValueError`
- [x] neighbor not listed as a graph node — caught by `validate_haunted_map`, raises `ValueError`

## Tests I Added

- `test_validate_haunted_map_rejects_non_dict` — checks that passing a non-dict raises `ValueError`
- `test_validate_haunted_map_rejects_non_dict_neighbors` — checks that a node with a list instead of dict raises `ValueError`
- `test_validate_haunted_map_accepts_node_with_no_outgoing_edges` — confirms a dead-end node is valid
- `test_monster_delivery_costs_single_node_graph` — a single-node graph should return cost 0 for that node
- `test_monster_delivery_costs_prefers_cheaper_longer_path` — confirms Dijkstra picks the lower-cost multi-hop route over a direct expensive one
- `test_shortest_monster_delivery_direct_edge` — confirms a direct edge beats a longer route even if both reach the target
- `test_best_next_monster_stop_returns_cheapest` — stretch: picks the cheapest reachable target from a list
- `test_best_next_monster_stop_tie_returns_first_in_list` — stretch: on a tie, the first target in the list wins
- `test_best_next_monster_stop_all_unreachable` — stretch: returns `("", inf)` when nothing is reachable
- `test_best_next_monster_stop_missing_start` — stretch: returns `("", inf)` when start isn't in the graph

## Assistance & Sources

AI used? Y

- Used to review overall code structure and README formatting.

Other sources used:

- Course notes on Dijkstra's algorithm and heaps

## Notes for Instructor

Implemented the stretch function `best_next_monster_stop` as well. It reuses `monster_delivery_costs` to get all distances in one pass, then scans the targets list in order so ties naturally resolve to the first one.