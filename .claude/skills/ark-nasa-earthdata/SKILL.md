---
name: ark-nasa-earthdata
description: Use when accessing NASA Earth science data, including Earthdata Search, MODIS, VIIRS, Landsat via earthaccess, NASA POWER climate data, api.nasa.gov services (APOD, Mars Rover, NEO, EPIC), or data harvesting and storage.
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
  - APOD
  - Mars Rover
  - asteroids
  - NEO
  - EPIC
  - NASA harvest
role: specialist
scope: implementation
output-format: code
---

# NASA Earth Data Access & Harvesting

Comprehensive access to NASA's Earth science data archives, public APIs, and automated harvesting workflows.

## Two NASA API Systems

| System | Purpose | Auth Method | Key Variable |
|--------|---------|-------------|--------------|
| **Earthdata** | Scientific datasets (MODIS, Landsat, etc.) | JWT Token | `EARTHDATA_TOKEN` |
| **api.nasa.gov** | Public APIs (APOD, Mars, NEO, EPIC) | API Key | `NASA_API_KEY` |

## Core Libraries

| Library | Purpose | Install |
|---------|---------|---------|
| **earthaccess** | NASA Earthdata unified API | `pip install earthaccess` |
| **requests** | api.nasa.gov and direct calls | Built-in |
| **harmony-py** | Data transformation | `pip install harmony-py` |

## api.nasa.gov Services

### APOD - Astronomy Picture of the Day
```python
import requests
import os

API_KEY = os.getenv('NASA_API_KEY', 'DEMO_KEY')

# Get today's APOD
response = requests.get(
    'https://api.nasa.gov/planetary/apod',
    params={'api_key': API_KEY}
)
apod = response.json()
print(f"Title: {apod['title']}")
print(f"URL: {apod['url']}")
```

### Mars Rover Photos
```python
# Get Curiosity photos from sol 1000
response = requests.get(
    'https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos',
    params={
        'sol': 1000,
        'camera': 'FHAZ',
        'api_key': API_KEY
    }
)
photos = response.json()['photos']
```

### NeoWs - Near Earth Objects
```python
# Get asteroids approaching Earth this week
response = requests.get(
    'https://api.nasa.gov/neo/rest/v1/feed',
    params={
        'start_date': '2025-02-01',
        'end_date': '2025-02-07',
        'api_key': API_KEY
    }
)
neo_data = response.json()
```

### EPIC - Earth Imagery
```python
# Get recent Earth images
response = requests.get(
    'https://api.nasa.gov/EPIC/api/natural/images',
    params={'api_key': API_KEY}
)
images = response.json()
```

## Earthdata Scientific Data

### Authentication
```python
import earthaccess
import os

# Method 1: Environment variables
os.environ['EARTHDATA_TOKEN'] = 'your-token'
auth = earthaccess.login(strategy='environment')

# Method 2: Interactive
auth = earthaccess.login(persist=True)  # Saves to ~/.netrc
```

### Search & Download
```python
# Search for MODIS data
results = earthaccess.search_data(
    short_name="MCD43A4",
    bounding_box=(54, 24, 56, 26),  # UAE
    temporal=("2025-01-01", "2025-01-31"),
    count=10
)

# Download to local storage
files = earthaccess.download(results, "./data/modis")

# Or stream directly to xarray
ds = earthaccess.open(results)
```

### Popular Datasets

| Dataset | Short Name | Resolution | Use Case |
|---------|------------|------------|----------|
| MODIS Surface Reflectance | MCD43A4 | 500m | Land cover |
| VIIRS Nightlights | VNP46A2 | 500m | Urban analysis |
| SMAP Soil Moisture | SPL3SMP | 9km | Agriculture |
| GPM Precipitation | GPM_3IMERGDF | 0.1° | Hydrology |
| Landsat HLS | HLSS30 | 30m | Change detection |
| ASTER DEM | ASTGTM | 30m | Terrain |

## NASA POWER Climate API

```python
import requests

url = "https://power.larc.nasa.gov/api/temporal/daily/point"
params = {
    "start": "20250101",
    "end": "20250131",
    "latitude": 25.20,
    "longitude": 55.27,
    "community": "RE",
    "parameters": "T2M,PRECTOTCORR,ALLSKY_SFC_SW_DWN,WS2M",
    "format": "JSON"
}
response = requests.get(url, params=params)
data = response.json()
```

### POWER Parameters

| Parameter | Description |
|-----------|-------------|
| T2M | Temperature at 2m (°C) |
| PRECTOTCORR | Precipitation (mm/day) |
| ALLSKY_SFC_SW_DWN | Solar radiation (kW-hr/m²/day) |
| WS2M | Wind speed at 2m (m/s) |
| RH2M | Relative humidity at 2m (%) |

