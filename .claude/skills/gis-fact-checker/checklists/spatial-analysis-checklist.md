# Spatial Analysis Verification Checklist

Systematic verification checklist for geospatial analysis reports and claims.

---

## Pre-Verification Setup

- [ ] **Identify document type**: Research paper, technical report, web map, metadata file
- [ ] **Extract all geospatial claims**: Coordinates, areas, distances, dates, sources
- [ ] **Categorize claims**: Coordinate, projection, calculation, data, statistical, attribution
- [ ] **Prioritize by risk**: High-impact claims first (areas, classifications, dates)
- [ ] **Prepare verification log**: Document structure for tracking findings

---

## Section 1: Coordinate Validation

### Basic Range Checks
- [ ] All latitudes ∈ [-90, 90]
- [ ] All longitudes ∈ [-180, 180]
- [ ] No impossible precision (e.g., 12 decimal places from 30m data)

### Location Verification
- [ ] Reverse geocode coordinates via Nominatim or GADM
- [ ] Verify location matches description (country, region, city)
- [ ] Check if coordinates match claimed feature (building, park, etc.)
- [ ] Cross-reference with OSM or Natural Earth

### Coordinate Format Consistency
- [ ] Decimal degrees vs degrees-minutes-seconds correctly converted
- [ ] Hemisphere letters (N/S/E/W) match signs
- [ ] Coordinate order consistent (lat,lon or lon,lat documented)

**Evidence Required:**
- Screenshot of location on map
- Nominatim reverse geocode result
- Known reference point comparison

---

## Section 2: Projection & CRS Validation

### EPSG Code Verification
- [ ] Query EPSG.io for each EPSG code
- [ ] Confirm projection type matches data type (geographic vs projected)
- [ ] Verify area of use includes claim location
- [ ] Check datum specification (WGS84, NAD83, GDA94, etc.)

### Projection Appropriateness
- [ ] **For area calculations**: Equal-area projection used (UTM, Albers, Lambert)
- [ ] **For distance calculations**: Conformal projection or geodesic method
- [ ] **For web maps**: Web Mercator (EPSG:3857) only for display, not calculation
- [ ] **For global data**: Appropriate global projection (Equal Earth, Robinson)

### Transformation Validity
- [ ] If data combined from multiple CRS, transformation documented
- [ ] Datum transformation parameters specified if needed
- [ ] No mixing of geographic and projected coordinates

**Evidence Required:**
- EPSG.io screenshot showing projection details
- WKT or Proj4 definition
- Area of use map confirming coverage

---

## Section 3: Area & Distance Calculations

### Area Verification
- [ ] Identify claimed area value and units
- [ ] Determine projection used (must be projected, not geographic)
- [ ] Re-calculate area using appropriate equal-area projection
- [ ] Verify unit conversions (m² → km², hectares)
- [ ] Compare with known reference (country size, lake area)
- [ ] Check for partial pixel handling at boundaries

### Distance Verification
- [ ] Identify claimed distance value and units
- [ ] Determine if planar or geodesic calculation
- [ ] For >100km distances: geodesic method required
- [ ] Re-calculate using Vincenty or Haversine formula
- [ ] Verify against known distances (city-to-city)

### Perimeter Verification
- [ ] Check if perimeter calculation method specified
- [ ] Verify appropriate projection used
- [ ] Confirm edge pixel handling

**Calculation Documentation Template:**
```
Claim: Area = [value] [units]
Original CRS: [EPSG code or description]
Verification CRS: [EPSG code for recalculation]
Recalculated Area: [value] [units]
Difference: [percentage or absolute difference]
Finding: [VERIFIED | CONTRADICTED]
```

---

## Section 4: Data Recency & Version

### Acquisition Date Verification
- [ ] Extract claimed date or date range
- [ ] Identify data source (Landsat, Sentinel, MODIS, etc.)
- [ ] Query provider catalog (EarthExplorer, Copernicus, NASA Earthdata)
- [ ] Verify acquisition vs processing vs publication date
- [ ] Check for composite date ranges (e.g., "8-day composite")
- [ ] Confirm temporal resolution matches claim

### Dataset Version Verification
- [ ] Identify dataset name and claimed version
- [ ] Check provider website for latest version
- [ ] Verify DOI or persistent identifier
- [ ] Confirm processing level (L1C, L2A, etc.)
- [ ] Check for updates or corrections since publication

