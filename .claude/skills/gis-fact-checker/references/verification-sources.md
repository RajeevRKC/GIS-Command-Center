# Verification Sources Reference

Authoritative sources for validating geospatial claims, organized by tier and domain.

---

## Tier 1: Authoritative Sources

### Satellite Imagery & Earth Observation

**USGS EarthExplorer**
- URL: https://earthexplorer.usgs.gov/
- Coverage: Landsat (1972-present), ASTER, aerial photography
- Use for: Imagery acquisition dates, resolution specs, scene metadata
- Verification: Search by coordinates, download metadata files

**Copernicus Open Access Hub**
- URL: https://scihub.copernicus.eu/
- Coverage: Sentinel-1 (SAR), Sentinel-2 (optical), Sentinel-3 (ocean/land)
- Use for: Sentinel data specifications, acquisition dates, processing levels
- Verification: Query API by date/location, check product specifications

**NASA Earthdata**
- URL: https://earthdata.nasa.gov/
- Coverage: MODIS, Landsat, SRTM, ASTER GDEM
- Use for: Product specifications, temporal resolution, band definitions
- Verification: Check product documentation, DOI references

### Coordinate Reference Systems

**EPSG.io**
- URL: https://epsg.io/
- Coverage: 6000+ coordinate reference systems
- Use for: EPSG code verification, projection parameters, area of use
- Verification: Search by code or name, compare WKT definitions
- Example: EPSG:4326 (WGS84 geographic) vs EPSG:3857 (Web Mercator)

**Spatial Reference**
- URL: https://spatialreference.org/
- Coverage: EPSG, ESRI, OGC definitions
- Use for: Cross-platform CRS definitions, conversion parameters
- Verification: Compare formats (WKT, Proj4, GeoJSON)

### Administrative Boundaries

**GADM (Global Administrative Areas)**
- URL: https://gadm.org/
- Coverage: 400,000+ administrative areas worldwide
- Use for: Country/province/district boundary verification
- Verification: Download shapefiles, compare geometries
- Current version: 4.1 (check for updates)

**Natural Earth**
- URL: https://www.naturalearthdata.com/
- Coverage: Cultural and physical vector data at 1:10m, 1:50m, 1:110m
- Use for: Coastlines, borders, populated places
- Verification: Download reference data, visual comparison

---

## Tier 2: Community Sources

### OpenStreetMap (OSM)

**Main Database**
- URL: https://www.openstreetmap.org/
- Coverage: Global crowdsourced geographic data
- Use for: Place names, road networks, land use verification
- Verification: Query Overpass API, visual inspection
- Data quality: Variable by region, check edit history

**Overpass Turbo**
- URL: https://overpass-turbo.eu/
- Use for: Querying OSM data by tag, bounding box
- Example: `[out:json]; node["name"="Location Name"](bbox); out;`

**Nominatim**
- URL: https://nominatim.openstreetmap.org/
- Use for: Geocoding verification, place name resolution
- Verification: Reverse geocode coordinates, compare results

### National Mapping Agencies

**USGS National Map**
- URL: https://www.usgs.gov/programs/national-geospatial-program/national-map
- Coverage: US topographic maps, elevation, land cover
- Use for: US-specific verification, USGS product validation

**Ordnance Survey (UK)**
- URL: https://www.ordnancesurvey.co.uk/
- Coverage: UK mapping products
- Use for: UK coordinate verification, place names

**Geoscience Australia**
- URL: https://www.ga.gov.au/
- Coverage: Australian geodetic, topographic data
- Use for: Australian coordinate systems, boundary verification

---

## Tier 3: Derived Products

### Indices & Derived Datasets

**MODIS NDVI Products**
- Product: MOD13Q1 (250m), MOD13A1 (500m)
- Documentation: https://lpdaac.usgs.gov/products/mod13q1v006/
- Use for: Validating NDVI value ranges, temporal compositing
- Verification: Download product, compare algorithms

**Global Forest Change**
- URL: https://earthenginepartners.appspot.com/science-2013-global-forest
- Coverage: 2000-2022 forest loss/gain
- Use for: Forest change claims, tree cover percentage
- Verification: Compare pixel values, check dataset version

