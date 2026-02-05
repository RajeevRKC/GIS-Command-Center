# NASA Public APIs (api.nasa.gov)

Free APIs for public NASA data - no Earthdata account required.

## Authentication

Get API key at: https://api.nasa.gov/

```python
import os
API_KEY = os.getenv('NASA_API_KEY', 'DEMO_KEY')
```

**Rate Limits:**
- DEMO_KEY: 30 requests/hour, 50/day
- Registered: 1000 requests/hour

---

## APOD - Astronomy Picture of the Day

**Endpoint:** `https://api.nasa.gov/planetary/apod`

### Basic Request
```python
import requests

response = requests.get(
    'https://api.nasa.gov/planetary/apod',
    params={'api_key': API_KEY}
)
apod = response.json()
```

### Parameters
| Param | Type | Description |
|-------|------|-------------|
| date | YYYY-MM-DD | Specific date |
| start_date | YYYY-MM-DD | Range start |
| end_date | YYYY-MM-DD | Range end |
| count | int | Random images |
| thumbs | bool | Include video thumbnails |

### Response Fields
```json
{
  "date": "2025-02-05",
  "title": "Image Title",
  "explanation": "Scientific description...",
  "url": "https://apod.nasa.gov/apod/image/...",
  "hdurl": "https://apod.nasa.gov/apod/image/.../hd.jpg",
  "media_type": "image",
  "copyright": "Author Name"
}
```

### Date Range Example
```python
# Get last 7 days
from datetime import datetime, timedelta

end = datetime.now()
start = end - timedelta(days=7)

response = requests.get(
    'https://api.nasa.gov/planetary/apod',
    params={
        'api_key': API_KEY,
        'start_date': start.strftime('%Y-%m-%d'),
        'end_date': end.strftime('%Y-%m-%d')
    }
)
images = response.json()  # Returns list
```

---

## Mars Rover Photos

**Endpoint:** `https://api.nasa.gov/mars-photos/api/v1/rovers/{rover}/photos`

### Rovers Available
| Rover | Status | Cameras |
|-------|--------|---------|
| curiosity | Active | FHAZ, RHAZ, MAST, CHEMCAM, MAHLI, MARDI, NAVCAM |
| opportunity | Complete | FHAZ, RHAZ, NAVCAM, PANCAM, MINITES |
| spirit | Complete | FHAZ, RHAZ, NAVCAM, PANCAM, MINITES |
| perseverance | Active | EDL_RUCAM, EDL_RDCAM, EDL_DDCAM, EDL_PUCAM1/2, NAVCAM_LEFT/RIGHT, MCZ_LEFT/RIGHT, FRONT_HAZCAM_LEFT/RIGHT, REAR_HAZCAM_LEFT/RIGHT, SKYCAM, SHERLOC_WATSON |

### By Sol (Martian Day)
```python
response = requests.get(
    'https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos',
    params={
        'sol': 1000,
        'camera': 'FHAZ',
        'api_key': API_KEY
    }
)
```

### By Earth Date
```python
response = requests.get(
    'https://api.nasa.gov/mars-photos/api/v1/rovers/perseverance/photos',
    params={
        'earth_date': '2025-01-15',
        'api_key': API_KEY
    }
)
```

### Response
```json
{
  "photos": [
    {
      "id": 102693,
      "sol": 1000,
      "camera": {"name": "FHAZ", "full_name": "Front Hazard Avoidance Camera"},
      "img_src": "http://mars.jpl.nasa.gov/...",
      "earth_date": "2015-05-30",
      "rover": {"name": "Curiosity", "status": "active"}
    }
  ]
}
```

### Get Rover Manifest
```python
response = requests.get(
    f'https://api.nasa.gov/mars-photos/api/v1/manifests/curiosity',
    params={'api_key': API_KEY}
)
manifest = response.json()['photo_manifest']
print(f"Total photos: {manifest['total_photos']}")
print(f"Max sol: {manifest['max_sol']}")
```

---

## NeoWs - Near Earth Object Web Service

