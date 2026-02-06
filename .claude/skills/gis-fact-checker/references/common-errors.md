# Common GIS Errors Reference

Frequently encountered errors in geospatial analysis claims, with detection methods and corrections.

---

## Projection & Coordinate System Errors

### 1. Wrong EPSG Code for Data Type

**Error Pattern:**
- Using EPSG:4326 (WGS84 geographic) for projected data
- Using EPSG:3857 (Web Mercator) for geodesic calculations
- Claiming UTM zone without specifying hemisphere (N/S)

**Detection:**
- Check if data is described as "projected" but uses geographic EPSG
- Verify coordinate values: geographic (±180, ±90) vs projected (large numbers)
- Query EPSG.io to confirm projection type

**Example:**
```
WRONG: "Area calculated in EPSG:4326"
(4326 is geographic - no area units)

RIGHT: "Area calculated in EPSG:32637 (UTM Zone 37N)"
(32637 is projected - meters)
```

**Correction:**
Identify appropriate projected CRS for region:
- UTM zones: EPSG:326xx (North) or 327xx (South), where xx = zone number
- National grids: OSGB36 (UK), GDA94 (Australia), etc.

---

### 2. Geographic vs Projected Confusion

**Error Pattern:**
- Reporting area in "square degrees"
- Distance in degrees instead of meters/kilometers
- Mixing geographic and projected coordinates

**Detection:**
- Check units in calculations
- Verify if units match projection type
- Look for degree symbols (°) in area/distance claims

**Example:**
```
WRONG: "Area: 0.25 square degrees"
(Meaningless - degrees are not area units)

RIGHT: "Area: 777 km² (calculated in UTM Zone 37N)"
```

**Correction:**
- Reproject to appropriate UTM or equal-area projection
- Recalculate using projected coordinates
- Report units: m², km², hectares

---

### 3. Missing or Wrong Datum

**Error Pattern:**
- EPSG code without datum specification
- Assuming WGS84 when data uses different datum
- Missing datum transformation parameters

**Detection:**
- Check EPSG.io for datum information
- Verify if datum matches region (NAD83 in North America, GDA94 in Australia)
- Look for coordinate shifts when overlaying datasets

**Example:**
```
INCOMPLETE: "EPSG:4269"
(NAD83 geographic - should specify if original or HARN)

COMPLETE: "EPSG:4269 (NAD83 original datum)"
```

**Correction:**
- Specify datum explicitly
- Document datum transformation if converting
- Use EPSG code that includes datum (e.g., EPSG:4326 = WGS84)

---

## Calculation Errors

### 4. Area Calculated in Wrong Projection

**Error Pattern:**
- Calculating area using unprojected (lat/lon) coordinates
- Using Web Mercator (EPSG:3857) for area near poles
- Not accounting for projection distortion

**Detection:**
- If area claim is from lat/lon data → suspect
- Check if projection is appropriate for area calculation
- Compare claimed area with known reference (country size, etc.)

**Example:**
```
WRONG:
  Polygon in EPSG:4326 (WGS84 geographic)
  Area: 1000 km²
  (Likely incorrect - calculated in degrees)

RIGHT:
  Polygon reprojected to EPSG:32637 (UTM)
  Area: 1000 km²
  (Calculated in meters, converted to km²)
```

**Correction:**
1. Reproject geometry to equal-area projection (e.g., UTM, Albers Equal Area)
2. Calculate area in projected units (m²)
3. Convert to desired units (km², hectares)

**Detection Script Concept:**
```python
# If polygon.crs.is_geographic and area_claimed > 0:
#   FLAG: "Area calculated from geographic coordinates"
```

---

### 5. Planar vs Geodesic Distance

**Error Pattern:**
- Using planar distance for large distances (>100km)
- Not accounting for Earth's curvature
- Reporting great circle distance as straight line

**Detection:**
- Check distance magnitude
- Verify if geodesic calculation mentioned
- Compare with known distances (city-to-city)

**Example:**
```
WRONG: "Distance: 5000 km (calculated in EPSG:4326)"
(Planar calculation on lat/lon is inaccurate for large distances)

RIGHT: "Distance: 5000 km (geodesic, WGS84 ellipsoid)"
```

**Correction:**
- Use geodesic calculation (Vincenty or Haversine)
- Specify calculation method
- For large distances, geodesic > planar by several kilometers

---

## Data Recency Errors

### 6. Confusing Acquisition vs Processing Date

**Error Pattern:**
- Citing processing/publication date as acquisition date
- Claiming "recent" imagery that's years old
- Not specifying date type