**WorldClim**
- URL: https://www.worldclimate.org/
- Coverage: Global climate surfaces (temperature, precipitation)
- Use for: Climate variable verification
- Verification: Extract values by coordinates, compare interpolation methods

### Commercial Providers (with documentation)

**Planet Labs**
- Resolution: 3-5m (PlanetScope), 0.5m (SkySat)
- Use for: High-resolution imagery claims (with access)
- Verification: Check product specifications, licensing

**Maxar (DigitalGlobe)**
- Resolution: 0.3m-0.5m
- Use for: Very high-resolution imagery verification
- Verification: Confirm access, check collection dates

---

## Verification Protocols by Claim Type

### Coordinates

1. Range check: lat ∈ [-90, 90], lon ∈ [-180, 180]
2. Reverse geocode via Nominatim or GADM
3. Visual verification on base map (OSM, Natural Earth)
4. Compare with known reference points

### Projections

1. Query EPSG.io by code
2. Verify area of use matches claim location
3. Check projection type (geographic, projected, geocentric)
4. Confirm datum (WGS84, NAD83, etc.)
5. Validate against source data CRS

### Areas/Distances

1. Identify claimed values and units
2. Check projection used for calculation
3. Re-compute using appropriate projected CRS (e.g., UTM for region)
4. Compare planar vs geodesic calculations
5. Verify against known reference areas (countries, lakes)

### Data Recency

1. Extract claimed date and source
2. Query provider catalog (EarthExplorer, Copernicus)
3. Distinguish acquisition vs processing vs publication dates
4. Check for updated versions
5. Verify temporal resolution (daily, 8-day composite, annual)

### Resolution/Scale

1. Identify claimed spatial resolution
2. Check source data specifications
3. Verify pixel size in native CRS
4. Check for resampling (upscaling vs downscaling)
5. Validate map scale calculation (1:scale = ground distance / map distance)

### Attribution

1. Identify all data sources
2. Check provider license requirements:
   - Copernicus: "Modified Copernicus Sentinel data [year]"
   - Landsat: "Courtesy of the U.S. Geological Survey"
   - OSM: "© OpenStreetMap contributors"
3. Verify dataset version citations
4. Confirm DOI or persistent identifier usage

---

## Quick Reference: Common Data Specifications

| Dataset | Resolution | Temporal | Bands | Attribution Required |
|---------|-----------|----------|-------|---------------------|
| Landsat 8 | 30m (15m pan) | 16-day | 11 | Yes - USGS |
| Sentinel-2 | 10m/20m/60m | 5-day | 13 | Yes - Copernicus |
| MODIS | 250m/500m/1km | Daily/8-day | 36 | Yes - NASA |
| SRTM | 30m (90m global) | 2000 (one-time) | 1 (elevation) | Yes - NASA/NGA |
| Planet | 3-5m | Daily | 4 | Yes - Commercial |

---

## Verification Workflow Template

```
Claim: [State the geospatial claim]
Category: [coordinate_accuracy | projection_systems | area_distance | data_recency | etc.]

Verification Method:
1. [First verification step]
2. [Second verification step]
3. [Third verification step]

Sources Consulted:
- [Tier 1 source]: [URL] - [Result]
- [Tier 2 source]: [URL] - [Result]

Evidence:
- [Screenshot/data/calculation]
- [Query result]

Finding: [VERIFIED | LIKELY | UNVERIFIABLE | CONTRADICTED]
Confidence: [HIGH | MEDIUM | LOW]
Notes: [Additional context]
```

---

## Search Query Templates

### EPSG.io
```
https://epsg.io/?q=[search term]
Example: https://epsg.io/32637 (UTM Zone 37N)
```

### Nominatim Reverse Geocode
```
https://nominatim.openstreetmap.org/reverse?lat=[lat]&lon=[lon]&format=json
```

### Copernicus Data Space
```
Search API: https://catalogue.dataspace.copernicus.eu/resto/api/collections/[collection]/search.json
Example collection: Sentinel2
Parameters: startDate, completionDate, geometry
```

### USGS M2M API
```
Endpoint: https://m2m.cr.usgs.gov/api/api/json/stable/
Methods: datasetSearch, sceneSearch, downloadOptions
Requires: Authentication token
```

---

*Updated: 2026-02-06*
*For latest data source URLs and API endpoints, verify provider documentation*
