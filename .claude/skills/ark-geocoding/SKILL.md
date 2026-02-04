---
name: ark-geocoding
description: Use when converting addresses to coordinates, reverse geocoding, batch geocoding, or accessing location services APIs like Nominatim, Google, or Mapbox.
triggers:
  - geocoding
  - address to coordinates
  - reverse geocoding
  - location services
  - Nominatim
  - GeoPy
  - address lookup
  - batch geocoding
role: specialist
scope: implementation
output-format: code
---

# Geocoding & Location Services

Address-to-coordinate conversion and location intelligence services.

## Core Libraries

| Library | Purpose | Providers |
|---------|---------|-----------|
| **GeoPy** | Unified geocoding | 20+ providers |
| **pgeocode** | Postal codes | Global postal data |
| **geocoder** | Simple interface | Multiple APIs |
| **Nominatim** | OpenStreetMap | Free, rate-limited |

## Installation

```bash
pip install geopy pgeocode geocoder
```

## Provider Comparison

| Provider | Free Tier | Rate Limit | Accuracy |
|----------|-----------|------------|----------|
| Nominatim | Unlimited | 1 req/sec | Good |
| Google | $200/mo | 50 QPS | Excellent |
| Mapbox | 100k/mo | 600/min | Excellent |
| HERE | 250k/mo | 30 QPS | Excellent |
| Bing | 125k/yr | 10 QPS | Good |
| TomTom | 2.5k/day | 5 QPS | Excellent |

## Quick Start

### GeoPy (Nominatim)
```python
from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="my_app")

# Forward geocoding
location = geolocator.geocode("1600 Pennsylvania Ave, Washington DC")
print(location.latitude, location.longitude)

# Reverse geocoding
address = geolocator.reverse("38.8977, -77.0365")
print(address.address)
```

### Batch Geocoding
```python
from geopy.extra.rate_limiter import RateLimiter
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
df['coords'] = df['address'].apply(geocode)
```

## Common Operations

### Forward Geocoding
- Address to coordinates
- Place name lookup
- POI search

### Reverse Geocoding
- Coordinates to address
- Nearest address
- Admin boundaries

### Batch Processing
- CSV/DataFrame geocoding
- Rate-limited requests
- Error handling

## MCP Integration

TomTom MCP server available:
```json
{
  "mcpServers": {
    "tomtom": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-server-tomtom"]
    }
  }
}
```

## Reference Guide

| Topic | Reference | Load When |
|-------|-----------|-----------|
| GeoPy | `references/geopy.md` | Provider setup |
| Batch | `references/batch-geocoding.md` | Large datasets |
| Validation | `references/address-validation.md` | Quality checks |
| Caching | `references/geocode-caching.md` | Performance |

## Constraints

### MUST DO
- Respect rate limits
- Cache geocoding results
- Handle API errors gracefully
- Use appropriate provider for region

### MUST NOT DO
- Hammer free APIs
- Store API keys in code
- Skip address normalization
- Ignore geocoding confidence scores
