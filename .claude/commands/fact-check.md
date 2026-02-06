# Command: fact-check

Verify geospatial and GIS claims in spatial analysis reports, web map configurations, and research outputs.

---

## Syntax

```
/fact-check [target]
```

**Parameters:**
- `target` (optional): Path to document, URL, or description of claims to verify
  - If omitted: Analyzes most recent GIS analysis output or spatial report

---

## Description

Systematically verifies geospatial claims including:
- Coordinate accuracy and validity
- Projection systems and EPSG codes
- Area, distance, and perimeter calculations
- Satellite imagery recency and data versions
- Classification accuracy and statistical analysis
- Spatial resolution and map scale claims
- Data attribution and licensing compliance

Routes to `gis-fact-checker` skill which uses tiered verification sources and produces structured fact-checking reports.

---

## Examples

### Basic Usage

```bash
/fact-check ./reports/land-cover-analysis.pdf
```
Verifies all geospatial claims in land cover analysis report.

```bash
/fact-check https://example.com/gis-dashboard
```
Verifies claims in web GIS dashboard or map configuration.

```bash
/fact-check
```
Verifies most recent spatial analysis output in current workspace.

### With Specific Focus

```bash
/fact-check ./outputs/area-calculations.md
```
Focuses on area/distance calculation verification.

```bash
/fact-check ./metadata/sentinel-processing.xml
```
Verifies satellite imagery metadata claims.

---

## Target Types

| Type | Example | Verification Focus |
|------|---------|-------------------|
| **Spatial reports** | `./reports/analysis.pdf` | Coordinates, areas, projections, dates |
| **Web maps** | `https://map.example.com` | EPSG codes, attribution, tile sources |
| **Metadata files** | `./data/scene.xml` | Acquisition dates, resolution, CRS |
| **Research papers** | `./docs/paper.docx` | Statistical analysis, methodology, sources |
| **Config files** | `./config/map-settings.json` | CRS definitions, zoom levels, bounds |

---

## Verification Process

1. **Claim Extraction**: Identifies all geospatial claims in target
2. **Categorization**: Groups by type (coordinates, projections, calculations, etc.)
3. **Source Selection**: Chooses appropriate verification sources (Tier 1 preferred)
4. **Evidence Collection**: Queries EPSG.io, EarthExplorer, Copernicus, etc.
5. **Confidence Rating**: Assigns VERIFIED, LIKELY, UNVERIFIABLE, or CONTRADICTED
6. **Report Generation**: Produces structured fact-checking report

---

## Verification Sources

**Tier 1 (Authoritative):**
- USGS EarthExplorer (satellite imagery metadata)
- Copernicus Open Access Hub (Sentinel data)
- EPSG.io (coordinate reference systems)
- NASA Earthdata (MODIS, Landsat, SRTM)
- GADM (administrative boundaries)

**Tier 2 (Community):**
- OpenStreetMap (place names, boundaries)
- Natural Earth (geographic reference data)
- National mapping agencies (country-specific)

**Tier 3 (Derived):**
- Derived products (indices, change detection)
- Third-party databases (with documentation)

---

## Output Format

Produces structured report with:

```markdown
# Fact-Check Report: [Target]

## Summary
- Total claims: [n]
- Verified: [n] ✓
- Likely correct: [n] ~
- Unverifiable: [n] ?
- Contradicted: [n] ✗

## Findings by Category

### Coordinate Accuracy
[Claim 1]: VERIFIED
  Evidence: [Nominatim result, GADM match]
  Confidence: HIGH

### Projection Systems
[Claim 2]: CONTRADICTED
  Evidence: [EPSG.io shows different projection type]
  Confidence: HIGH
  Issue: Wrong EPSG code for data type

[... additional categories ...]

## Critical Issues
[List of high-impact errors]

## Recommendations
[Suggested corrections and improvements]
```

---

## Flags & Options

(Future expansion - currently routes directly to skill)

---

## Related Commands

| Command | Purpose |
|---------|---------|
| `/gis:validate-projection` | Deep dive on projection validation |
| `/gis:verify-attribution` | Check data attribution compliance |
| `/gis:recalculate-area` | Re-compute area from geometry |

---

## Common Use Cases

### Before Publication
```bash
/fact-check ./draft/research-paper.docx
```
Verify all claims before submitting research paper.

### Quality Control
```bash
/fact-check ./outputs/annual-report/
```
Batch verify all spatial analyses in annual report.

### Data Acquisition
```bash
/fact-check ./vendor-data/specifications.pdf
```
Verify vendor claims about data quality and specifications.

### Web Map Review
```bash
/fact-check https://internal.example.com/gis-portal
```
Verify web map metadata and attribution compliance.

---

## Integration

Works with GIS Command Center components:
- **GISMaster orchestrator**: Coordinates verification across multiple analyses
- **Spatial analyst agent**: Re-computes calculations for verification
- **Data validator agent**: Cross-references with authoritative sources
- **Attribution checker**: Verifies licensing and credit compliance

---

## Notes

- **Authoritative sources preferred**: Tier 1 sources provide highest confidence
- **Evidence required**: All findings documented with source URLs and screenshots
- **Reproducible**: Verification steps logged for audit trail
- **Non-destructive**: Reports findings without modifying original documents

---

*Command routes to: `gis-fact-checker` skill*
*Created: 2026-02-06*
