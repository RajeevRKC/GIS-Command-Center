---
name: ark-network-analysis
description: Use when performing geospatial network analysis, street routing, transportation modeling, isochrone analysis, or OpenStreetMap network processing with OSMnx and NetworkX.
triggers:
  - network analysis
  - routing
  - OSMnx
  - street network
  - transportation
  - isochrone
  - shortest path
  - accessibility analysis
  - NetworkX geospatial
role: specialist
scope: implementation
output-format: code
---

# Geospatial Network Analysis

Street network modeling, routing, and transportation analysis.

## Core Libraries

| Library | Purpose | Use Case |
|---------|---------|----------|
| **OSMnx** | OSM network download | Street networks |
| **NetworkX** | Graph analysis | Algorithms, metrics |
| **pandana** | Accessibility analysis | POI queries |
| **momepy** | Urban morphology | Street patterns |
| **pyrosm** | Fast OSM parsing | Large extracts |

## Installation

```bash
pip install osmnx networkx pandana momepy pyrosm
```

## OSMnx Quick Start

```python
import osmnx as ox

# Download street network
G = ox.graph_from_place("San Francisco, California", network_type="drive")

# Basic stats
stats = ox.basic_stats(G)

# Plot network
fig, ax = ox.plot_graph(G)

# Save to file
ox.save_graphml(G, "sf_network.graphml")
```

## Network Types

| Type | Description | Use Case |
|------|-------------|----------|
| `drive` | Drivable streets | Vehicle routing |
| `walk` | Walkable paths | Pedestrian analysis |
| `bike` | Bikeable routes | Cycling infrastructure |
| `all` | All OSM ways | Complete network |
| `all_private` | Including private | Full coverage |

## Routing & Shortest Path

```python
import osmnx as ox
import networkx as nx

# Get network with travel times
G = ox.graph_from_place("Berkeley, CA", network_type="drive")
G = ox.add_edge_speeds(G)
G = ox.add_edge_travel_times(G)

# Find nearest nodes
orig = ox.nearest_nodes(G, X=orig_lon, Y=orig_lat)
dest = ox.nearest_nodes(G, X=dest_lon, Y=dest_lat)

# Shortest path by travel time
route = nx.shortest_path(G, orig, dest, weight="travel_time")

# Plot route
fig, ax = ox.plot_graph_route(G, route)
```

## Isochrone Analysis

```python
# Get subgraph within travel time
trip_time = 15  # minutes
subgraph = nx.ego_graph(G, center_node, radius=trip_time*60, distance="travel_time")

# Get convex hull of reachable nodes
isochrone = ox.graph_to_gdfs(subgraph, edges=False).unary_union.convex_hull
```

## Network Metrics

| Metric | Function | Measures |
|--------|----------|----------|
| Degree | `G.degree()` | Connectivity |
| Betweenness | `nx.betweenness_centrality()` | Flow importance |
| Closeness | `nx.closeness_centrality()` | Accessibility |
| Circuity | `ox.basic_stats()` | Route directness |

## Reference Guide

| Topic | Reference | Load When |
|-------|-----------|-----------|
| OSMnx | `references/osmnx.md` | Network download |
| Routing | `references/routing.md` | Path finding |
| Metrics | `references/network-metrics.md` | Analysis |
| Accessibility | `references/accessibility.md` | Isochrones, POI |

## Constraints

### MUST DO
- Simplify networks for analysis
- Use appropriate network type
- Project to local CRS for distances
- Handle disconnected components

### MUST NOT DO
- Use unprojected coords for distances
- Ignore one-way streets
- Skip network simplification
- Assume full connectivity