### Scene/Tile Metadata
- [ ] Extract scene ID or tile ID if provided
- [ ] Query metadata by ID
- [ ] Verify cloud cover percentage
- [ ] Check for data quality flags
- [ ] Confirm spatial coverage (full vs partial)

**Evidence Required:**
- Catalog query results (screenshot or export)
- Metadata file excerpt
- Scene ID with acquisition timestamp

---

## Section 5: Resolution & Scale

### Resolution Verification
- [ ] Identify claimed spatial resolution
- [ ] Check source sensor specifications
- [ ] Verify native resolution vs resampled
- [ ] Confirm band-specific resolutions (e.g., Sentinel-2: 10m/20m/60m)
- [ ] Check if upscaling disclosed
- [ ] Verify pixel size in appropriate CRS (meters, not degrees)

### Scale Validation
- [ ] Calculate minimum scale: resolution × 2000
- [ ] Verify claimed scale appropriate for data resolution
- [ ] Check if scale bar matches coordinate system
- [ ] Confirm screen vs print scale specified

### Detail Level Consistency
- [ ] Features visible at resolution should be detectable
- [ ] Classification detail matches resolution capability
- [ ] No sub-pixel features claimed without super-resolution disclosure

**Resolution Reference:**
| Sensor | Native Resolution | Bands |
|--------|------------------|-------|
| Landsat 8/9 | 30m (15m pan) | Multispectral/Pan |
| Sentinel-2 | 10m/20m/60m | Band-specific |
| MODIS | 250m/500m/1km | Band-specific |
| SRTM | 30m (US), 90m (global) | Elevation |
| Planet | 3-5m | Multispectral |

---

## Section 6: Statistical Analysis

### Index Value Verification
- [ ] **NDVI**: Values ∈ [-1, 1]
- [ ] **NDWI**: Values ∈ [-1, 1]
- [ ] **EVI**: Values typically ∈ [-1, 1], check scaling
- [ ] Verify band combinations correct for sensor
- [ ] Check for scale factors (Sentinel often 0-10000 scale)

### Band Assignment Verification
- [ ] Confirm band numbers match sensor
- [ ] Verify wavelengths if custom index
- [ ] Check for Landsat 7 vs 8 vs 9 differences
- [ ] Confirm Sentinel-2 band naming (B8 vs B8A)

### Zonal Statistics Verification
- [ ] Aggregation method specified (mean, sum, median, etc.)
- [ ] Boundary pixel handling documented (>50% inclusion threshold)
- [ ] Nodata/cloud masking applied
- [ ] Sample size (n) reported
- [ ] Standard deviation or error bars included

### Time Series Verification
- [ ] Temporal resolution consistent
- [ ] Gap-filling methodology documented
- [ ] Seasonality accounted for
- [ ] Trend calculation method specified

**Evidence Required:**
- Recalculated index values
- Band combination verification
- Statistical methodology documentation

---

## Section 7: Classification & Accuracy

### Classification Scheme Verification
- [ ] Identify classification system (LULC, vegetation type, etc.)
- [ ] Verify scheme matches established standard (CORINE, Anderson, etc.)
- [ ] Check class definitions documented
- [ ] Confirm number of classes matches description

### Accuracy Assessment
- [ ] Overall accuracy reported
- [ ] Confusion matrix provided
- [ ] Kappa statistic included
- [ ] User's/Producer's accuracy by class
- [ ] Validation dataset independent from training
- [ ] Sample size adequate (>50 per class minimum)

### Training Data Verification
- [ ] Training data source documented
- [ ] Sample distribution by class reported
- [ ] Geographic distribution appropriate
- [ ] Temporal alignment with imagery

**Minimum Standards:**
- Overall accuracy >80% for most applications
- Kappa >0.7 for strong agreement
- User's accuracy >70% per class

---

## Section 8: Attribution & Licensing

### Data Source Attribution
- [ ] **Copernicus/Sentinel**: "Contains modified Copernicus Sentinel data [year]"
- [ ] **Landsat**: "Landsat data courtesy of the U.S. Geological Survey"
- [ ] **MODIS**: "MODIS data provided by NASA EOSDIS"
- [ ] **OpenStreetMap**: "© OpenStreetMap contributors"
- [ ] **Natural Earth**: "Made with Natural Earth"
- [ ] **SRTM**: "SRTM data courtesy of NASA JPL"