## Data Harvesting Framework

### Directory Structure
```
data/
├── nasa/
│   ├── apod/           # Astronomy pictures
│   │   └── 2025/
│   │       └── 02/
│   ├── mars/           # Mars rover photos
│   │   └── curiosity/
│   ├── neo/            # Near Earth objects
│   │   └── weekly/
│   ├── epic/           # Earth imagery
│   ├── modis/          # MODIS products
│   ├── landsat/        # Landsat scenes
│   ├── power/          # Climate data
│   └── catalog.json    # Local data index
```

### Harvest APOD Script
```python
"""Harvest NASA Astronomy Picture of the Day"""
import os
import json
import requests
from datetime import datetime, timedelta
from pathlib import Path

def harvest_apod(days=7, output_dir="data/nasa/apod"):
    """Download recent APOD images and metadata"""
    API_KEY = os.getenv('NASA_API_KEY', 'DEMO_KEY')
    base_url = 'https://api.nasa.gov/planetary/apod'

    output = Path(output_dir)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)

    response = requests.get(base_url, params={
        'api_key': API_KEY,
        'start_date': start_date.strftime('%Y-%m-%d'),
        'end_date': end_date.strftime('%Y-%m-%d')
    })

    items = response.json()
    harvested = []

    for item in items:
        date = item['date']
        year, month, _ = date.split('-')

        # Create directory
        dir_path = output / year / month
        dir_path.mkdir(parents=True, exist_ok=True)

        # Save metadata
        meta_file = dir_path / f"{date}.json"
        with open(meta_file, 'w') as f:
            json.dump(item, f, indent=2)

        # Download image if not video
        if item.get('media_type') == 'image':
            img_url = item.get('hdurl') or item['url']
            ext = img_url.split('.')[-1]
            img_file = dir_path / f"{date}.{ext}"

            if not img_file.exists():
                img_data = requests.get(img_url).content
                with open(img_file, 'wb') as f:
                    f.write(img_data)

        harvested.append({'date': date, 'title': item['title']})

    return harvested
```

### Harvest Earthdata
```python
"""Harvest NASA Earthdata products for a region"""
import earthaccess
from pathlib import Path

def harvest_modis(bbox, temporal, output_dir="data/nasa/modis"):
    """Download MODIS surface reflectance for region"""
    auth = earthaccess.login(strategy='environment')

    results = earthaccess.search_data(
        short_name="MCD43A4",
        bounding_box=bbox,
        temporal=temporal
    )

    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)

    files = earthaccess.download(results, str(output))
    return files
```

### Harvest Climate Data
```python
"""Harvest NASA POWER climate data"""
import requests
import json
from pathlib import Path

def harvest_power_climate(lat, lon, start, end, output_dir="data/nasa/power"):
    """Download POWER climate data for location"""
    url = "https://power.larc.nasa.gov/api/temporal/daily/point"
    params = {
        "start": start,
        "end": end,
        "latitude": lat,
        "longitude": lon,
        "community": "RE",
        "parameters": "T2M,PRECTOTCORR,ALLSKY_SFC_SW_DWN,WS2M,RH2M",
        "format": "JSON"
    }

    response = requests.get(url, params=params)
    data = response.json()

    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)

    filename = f"power_{lat}_{lon}_{start}_{end}.json"
    with open(output / filename, 'w') as f:
        json.dump(data, f, indent=2)

    return data
```

## MCP Server Configuration

```json
{
  "mcpServers": {
    "nasa": {
      "command": "npx",
      "args": ["-y", "@programcomputer/nasa-mcp-server@latest"],
      "env": {
        "NASA_API_KEY": "${NASA_API_KEY}"
      }
    }
  }
}
```

## Rate Limits

| Service | Limit | Notes |
|---------|-------|-------|
| api.nasa.gov (DEMO_KEY) | 30/hr, 50/day | For testing only |
| api.nasa.gov (registered) | 1000/hr | Recommended |
| Earthdata | No strict limit | Be respectful |
| POWER | 60/minute | Per parameter |

## Reference Guide

| Topic | Reference | Load When |
|-------|-----------|-----------|
| earthaccess | `references/earthaccess.md` | Scientific data |
| api.nasa.gov | `references/nasa-public-apis.md` | APOD, Mars, NEO |
| POWER | `references/power-api.md` | Climate data |
| Harvesting | `references/harvest-workflows.md` | Bulk downloads |

## Constraints

### MUST DO
- Use registered API key (not DEMO_KEY) for production
- Store credentials in .env, not code
- Implement retry logic for downloads
- Log harvest operations
- Check local cache before re-downloading

### MUST NOT DO
- Exceed rate limits
- Store API keys in version control
- Download without verifying data quality
- Ignore temporal coverage gaps