**Endpoint:** `https://api.nasa.gov/neo/rest/v1/`

### Feed (By Date Range)
```python
response = requests.get(
    'https://api.nasa.gov/neo/rest/v1/feed',
    params={
        'start_date': '2025-02-01',
        'end_date': '2025-02-07',
        'api_key': API_KEY
    }
)
neo_data = response.json()

# Access objects by date
for date, asteroids in neo_data['near_earth_objects'].items():
    print(f"{date}: {len(asteroids)} asteroids")
    for ast in asteroids:
        name = ast['name']
        diameter = ast['estimated_diameter']['meters']['estimated_diameter_max']
        hazardous = ast['is_potentially_hazardous_asteroid']
        print(f"  {name}: {diameter:.0f}m, hazardous={hazardous}")
```

### Lookup Specific Asteroid
```python
asteroid_id = '3542519'
response = requests.get(
    f'https://api.nasa.gov/neo/rest/v1/neo/{asteroid_id}',
    params={'api_key': API_KEY}
)
```

### Browse All
```python
response = requests.get(
    'https://api.nasa.gov/neo/rest/v1/neo/browse',
    params={'api_key': API_KEY}
)
```

---

## EPIC - Earth Polychromatic Imaging Camera

**Endpoint:** `https://api.nasa.gov/EPIC/api/`

### Get Natural Color Images
```python
response = requests.get(
    'https://api.nasa.gov/EPIC/api/natural/images',
    params={'api_key': API_KEY}
)
images = response.json()
```

### Get Enhanced Images
```python
response = requests.get(
    'https://api.nasa.gov/EPIC/api/enhanced/images',
    params={'api_key': API_KEY}
)
```

### Get Specific Date
```python
response = requests.get(
    'https://api.nasa.gov/EPIC/api/natural/date/2025-01-15',
    params={'api_key': API_KEY}
)
```

### Image URL Construction
```python
# From response
image = images[0]
date = image['date'].split(' ')[0].replace('-', '/')
filename = image['image']

# Natural color
url = f"https://epic.gsfc.nasa.gov/archive/natural/{date}/png/{filename}.png"

# Enhanced
url = f"https://epic.gsfc.nasa.gov/archive/enhanced/{date}/png/{filename}.png"
```

---

## EONET - Earth Observatory Natural Event Tracker

**Endpoint:** `https://eonet.gsfc.nasa.gov/api/v3/`

### Get Recent Events
```python
response = requests.get(
    'https://eonet.gsfc.nasa.gov/api/v3/events',
    params={'limit': 10}
)
events = response.json()['events']
```

### Filter by Category
```python
# Categories: wildfires, severeStorms, volcanoes, seaLakeIce, etc.
response = requests.get(
    'https://eonet.gsfc.nasa.gov/api/v3/events',
    params={
        'category': 'wildfires',
        'status': 'open',
        'limit': 20
    }
)
```

### Event Response
```json
{
  "id": "EONET_6448",
  "title": "Wildfire - California",
  "categories": [{"id": "wildfires", "title": "Wildfires"}],
  "geometry": [
    {"date": "2025-01-15", "type": "Point", "coordinates": [-122.5, 37.8]}
  ]
}
```

---

## NASA Image and Video Library

**Endpoint:** `https://images-api.nasa.gov/`

### Search
```python
response = requests.get(
    'https://images-api.nasa.gov/search',
    params={
        'q': 'apollo 11',
        'media_type': 'image'
    }
)
```

### Asset Details
```python
nasa_id = 'as11-40-5874'
response = requests.get(f'https://images-api.nasa.gov/asset/{nasa_id}')
```

---

## Error Handling

```python
def nasa_api_request(url, params):
    """Make NASA API request with error handling"""
    try:
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        if response.status_code == 429:
            print("Rate limit exceeded. Wait and retry.")
        elif response.status_code == 403:
            print("Invalid API key")
        raise
    except requests.exceptions.Timeout:
        print("Request timed out")
        raise
```
