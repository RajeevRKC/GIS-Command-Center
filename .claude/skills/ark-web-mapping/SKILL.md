---
name: ark-web-mapping
description: Use when creating interactive web maps, geospatial visualizations, or browser-based mapping applications using Folium, Leafmap, deck.gl, or MapLibre.
triggers:
  - web map
  - interactive map
  - Folium
  - Leafmap
  - deck.gl
  - MapLibre
  - Leaflet
  - map visualization
  - geospatial visualization
role: specialist
scope: implementation
output-format: code
---

# Web Mapping & Visualization

Interactive geospatial visualization for web applications and Jupyter notebooks.

## Core Libraries

| Library | Type | Best For |
|---------|------|----------|
| **Folium** | Python/Leaflet | Quick interactive maps |
| **Leafmap** | Python/ipyleaflet | Jupyter + Earth Engine |
| **ipyleaflet** | Jupyter widgets | Interactive notebooks |
| **pydeck** | Python/deck.gl | Large-scale 3D viz |
| **lonboard** | Python/deck.gl | Fast GeoDataFrame viz |
| **Mapbox GL JS** | JavaScript | Custom web apps |
| **MapLibre GL** | JavaScript | Open-source vector maps |

## Installation

```bash
pip install folium leafmap pydeck lonboard ipyleaflet
```

## Quick Start

### Folium (Simple Maps)
```python
import folium
m = folium.Map(location=[lat, lon], zoom_start=12)
folium.Marker([lat, lon], popup="Location").add_to(m)
m.save("map.html")
```

### Leafmap (Jupyter)
```python
import leafmap
m = leafmap.Map(center=[lat, lon], zoom=10)
m.add_geojson("data.geojson")
m
```

### Pydeck (Large Datasets)
```python
import pydeck as pdk
layer = pdk.Layer("ScatterplotLayer", data=df, ...)
deck = pdk.Deck(layers=[layer])
deck.to_html("viz.html")
```

## Layer Types

| Layer | Use Case | Library |
|-------|----------|---------|
| Markers | Point locations | Folium, Leafmap |
| Choropleth | Thematic mapping | Folium, Pydeck |
| Heatmap | Density visualization | Folium, Pydeck |
| 3D Extrusion | Building heights | Pydeck, MapLibre |
| Vector Tiles | Large datasets | MapLibre, Pydeck |
| Raster Tiles | Satellite imagery | Leafmap, Folium |

## Basemaps

| Provider | Style | Access |
|----------|-------|--------|
| OpenStreetMap | Standard | Free |
| CartoDB | Light/Dark | Free |
| Stamen | Terrain/Toner | Free |
| Mapbox | Custom | API key |
| Google | Satellite | API key |

## Reference Guide

| Topic | Reference | Load When |
|-------|-----------|-----------|
| Folium | `references/folium.md` | Quick maps |
| Pydeck | `references/pydeck.md` | Large data |
| Styling | `references/map-styling.md` | Custom appearance |
| Interactivity | `references/interactivity.md` | User interaction |

## Constraints

### MUST DO
- Set appropriate zoom levels
- Use clustering for many points
- Optimize GeoJSON file sizes
- Add attribution for basemaps

### MUST NOT DO
- Load millions of points directly
- Ignore mobile responsiveness
- Skip coordinate validation
- Use unlicensed basemaps