**Detection:**
- Check provider catalog for actual acquisition date
- Query USGS EarthExplorer or Copernicus by scene ID
- Verify date against metadata files

**Example:**
```
WRONG: "Sentinel-2 imagery from January 2024"
(Check: Is this acquisition or processing date?)

RIGHT: "Sentinel-2 imagery acquired 2024-01-15, processed 2024-01-17"
```

**Correction:**
- Always cite acquisition date (sensor capture time)
- Specify if using composite (date range)
- Check metadata: Landsat (DATE_ACQUIRED), Sentinel (SENSING_TIME)

---

### 7. Outdated Dataset Version

**Error Pattern:**
- Using old dataset version when newer available
- Not citing dataset version
- Claiming current data when using archival

**Detection:**
- Check provider website for latest version
- Verify DOI or product version number
- Compare date range with claim

**Example:**
```
WRONG: "Global Forest Change data (2020)"
(Latest version covers 2000-2023)

RIGHT: "Global Forest Change v1.11 (2000-2023)"
```

**Correction:**
- Cite specific version: "MODIS MCD12Q1 v061"
- Check release date vs data coverage
- Update to latest version if available

---

## Resolution & Scale Errors

### 8. Upscaled Resolution Claimed as Native

**Error Pattern:**
- Claiming 10m resolution from 30m Landsat
- Resampling without disclosure
- Overstating data precision

**Detection:**
- Check source data specifications
- Verify sensor capabilities
- Look for resampling methodology

**Example:**
```
WRONG: "10m resolution land cover map from Landsat 8"
(Landsat 8 is 30m - cannot achieve true 10m)

RIGHT: "Land cover map resampled to 10m from Landsat 8 (native 30m)"
```

**Common Native Resolutions:**
- Landsat 8: 30m (15m panchromatic)
- Sentinel-2: 10m (bands 2,3,4,8), 20m (bands 5,6,7,8A,11,12), 60m (bands 1,9,10)
- MODIS: 250m (bands 1-2), 500m (bands 3-7), 1km (bands 8-36)
- SRTM: 30m (US), 90m (global)

---

### 9. Map Scale Incompatible with Resolution

**Error Pattern:**
- Displaying 30m data at 1:5,000 scale
- Scale too large for data detail
- Not adjusting for screen vs print

**Detection:**
- Calculate: scale_denominator = ground_distance / map_distance
- Verify if features visible at claimed scale
- Check if resolution supports scale

**Rule of Thumb:**
```
Minimum scale ≈ resolution × 2000
30m data → 1:60,000 minimum scale
10m data → 1:20,000 minimum scale
```

**Example:**
```
WRONG: "1:10,000 map from 30m Landsat"
(30m pixels would be 3mm on map - too coarse)

RIGHT: "1:100,000 map from 30m Landsat"
(30m pixels = 0.3mm - acceptable)
```

---

## Statistical & Index Errors

### 10. NDVI Values Outside Valid Range

**Error Pattern:**
- NDVI values > 1 or < -1
- Not handling clouds/water as nodata
- Incorrect band order in calculation

**Detection:**
- Check min/max values in results
- Verify band assignments: (NIR - Red) / (NIR + Red)
- Look for outliers

**Example:**
```
WRONG: "Average NDVI: 1.35"
(Impossible - NDVI range is -1 to 1)

RIGHT: "Average NDVI: 0.65 (vegetated areas only, clouds masked)"
```

**Correction:**
- Verify bands: Landsat 8 (NIR=B5, Red=B4), Sentinel-2 (NIR=B8, Red=B4)
- Mask clouds, water, snow
- Check for scale factors (Sentinel values often 0-10000, need /10000)

---

### 11. Incorrect Band Combinations

**Error Pattern:**
- Wrong band numbers for sensor
- Confusing Landsat 7/8/9 band numbering
- Using RGB bands for spectral indices

**Detection:**
- Verify sensor specifications
- Check band wavelengths
- Confirm index formula matches sensor

**Common Band Assignments:**

| Index | Formula | Landsat 8/9 | Sentinel-2 |
|-------|---------|-------------|------------|
| NDVI | (NIR-Red)/(NIR+Red) | (B5-B4)/(B5+B4) | (B8-B4)/(B8+B4) |
| NDWI | (Green-NIR)/(Green+NIR) | (B3-B5)/(B3+B5) | (B3-B8)/(B3+B8) |
| EVI | 2.5*(NIR-Red)/(NIR+6*Red-7.5*Blue+1) | Complex | Complex |

