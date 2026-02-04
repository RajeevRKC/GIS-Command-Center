---
name: ark-lidar-pointcloud
description: Use when processing LiDAR data, point clouds, terrain analysis, or 3D point data using PDAL, whitebox, or Open3D.
triggers:
  - LiDAR
  - point cloud
  - terrain analysis
  - DEM generation
  - PDAL
  - whitebox
  - elevation model
  - LAZ
  - LAS
role: specialist
scope: implementation
output-format: code
---

# LiDAR & Point Cloud Processing

Processing and analysis of 3D point cloud data for terrain modeling and feature extraction.

## Core Libraries

| Library | Purpose | Strength |
|---------|---------|----------|
| **PDAL** | Point Data Abstraction | Pipeline processing |
| **whitebox** | Geospatial analysis | Terrain algorithms |
| **laspy** | LAS/LAZ I/O | File manipulation |
| **Open3D** | 3D processing | Visualization, ML |
| **pylidar** | LiDAR tools | Canopy analysis |
| **lidar** | Terrain/hydro | Watershed analysis |

## Installation

```bash
pip install pdal laspy whitebox open3d
conda install -c conda-forge pdal python-pdal
```

## File Formats

| Format | Extension | Description |
|--------|-----------|-------------|
| LAS | .las | Standard point cloud |
| LAZ | .laz | Compressed LAS |
| E57 | .e57 | 3D imaging format |
| PLY | .ply | Polygon file format |
| PCD | .pcd | Point Cloud Data |

## Common Operations

### Terrain Products
- DEM/DTM generation
- DSM (surface model)
- Canopy Height Model (CHM)
- Slope and aspect
- Hillshade

### Point Cloud Processing
- Ground classification
- Noise filtering
- Thinning/decimation
- Clip to boundary
- Merge tiles

### Hydrology
- Flow accumulation
- Stream network extraction
- Watershed delineation
- Depression filling

## PDAL Pipeline Example

```json
{
  "pipeline": [
    "input.laz",
    {"type": "filters.assign", "assignment": "Classification[:]=0"},
    {"type": "filters.smrf"},
    {"type": "writers.gdal", "filename": "dem.tif", "resolution": 1.0}
  ]
}
```

## Reference Guide

| Topic | Reference | Load When |
|-------|-----------|-----------|
| PDAL | `references/pdal-pipelines.md` | Pipeline workflows |
| Terrain | `references/terrain-analysis.md` | DEM products |
| Classification | `references/point-classification.md` | Ground filtering |
| Hydrology | `references/hydro-analysis.md` | Watershed work |

## Constraints

### MUST DO
- Check point density before processing
- Use appropriate ground classification
- Validate coordinate system
- Consider memory for large datasets

### MUST NOT DO
- Process without filtering noise
- Ignore vertical datum
- Generate DEMs from unclassified data
- Skip void filling in outputs
