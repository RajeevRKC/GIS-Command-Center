---
name: ark-remote-sensing
description: Use when processing satellite imagery, radar data, multispectral analysis, or remote sensing workflows including Sentinel, Landsat, and MODIS data.
triggers:
  - remote sensing
  - satellite imagery
  - Sentinel
  - Landsat
  - MODIS
  - multispectral
  - SAR
  - radar imagery
  - NDVI
  - spectral analysis
role: specialist
scope: implementation
output-format: code
---

# Remote Sensing & Satellite Imagery

Processing and analysis of satellite, aerial, and radar imagery for Earth observation applications.

## Core Libraries

| Library | Purpose | Data Types |
|---------|---------|------------|
| **Satpy** | Meteorological satellites | MSG, GOES, Himawari |
| **sentinelhub** | Sentinel Hub API access | Sentinel-1/2/3/5P |
| **rasterio** | Raster I/O operations | GeoTIFF, COG |
| **xarray** | N-dimensional arrays | NetCDF, Zarr |
| **rioxarray** | Raster + xarray | Cloud-optimized |
| **pyroSAR** | SAR processing | Sentinel-1, TerraSAR |
| **RSGISLib** | Remote sensing ops | Classification, indices |
| **earthpy** | Earth science tools | Vegetation indices |

## Installation

```bash
pip install satpy sentinelhub rasterio xarray rioxarray pyroSAR earthpy
```

## Satellite Sources

| Satellite | Resolution | Revisit | Use Case |
|-----------|------------|---------|----------|
| Sentinel-2 | 10-60m | 5 days | Land cover, NDVI |
| Sentinel-1 | 5-40m | 6 days | SAR, change detection |
| Landsat 8/9 | 15-30m | 16 days | Long-term monitoring |
| MODIS | 250m-1km | Daily | Large-scale trends |
| Planet | 3-5m | Daily | High-res monitoring |

## Common Operations

### Vegetation Indices
- NDVI (Normalized Difference Vegetation Index)
- EVI (Enhanced Vegetation Index)
- SAVI (Soil Adjusted Vegetation Index)
- NDWI (Water Index)

### Spectral Analysis
- Band math and combinations
- Principal Component Analysis
- Spectral unmixing
- Image classification

### SAR Processing
- Radiometric calibration
- Speckle filtering
- Terrain correction
- Coherence analysis

## Reference Guide

| Topic | Reference | Load When |
|-------|-----------|-----------|
| Sentinel | `references/sentinel.md` | Copernicus data |
| SAR | `references/sar-processing.md` | Radar imagery |
| Indices | `references/spectral-indices.md` | Band calculations |
| Classification | `references/classification.md` | ML workflows |

## Constraints

### MUST DO
- Check cloud coverage before processing
- Apply atmospheric correction when needed
- Validate CRS and resolution
- Use COG format for large files

### MUST NOT DO
- Process without cloud masking
- Ignore radiometric calibration
- Mix sensors without resampling
- Skip quality assessment bands
