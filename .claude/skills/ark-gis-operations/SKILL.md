---
name: ark-gis-operations
description: Use when performing geospatial operations, coordinate transformations, spatial analysis, or GIS data processing through AI-assisted MCP integration.
triggers:
  - GIS
  - geospatial
  - spatial analysis
  - coordinate transformation
  - geopandas
  - shapely
role: specialist
scope: implementation
output-format: code
---

# GIS Operations MCP Integration

AI-powered geospatial intelligence through Model Context Protocol with 89 GIS functions.

## Prerequisites

- Python 3.10+
- MCP server installed
- GIS libraries (shapely, geopandas, rasterio, pyproj)

## MCP Configuration

Add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "gis": {
      "command": "uvx",
      "args": ["gis-mcp"]
    }
  }
}
```

## Capabilities

- **Geometry Operations** - Buffer, intersection, union, difference
- **Coordinate Transforms** - Reproject between CRS
- **Spatial Analysis** - Proximity, overlay, joins
- **Measurements** - Distance, area, length, centroid
- **Raster Processing** - NDVI, clip, resample, merge
- **Spatial Statistics** - Autocorrelation, clustering
- **Data Gathering** - Climate, biodiversity, satellite imagery

## Function Categories

| Category | Functions | Examples |
|----------|-----------|----------|
| **Shapely** | 29 | buffer, intersection, union |
| **PyProj** | 13 | transform, crs_to_wkt |
| **GeoPandas** | 13 | spatial_join, dissolve |
| **Rasterio** | 20 | ndvi, clip_raster, resample |
| **PySAL** | 18 | moran_i, queen_weights |
| **Visualization** | 2 | static_map, interactive_map |

## Example Prompts

```
"Buffer all points by 500 meters"
"Reproject from EPSG:4326 to EPSG:32610"
"Calculate the intersection of these polygons"
"Generate an NDVI index from the satellite image"
"Find all parcels within 1km of the river"
```

## Coordinate Systems

| EPSG | Name | Use Case |
|------|------|----------|
| 4326 | WGS84 | GPS, global |
| 3857 | Web Mercator | Web maps |
| 32610-32660 | UTM zones | Local measurements |

## Reference Guide

| Topic | Reference | Load When |
|-------|-----------|-----------|
| Setup | `references/setup.md` | Installation |
| Geometry | `references/geometry.md` | Shapely operations |
| Raster | `references/raster.md` | Rasterio processing |
| Statistics | `references/statistics.md` | PySAL analysis |

## Constraints

### MUST DO
- Validate CRS before operations
- Use appropriate projections for measurements
- Handle geometry validation

### MUST NOT DO
- Mix coordinate systems
- Ignore projection distortion
- Process without CRS awareness
