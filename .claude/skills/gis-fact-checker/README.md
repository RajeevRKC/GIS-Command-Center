# GIS Fact-Checker Skill

Systematic verification of geospatial analysis claims for the GIS Command Center.

---

## Overview

The `gis-fact-checker` skill provides domain-specific fact-checking for GIS and geospatial analysis outputs. It verifies coordinates, projections, calculations, data recency, classifications, and attributions against authoritative sources.

---

## Installation

**Location:** `D:/My-Applications/70-GIS-Command-Center/.claude/skills/gis-fact-checker/`

**Status:** ✓ Installed (2026-02-06)

---

## Structure

```
gis-fact-checker/
├── SKILL.md                                    (119 lines)
├── references/
│   ├── verification-sources.md                (258 lines)
│   └── common-errors.md                       (480 lines)
├── checklists/
│   └── spatial-analysis-checklist.md          (377 lines)
└── README.md                                   (this file)
```

**Total:** 1,234 lines of domain-specific verification guidance

---

## Usage

### Command Invocation

```bash
/fact-check [target]
```

**Examples:**
```bash
/fact-check ./reports/land-cover-analysis.pdf
/fact-check https://example.com/gis-dashboard
/fact-check                          # Verifies most recent analysis
```

### Direct Skill Invocation

From Claude Code interface:
- Type `/gis-fact-checker` to invoke directly
- Or use `/fact-check` command which routes to this skill

---

## Verification Categories

1. **Coordinate Accuracy** - Lat/lon validity, location verification
2. **Projection Systems** - EPSG codes, CRS verification
3. **Area/Distance Calculations** - Re-computation, unit validation
4. **Data Recency** - Acquisition dates, version verification
5. **Classification Accuracy** - Training data, accuracy assessment
6. **Statistical Analysis** - Index values, zonal statistics
7. **Scale/Resolution** - Native vs resampled, scale compatibility
8. **Attribution** - Data credits, license compliance

---

## Verification Sources (Tiered)

### Tier 1: Authoritative
- USGS EarthExplorer
- Copernicus Open Access Hub
- EPSG.io
- NASA Earthdata
- GADM

### Tier 2: Community
- OpenStreetMap
- Natural Earth
- National mapping agencies

### Tier 3: Derived
- Derived products
- Third-party databases

---

## Key Features

### Comprehensive Coverage
- 8 claim categories
- 16+ common error patterns
- 10-section verification checklist
- Tiered source hierarchy

### Domain Expertise
- GIS-specific validation rules
- Sensor specifications (Landsat, Sentinel, MODIS)
- Projection appropriateness guidelines
- Statistical analysis verification

### Evidence-Based
- All findings require documented evidence
- Source URLs and query results
- Confidence ratings (VERIFIED, LIKELY, UNVERIFIABLE, CONTRADICTED)
- Reproducible verification steps

---

## Reference Documents

### verification-sources.md (258 lines)
- Authoritative source URLs and APIs
- Query templates for each provider
- Verification protocols by claim type
- Common data specifications table

### common-errors.md (480 lines)
- 16 common error patterns with examples
- Detection methods and corrections
- Wrong EPSG codes, calculation errors, attribution issues
- Quick error detection checklist

### spatial-analysis-checklist.md (377 lines)
- 10-section systematic verification checklist
- Evidence requirements per section
- Calculation documentation templates
- Quick reference tool table

---

## Integration

### With GIS Command Center Components

| Component | Integration |
|-----------|-------------|
| GISMaster orchestrator | Coordinates multi-analysis verification |
| Spatial analyst agent | Re-computes calculations |
| Data validator agent | Cross-references authoritative sources |
| Attribution checker | Verifies licensing compliance |

### Extends Core Skill

**Extends:** `@ark-fact-checker`
- Inherits base fact-checking protocol
- Specializes for geospatial domain
- Uses same report format structure

---

## Common Error Patterns Detected