**Example:**
```
WRONG: "Landsat 8 NDVI = (B4-B3)/(B4+B3)"
(This is Landsat 7 numbering)

RIGHT: "Landsat 8 NDVI = (B5-B4)/(B5+B4)"
```

---

### 12. Zonal Statistics Without Methodology

**Error Pattern:**
- Reporting zonal mean/sum without specifying method
- Not handling partial pixels at boundaries
- Missing nodata handling

**Detection:**
- Check if aggregation method specified
- Verify boundary pixel handling
- Look for nodata masking

**Example:**
```
INCOMPLETE: "Mean NDVI for region: 0.45"

COMPLETE: "Mean NDVI for region: 0.45
(zonal mean, pixels with >50% coverage, clouds masked, n=1247 pixels)"
```

---

## Attribution Errors

### 13. Missing Open Data Attribution

**Error Pattern:**
- No credit for Copernicus/Sentinel data
- Missing "© OpenStreetMap contributors"
- Not citing Landsat/MODIS source

**Detection:**
- Check for attribution statement
- Verify against provider requirements
- Look for dataset mentions without credit

**Required Attributions:**

| Source | Required Text |
|--------|--------------|
| Copernicus Sentinel | "Contains modified Copernicus Sentinel data [year]" |
| Landsat | "Landsat data courtesy of the U.S. Geological Survey" |
| MODIS | "MODIS data provided by NASA EOSDIS Land Processes DAAC" |
| OpenStreetMap | "© OpenStreetMap contributors" |
| Natural Earth | "Made with Natural Earth" |

**Example:**
```
WRONG: "Satellite imagery used for analysis"
(Which satellite? Attribution missing)

RIGHT: "Contains modified Copernicus Sentinel-2 data (2023), processed by [organization]"
```

---

### 14. Wrong Dataset Version Citation

**Error Pattern:**
- Generic citation without version
- DOI missing or incorrect
- Not specifying processing level

**Detection:**
- Check if version number present
- Verify DOI resolves correctly
- Confirm processing level (L1C, L2A, etc.)

**Example:**
```
INCOMPLETE: "SRTM elevation data"

COMPLETE: "SRTM v3.0 1-arc-second (30m) elevation data
(NASA JPL, 2013, DOI: 10.5067/MEaSUREs/SRTM/SRTMGL1.003)"
```

---

## Coordinate Errors

### 15. Coordinates Outside Valid Range

**Error Pattern:**
- Latitude > 90 or < -90
- Longitude > 180 or < -180
- Swapped lat/lon

**Detection:**
- Range check: lat ∈ [-90, 90], lon ∈ [-180, 180]
- Reverse geocode to verify location
- Check if coordinates match described location

**Example:**
```
WRONG: "Location: 150.5°N, 45.2°E"
(Latitude cannot exceed 90°)

RIGHT: "Location: 45.2°N, 150.5°E"
```

---

### 16. Wrong Hemisphere Designation

**Error Pattern:**
- Negative longitude with "E" designation
- Positive latitude with "S" designation
- Inconsistent sign conventions

**Detection:**
- Check sign vs hemisphere letter
- Verify against known location
- Confirm decimal vs degrees-minutes-seconds

**Convention:**
```
North latitude: positive or "N"
South latitude: negative or "S"
East longitude: positive or "E"
West longitude: negative or "W"

Example:
  40.7°N, 74.0°W  =  40.7, -74.0 (decimal)
```

---

## Error Detection Checklist

Use this quick checklist when reviewing geospatial claims:

- [ ] **Coordinates**: Range valid? Location matches description?
- [ ] **EPSG code**: Verified on EPSG.io? Matches data type?
- [ ] **Projection**: Appropriate for calculation type (area/distance)?
- [ ] **Units**: Correct for projection? Conversions accurate?
- [ ] **Date**: Acquisition vs processing specified? Recent as claimed?
- [ ] **Resolution**: Native or resampled? Upscaling disclosed?
- [ ] **Scale**: Compatible with data resolution?
- [ ] **Index values**: Within valid range (-1 to 1 for NDVI)?
- [ ] **Bands**: Correct for sensor and index?
- [ ] **Attribution**: All sources credited? Licenses followed?
- [ ] **Version**: Dataset version cited? DOI included?
- [ ] **Methodology**: Calculation method documented? Assumptions stated?

---

*Updated: 2026-02-06*
*For systematic error detection, run checklist on every geospatial claim*
