---
name: gis-fact-checker
description: Verifies geospatial analysis claims including coordinates, projections, calculations, data recency, and attributions against authoritative GIS sources
allowed-tools:
  - Read
  - Grep
  - Glob
  - WebSearch
  - WebFetch
  - Task
user-invocable: true
references:
  - verification-sources.md
  - common-errors.md
checklists:
  - spatial-analysis-checklist.md
extends: "@ark-fact-checker"
---

<objective>
Systematically verify geospatial and GIS claims in spatial analysis reports, web map configurations, and research outputs by validating coordinates, projections, calculations, data recency, classifications, and attributions against authoritative sources.
</objective>

<quick_start>
When invoked, identify all verifiable geospatial claims in the target document. Categorize by type (coordinates, projections, calculations, data sources, etc.). For each claim, select appropriate verification method and authoritative source. Execute verification using tiered source hierarchy. Document findings in structured report following @ark-fact-checker protocol.
</quick_start>

<claim_categories>
  <category name="coordinate_accuracy">
    <validation>Verify lat/lon values are within valid ranges (-90 to 90, -180 to 180). Cross-reference against known locations using GADM, GeoNames, or OSM.</validation>
    <common_issues>Swapped coordinates, wrong hemisphere, precision exceeds data source accuracy</common_issues>
  </category>

  <category name="projection_systems">
    <validation>Verify EPSG codes match projection descriptions via EPSG.io. Confirm datum specifications. Check transformation parameters.</validation>
    <common_issues>Wrong EPSG code for region, geographic vs projected confusion, missing datum</common_issues>
  </category>

  <category name="area_distance_calculations">
    <validation>Re-compute areas/distances from geometry using appropriate projection. Verify units match claim. Check calculation methodology.</validation>
    <common_issues>Calculated in wrong projection, unit conversion errors, planar calculation on spherical data</common_issues>
  </category>

  <category name="data_recency">
    <validation>Verify satellite imagery dates against provider catalogs (Copernicus, USGS EarthExplorer, Sentinel Hub). Confirm acquisition vs processing dates.</validation>
    <common_issues>Citing processing date as acquisition date, claiming recent when using archival data</common_issues>
  </category>

  <category name="classification_accuracy">
    <validation>Cross-reference land use/terrain classifications with training data sources. Verify against ground truth where available.</validation>
    <common_issues>Mismatched classification schemes, extrapolating beyond training region</common_issues>
  </category>

  <category name="statistical_analysis">
    <validation>Re-derive zonal statistics, index values (NDVI, NDWI), and correlation coefficients from source rasters. Verify calculation parameters.</validation>
    <common_issues>NDVI outside -1 to 1 range, incorrect band combinations, aggregation method not specified</common_issues>
  </category>

  <category name="scale_resolution">
    <validation>Verify spatial resolution claims against data specifications. Check map scale calculations. Confirm detail level matches resolution.</validation>
    <common_issues>Upscaled resolution claimed as native, map scale incompatible with data resolution</common_issues>
  </category>

  <category name="attribution">
    <validation>Verify data source credits against provider requirements. Check license compliance. Confirm dataset versions.</validation>
    <common_issues>Missing attribution for open data, wrong dataset version cited, license violations</common_issues>
  </category>
</claim_categories>

<verification_sources>
  <tier level="1" authority="authoritative">
    <source>USGS EarthExplorer - satellite imagery metadata, acquisition dates</source>
    <source>Copernicus Open Access Hub - Sentinel data specifications</source>
    <source>EPSG.io - coordinate reference system definitions</source>
    <source>NASA Earthdata - MODIS, Landsat, SRTM specifications</source>
    <source>GADM - administrative boundary verification</source>
  </tier>

  <tier level="2" authority="community">
    <source>OpenStreetMap - place names, boundary verification</source>
    <source>Natural Earth - geographic reference data</source>
    <source>National mapping agencies - country-specific validation</source>
  </tier>

  <tier level="3" authority="derived">
    <source>Derived products - processed indices, change detection</source>
    <source>Third-party databases - commercial providers with documentation</source>
  </tier>
</verification_sources>

<process>
  <step n="1">Extract all geospatial claims from target document. Categorize by type.</step>
  <step n="2">For each claim, identify appropriate verification method and source tier.</step>
  <step n="3">Execute verification: query authoritative sources, re-compute calculations, cross-reference coordinates.</step>
  <step n="4">Document evidence: URLs, query results, calculation steps, screenshots where relevant.</step>
  <step n="5">Rate confidence: VERIFIED (Tier 1 source), LIKELY (Tier 2), UNVERIFIABLE (insufficient info), CONTRADICTED (evidence conflicts).</step>
  <step n="6">Compile findings using @ark-fact-checker report format with geospatial-specific sections.</step>
</process>

<common_errors>
  <error>Wrong EPSG code (e.g., EPSG:4326 for projected data, EPSG:3857 for geographic)</error>
  <error>Area calculated in degrees instead of meters (using unprojected WGS84)</error>
  <error>Stale imagery cited as recent (check acquisition vs publication date)</error>
  <error>Resolution claim mismatch (claiming 10m when using 30m Landsat)</error>
  <error>Coordinates outside valid range (lat > 90 or &lt; -90)</error>
  <error>Missing datum transformation when comparing datasets</error>
  <error>NDVI values outside -1 to 1 theoretical range</error>
  <error>Attribution missing for Copernicus, Landsat, or OSM data</error>
</common_errors>

<success_criteria>
  <criterion>All coordinate claims validated against known locations</criterion>
  <criterion>EPSG codes confirmed via EPSG.io with matching descriptions</criterion>
  <criterion>Area/distance calculations reproduced with documented methodology</criterion>
  <criterion>Data recency verified against provider catalogs with acquisition dates</criterion>
  <criterion>Statistical values re-derived or confirmed against specifications</criterion>
  <criterion>Attribution requirements met for all data sources</criterion>
  <criterion>Report documents confidence level with evidence for each claim</criterion>
</success_criteria>
