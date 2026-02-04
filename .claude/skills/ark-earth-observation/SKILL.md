---
name: ark-earth-observation
description: Use when accessing Earth observation platforms like Google Earth Engine, Planetary Computer, STAC catalogs, or OpenEO for large-scale geospatial analysis.
triggers:
  - Earth Engine
  - GEE
  - Planetary Computer
  - STAC
  - OpenEO
  - cloud computing
  - Earth observation
  - data cube
role: specialist
scope: implementation
output-format: code
---

# Earth Observation Platforms

Cloud-based geospatial analysis and data access for planetary-scale processing.

## Platforms

| Platform | Provider | Strength |
|----------|----------|----------|
| **Google Earth Engine** | Google | Massive archive, free compute |
| **Planetary Computer** | Microsoft | STAC API, cloud-native |
| **OpenEO** | ESA/Copernicus | Standardized processing |
| **AWS Earth** | Amazon | S3 data access |
| **Copernicus Hub** | ESA | Sentinel data source |

## Python Libraries

| Library | Platform | Purpose |
|---------|----------|---------|
| `ee` | Earth Engine | Python API |
| `geemap` | Earth Engine | Mapping interface |
| `pystac-client` | STAC | Catalog search |
| `stackstac` | STAC | xarray loading |
| `odc-stac` | STAC | Open Data Cube |
| `openeo` | OpenEO | Backend connection |

## Installation

```bash
pip install earthengine-api geemap pystac-client stackstac openeo
```

## Google Earth Engine

```python
import ee
ee.Authenticate()
ee.Initialize()

# Load Sentinel-2
s2 = ee.ImageCollection('COPERNICUS/S2_SR') \
    .filterDate('2024-01-01', '2024-12-31') \
    .filterBounds(geometry) \
    .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20))
```

## STAC Catalog Access

```python
from pystac_client import Client

catalog = Client.open("https://planetarycomputer.microsoft.com/api/stac/v1")
search = catalog.search(
    collections=["sentinel-2-l2a"],
    bbox=[-122.5, 37.5, -122.0, 38.0],
    datetime="2024-01-01/2024-12-31"
)
items = search.item_collection()
```

## Data Collections

| Collection | Platform | Coverage |
|------------|----------|----------|
| Sentinel-2 | All | Global, 10m |
| Landsat | All | Global, 30m |
| MODIS | GEE | Global, daily |
| NAIP | PC | US, 1m aerial |
| DEM | All | Global elevation |

## Reference Guide

| Topic | Reference | Load When |
|-------|-----------|-----------|
| GEE | `references/earth-engine.md` | Google processing |
| STAC | `references/stac-access.md` | Catalog searches |
| OpenEO | `references/openeo.md` | ESA backends |
| Cloud-Native | `references/cloud-native.md` | COG/Zarr workflows |

## Constraints

### MUST DO
- Authenticate before API calls
- Use cloud-native formats (COG, Zarr)
- Filter by date and bounds first
- Export results appropriately

### MUST NOT DO
- Download entire collections
- Ignore API quotas
- Skip cloud masking
- Process without spatial filtering
