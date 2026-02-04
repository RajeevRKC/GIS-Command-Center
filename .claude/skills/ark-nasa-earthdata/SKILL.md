---
name: ark-nasa-earthdata
description: Use when accessing NASA Earth science data, including Earthdata Search, MODIS, VIIRS, Landsat via earthaccess, NASA POWER climate data, AppEEARS, or Giovanni.
triggers:
  - NASA
  - Earthdata
  - earthaccess
  - MODIS
  - VIIRS
  - NASA POWER
  - AppEEARS
  - Giovanni
  - NASA API
  - Landsat NASA
role: specialist
scope: implementation
output-format: code
---

# NASA Earth Data Access

Comprehensive access to NASA's Earth science data archives and APIs.

## Core Libraries

| Library | Purpose | Data Access |
|---------|---------|-------------|
| **earthaccess** | NASA Earthdata unified API | All NASA DAAC holdings |
| **nasa-power** | Climate/weather data | POWER parameters |
| **harmony-py** | Data transformation | Subsetting, reprojection |
| **requests** | Direct API calls | Giovanni, AppEEARS |

## Installation

```bash
pip install earthaccess harmony-py requests pandas xarray
```

## NASA Data Sources

| Source | Data Type | Access Method |
|--------|-----------|---------------|
| **Earthdata Search** | All NASA Earth data | earthaccess |
| **LP DAAC** | Land data (MODIS, VIIRS) | earthaccess |
| **NSIDC** | Snow/ice data | earthaccess |
| **GES DISC** | Atmosphere data | earthaccess, Giovanni |
| **POWER** | Climate parameters | POWER API |
| **AppEEARS** | Subsetted extracts | AppEEARS API |

## earthaccess Quick Start

```python
import earthaccess

# Authenticate (uses ~/.netrc or prompts)
earthaccess.login()

# Search for data
results = earthaccess.search_data(
    short_name="MCD43A4",  # MODIS BRDF
    bounding_box=(-122.5, 37.5, -122.0, 38.0),
    temporal=("2024-01-01", "2024-12-31"),
    count=10
)

# Download or stream
files = earthaccess.download(results, "./data")

# Or stream directly
ds = earthaccess.open(results)  # Returns xarray
```

## NASA POWER API

```python
import requests
import pandas as pd

# Get daily climate data
url = "https://power.larc.nasa.gov/api/temporal/daily/point"
params = {
    "start": "20240101",
    "end": "20241231",
    "latitude": 37.5,
    "longitude": -122.0,
    "community": "RE",  # Renewable Energy
    "parameters": "T2M,PRECTOTCORR,ALLSKY_SFC_SW_DWN",
    "format": "JSON"
}
response = requests.get(url, params=params)
data = response.json()
```

## Popular Datasets

| Dataset | Short Name | Resolution | Use Case |
|---------|------------|------------|----------|
| MODIS Surface Reflectance | MCD43A4 | 500m | Land cover |
| VIIRS Nightlights | VNP46A2 | 500m | Urban analysis |
| SMAP Soil Moisture | SPL3SMP | 9km | Agriculture |
| GPM Precipitation | GPM_3IMERGDF | 0.1 deg | Hydrology |
| Landsat C2 | HLSS30 | 30m | Change detection |

## MCP Integration

NASA MCP server available:
```json
{
  "mcpServers": {
    "nasa": {
      "command": "npx",
      "args": ["-y", "@programcomputer/nasa-mcp-server@latest"],
      "env": {
        "NASA_API_KEY": "your-api-key"
      }
    }
  }
}
```

Get API key: https://api.nasa.gov/

## Reference Guide

| Topic | Reference | Load When |
|-------|-----------|-----------|
| earthaccess | `references/earthaccess.md` | Data search/download |
| POWER | `references/power-api.md` | Climate data |
| AppEEARS | `references/appeears.md` | Data subsetting |
| Datasets | `references/dataset-catalog.md` | Finding data |

## Constraints

### MUST DO
- Create NASA Earthdata account first
- Store credentials in ~/.netrc
- Respect rate limits
- Check data availability before processing

### MUST NOT DO
- Download without authentication
- Request excessive temporal ranges
- Ignore data quality flags
- Store API keys in code