### Citation Completeness
- [ ] Dataset name and version
- [ ] Provider/organization
- [ ] DOI or persistent identifier
- [ ] Access date or acquisition date
- [ ] Processing level specified
- [ ] License type stated

### License Compliance
- [ ] Open data properly credited
- [ ] Commercial data usage authorized
- [ ] Derivative work permissions obtained
- [ ] Share-alike requirements met if applicable

**Example Complete Citation:**
```
European Space Agency (ESA). (2023). Copernicus Sentinel-2
Level-2A Bottom-of-Atmosphere Reflectance. ESA Copernicus
Open Access Hub. Retrieved 2024-01-15.
https://scihub.copernicus.eu/
```

---

## Section 9: Methodology Documentation

### Processing Steps
- [ ] Preprocessing steps documented (atmospheric correction, orthorectification)
- [ ] Software and versions specified
- [ ] Algorithm names and parameters
- [ ] Quality control measures described

### Reproducibility
- [ ] Code/scripts available or described
- [ ] Random seeds set for reproducibility
- [ ] Input data versions specified
- [ ] Output data formats documented

### Assumptions & Limitations
- [ ] Key assumptions stated
- [ ] Known limitations acknowledged
- [ ] Uncertainty quantified where possible
- [ ] Scope of applicability defined

---

## Section 10: Cross-Validation

### Internal Consistency
- [ ] Maps match text descriptions
- [ ] Legends complete and accurate
- [ ] Table values sum correctly
- [ ] Units consistent throughout

### External Validation
- [ ] Compare with independent datasets
- [ ] Check against known ground truth
- [ ] Visual inspection with high-resolution imagery
- [ ] Comparison with published studies

### Temporal Consistency
- [ ] If time series: trends make sense
- [ ] Seasonal patterns expected
- [ ] No impossible changes (forest→ocean)
- [ ] Change detection methodology sound

---

## Final Verification Report

### Summary Statistics
- [ ] Total claims identified: [n]
- [ ] Claims verified: [n] ✓
- [ ] Claims likely correct: [n] ~
- [ ] Claims unverifiable: [n] ?
- [ ] Claims contradicted: [n] ✗

### Confidence Ratings
- [ ] **HIGH**: Tier 1 source, exact match
- [ ] **MEDIUM**: Tier 2 source, close match
- [ ] **LOW**: Tier 3 source, approximate

### Critical Findings
- [ ] List any claims that failed verification
- [ ] Document high-impact errors (wrong areas, outdated data)
- [ ] Flag missing attributions
- [ ] Highlight methodology gaps

### Recommendations
- [ ] Corrections needed
- [ ] Additional verification suggested
- [ ] Documentation improvements
- [ ] Data updates recommended

---

## Evidence Archive

For each verified claim, archive:
- [ ] Original claim text
- [ ] Verification method
- [ ] Source URLs
- [ ] Query results
- [ ] Screenshots
- [ ] Calculation logs
- [ ] Confidence rating
- [ ] Notes

---

## Quick Reference: Verification Tools

| Task | Tool | URL |
|------|------|-----|
| EPSG verification | EPSG.io | https://epsg.io/ |
| Reverse geocode | Nominatim | https://nominatim.openstreetmap.org/ |
| Landsat metadata | EarthExplorer | https://earthexplorer.usgs.gov/ |
| Sentinel metadata | Copernicus Hub | https://scihub.copernicus.eu/ |
| Boundary check | GADM | https://gadm.org/ |
| OSM query | Overpass Turbo | https://overpass-turbo.eu/ |
| MODIS specs | LP DAAC | https://lpdaac.usgs.gov/ |

---

## Checklist Usage Notes

1. **Not all sections apply to every document** - Skip irrelevant sections
2. **Prioritize by impact** - Verify area calculations before minor metadata
3. **Document everything** - Evidence is key for fact-checking reports
4. **Use tier system** - Tier 1 sources provide highest confidence
5. **Be systematic** - Complete each section before moving to next
6. **Flag don't fix** - Report findings, don't silently correct
7. **Quantify confidence** - Always rate: VERIFIED, LIKELY, UNVERIFIABLE, CONTRADICTED

---

*Version: 1.0*
*Updated: 2026-02-06*
*Use this checklist as a systematic guide for verifying geospatial analysis claims*