1. **Wrong EPSG code** (geographic vs projected)
2. **Area in degrees** (unprojected calculation)
3. **Stale imagery** (acquisition vs processing date)
4. **Resolution mismatch** (upscaled claimed as native)
5. **Coordinates out of range** (lat > 90°)
6. **Missing datum** transformation
7. **NDVI out of range** (< -1 or > 1)
8. **Missing attribution** (Copernicus, OSM, Landsat)

---

## Report Format

Produces structured fact-checking report:

```markdown
# Fact-Check Report: [Target]

## Summary
- Total claims: X
- Verified: X ✓
- Likely: X ~
- Unverifiable: X ?
- Contradicted: X ✗

## Findings by Category
[Category 1]
  Claim: [statement]
  Finding: [VERIFIED|LIKELY|UNVERIFIABLE|CONTRADICTED]
  Evidence: [sources, URLs, calculations]
  Confidence: [HIGH|MEDIUM|LOW]

## Critical Issues
[High-impact errors]

## Recommendations
[Corrections and improvements]
```

---

## Example Verification Flow

1. **Input:** `./reports/forest-change-analysis.pdf`
2. **Extract:** "Forest area: 1,250 km² (calculated from Landsat 8)"
3. **Categorize:** Area calculation claim
4. **Verify:**
   - Check projection used (must be projected, not EPSG:4326)
   - Query USGS for Landsat 8 specifications
   - Re-compute area from geometry if available
   - Verify units and conversions
5. **Rate:** VERIFIED (if matches) or CONTRADICTED (if differs)
6. **Document:** Evidence, sources, confidence level

---

## Dependencies

### Required Tools
- Read, Grep, Glob (file operations)
- WebSearch, WebFetch (source verification)
- Task (complex multi-step verification)

### External Sources
- Internet access for source verification
- EPSG.io, EarthExplorer, Copernicus APIs
- Nominatim geocoding service

---

## Maintenance

### Update Frequency
- **Monthly:** Check for new satellite missions, updated datasets
- **Quarterly:** Verify source URLs still active
- **Annually:** Review error patterns, add new common issues

### Version History
- **v1.0** (2026-02-06): Initial creation
  - 8 claim categories
  - 16 common error patterns
  - 3-tier source hierarchy
  - 10-section verification checklist

---

## Related Skills

| Skill | Purpose | Relationship |
|-------|---------|--------------|
| `@ark-fact-checker` | Base fact-checking protocol | Parent skill (extended) |
| `spatial-analyst` | Geospatial analysis | Provides calculations to verify |
| `data-validator` | Data quality checks | Complementary validation |
| `attribution-checker` | License compliance | Specialized attribution focus |

---

## Performance

### Typical Verification Times

| Document Type | Claims | Time | Complexity |
|--------------|--------|------|------------|
| Single map | 5-10 | 2-5 min | Low |
| Technical report | 20-50 | 10-20 min | Medium |
| Research paper | 50-100+ | 30-60 min | High |
| Web GIS dashboard | 10-30 | 5-15 min | Medium |

---

## Limitations

1. **Requires internet access** for authoritative source verification
2. **Cannot verify proprietary data** without access credentials
3. **Manual re-computation** needed for complex calculations without source data
4. **Quality depends on claim clarity** - vague claims harder to verify
5. **Source availability** - some historical data may not be queryable

---

## Future Enhancements

- [ ] Automated geometry re-calculation from GeoJSON/Shapefile
- [ ] Batch verification for multiple documents
- [ ] Integration with QGIS/ArcGIS for visual verification
- [ ] Machine learning for error pattern detection
- [ ] Real-time verification during analysis (pre-commit hook)

---

## Contact & Support

**Owner:** GIS Command Center
**Orchestrator:** GISMaster
**Created:** 2026-02-06
**Version:** 1.0

For questions or improvements, consult GISMaster orchestrator or update skill documentation directly.

---

*Quality through verification. Accuracy through evidence. Trust through transparency.*
