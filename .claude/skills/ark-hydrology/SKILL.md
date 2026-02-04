---
name: ark-hydrology
description: Use when performing watershed analysis, flood modeling, hydrological processing, stream network extraction, or water resource analysis using Python tools.
triggers:
  - hydrology
  - watershed
  - flood analysis
  - stream network
  - flow accumulation
  - drainage
  - HyRiver
  - PyGeoHydro
  - water resources
role: specialist
scope: implementation
output-format: code
---

# Hydrology & Watershed Analysis

Water resource analysis, watershed delineation, and flood modeling tools.

## Core Libraries

| Library | Purpose | Strength |
|---------|---------|----------|
| **HyRiver** | Web service data access | USGS, NHD, NFHL |
| **PyGeoHydro** | Hydroclimate data | Streamflow, FEMA data |
| **Pysheds** | Watershed delineation | Fast, simple |
| **WhiteboxTools** | Terrain hydrology | Flow algorithms |
| **RichDEM** | High-performance DEM | Flow routing |
| **GeoAnalyze** | Full workflow | Basin processing |

## Installation

```bash
pip install pysheds whitebox richdem
pip install pygeohydro pynhd py3dep pydaymet
```

## HyRiver Stack

| Package | Function |
|---------|----------|
| `PyGeoHydro` | Streamflow, FEMA flood |
| `PyNHD` | National Hydrography Dataset |
| `Py3DEP` | 3DEP elevation data |
| `PyDaymet` | Daymet climate data |
| `PyGeoOGC` | OGC web services |

## Watershed Delineation

```python
from pysheds.grid import Grid

# Load DEM
grid = Grid.from_raster('dem.tif')
dem = grid.read_raster('dem.tif')

# Fill depressions
pit_filled = grid.fill_pits(dem)
flooded = grid.fill_depressions(pit_filled)
inflated = grid.resolve_flats(flooded)

# Flow direction & accumulation
fdir = grid.flowdir(inflated)
acc = grid.accumulation(fdir)

# Delineate catchment
catch = grid.catchment(x=lon, y=lat, fdir=fdir)
```

## USGS Data Access

```python
from pygeohydro import NWIS

# Get streamflow data
nwis = NWIS()
stations = nwis.get_info({"stateCd": "CA", "siteType": "ST"})
discharge = nwis.get_streamflow(station_ids, dates)
```

## Common Operations

### Terrain Processing
- Depression filling
- Flow direction (D8, MFD)
- Flow accumulation
- Stream network extraction

### Watershed Analysis
- Catchment delineation
- Subbasin extraction
- Pour point snapping
- Contributing area

### Flood Analysis
- FEMA flood zone access
- Inundation mapping
- Flood frequency analysis
- Stage-discharge curves

## Reference Guide

| Topic | Reference | Load When |
|-------|-----------|-----------|
| Pysheds | `references/pysheds.md` | Watershed delineation |
| HyRiver | `references/hyriver.md` | Web data access |
| Flood | `references/flood-analysis.md` | FEMA, inundation |
| Terrain | `references/terrain-hydro.md` | DEM processing |

## Constraints

### MUST DO
- Fill depressions before flow routing
- Snap pour points to streams
- Validate drainage network
- Use appropriate DEM resolution

### MUST NOT DO
- Route flow on raw DEMs
- Ignore flat areas
- Skip pit filling
- Use coarse DEMs for small basins
