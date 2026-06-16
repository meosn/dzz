# Dzz

A small collection of algorithm experiments, data structure prototypes, and routing demos.

## Project map

### `graph-routing/`
Pathfinding and routing experiments on grids and city graphs.

- `weighted-grid-travel-time.py` - weighted grid traversal with terrain-aware travel time.
- `grid-adjacency-draft.py` - early draft for grid-to-graph conversion.
- `grid-dijkstra-demo.py` - a compact shortest-path demo for grid graphs.
- `air-route-a-star.py` - A* route planning for flight-like city networks with fuel constraints.

### `data-structures/`
Linked list and tree experiments focused on core container behavior.

- `singly-linked-list.py` - a custom singly linked list with insert/remove helpers.
- `doubly-linked-list.py` - a more advanced doubly linked list with circular mode support.
- `undo-redo-history.py` - an undo/redo history model built on a doubly linked list.
- `treap.py` - a randomized treap with insert, delete, and console tree output.

### `network-planning/`
Graph-based infrastructure planning.

- `radio-network-prim.py` - a Prim-based prototype for clustered network planning.

## Notes

- These scripts are intentionally kept as separate mini-projects.
- Several files are exploratory or draft-level code; they are preserved for reference, but now live under clearer names.
- If you want, the next step can be splitting each folder into its own GitHub repository.
