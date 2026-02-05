# GIS Command Center

> Comprehensive geospatial intelligence workspace for serious GIS and remote sensing work.

**Location:** `D:/My-Applications/70-GIS-Command-Center`
**Created:** 2026-02-04
**Maintainer:** MasterMindMandan
**Orchestrator:** ATLAS (Advanced Terrain & Location Analysis System)

---

## Orchestrator: ATLAS

**ATLAS** is the GIS Command Center's orchestrator -- a seasoned geospatial strategist who thinks in layers. ATLAS routes all incoming geospatial tasks to the appropriate specialist agent, chains multi-skill workflows, and manages cross-hub data flows.

**Persona Profile:** `.claude/core/ATLAS.md`

**Key Capabilities:**
- Intelligent routing across 12 skills and 7 specialist agents
- Multi-skill workflow chaining (e.g., satellite processing -> classification -> web map)
- Cross-hub integration with Carbon Hub, Green Sciences, and Business DevCon
- CRS verification protocol -- ATLAS insists on correct projections before any analysis
- Work Files intake and data routing

---

## Specialist Agents (7 Total)

| Agent | Color | Skills | Domain |
|-------|-------|--------|--------|
| **Spatial Analyst** | Navy | ark-gis-operations, ark-qgis-mapping, ark-arcgis-pro | Vector/raster geoprocessing, desktop GIS, CRS management |
| **Remote Sensing Analyst** | Indigo | ark-remote-sensing, ark-earth-observation, ark-nasa-earthdata | Satellite imagery, spectral analysis, Earth observation platforms |
| **Cartographer** | Teal | ark-web-mapping, ark-geocoding | Map design, web visualization, geocoding |
| **Terrain Specialist** | Sienna | ark-lidar-pointcloud | LiDAR, DEM/DTM/DSM, terrain analysis, 3D surfaces |
| **Hydrologist** | Cerulean | ark-hydrology | Watershed, flood modeling, drainage, water resources |
| **Network Analyst** | Orange | ark-network-analysis | Transportation, routing, isochrones, accessibility |
| **GeoAI Specialist** | Purple | ark-geospatial-ai | ML/DL classification, object detection, segmentation |

**Agent files:** `.claude/agents/`

### Agent Routing Table

| Topic | Route To | Keywords |
|-------|----------|----------|
| Vector/raster operations, geoprocessing | Spatial Analyst | buffer, intersect, clip, dissolve, shapefile, CRS, QGIS, ArcGIS |
| Satellite imagery, spectral analysis | Remote Sensing Analyst | Sentinel, Landsat, NDVI, GEE, NASA, STAC, radar |
| Map design, web visualization | Cartographer | Folium, Leafmap, web map, choropleth, geocoding |
| LiDAR, DEM, terrain, elevation | Terrain Specialist | LiDAR, point cloud, DEM, slope, hillshade |
| Watershed, flood, water resources | Hydrologist | watershed, flood, drainage, stream, catchment |
| Transportation, routing, accessibility | Network Analyst | OSMnx, routing, isochrone, shortest path |
| ML/DL classification, object detection | GeoAI Specialist | machine learning, classification, torchgeo, SAM |

---

## Mission

This workspace provides complete coverage of geospatial operations:
- Desktop GIS (QGIS, ArcGIS Pro)
- Core GIS operations (89 functions)
- Remote sensing & satellite imagery
- Web mapping & visualization
- LiDAR & point cloud processing
- Earth observation platforms (GEE, STAC)
- Geospatial AI & deep learning
- Geocoding & location services

---

## Skills Inventory (12 Total)

### Core GIS (3 skills - from Component Repository)

| Skill | Functions | Use Case |
|-------|-----------|----------|
| `ark-gis-operations` | 89 | Shapely, GeoPandas, Rasterio, PySAL |
| `ark-qgis-mapping` | 15 | QGIS desktop control via MCP |
| `ark-arcgis-pro` | 8 | ArcGIS Pro enterprise GIS |

### Remote Sensing & Imagery (3 skills)

| Skill | Libraries | Use Case |
|-------|-----------|----------|
| `ark-remote-sensing` | Satpy, sentinelhub, pyroSAR | Satellite & radar processing |
| `ark-earth-observation` | ee, geemap, pystac-client | Cloud platforms (GEE, STAC) |
| `ark-nasa-earthdata` | earthaccess, POWER API | NASA data archives |

### Visualization (1 skill)

| Skill | Libraries | Use Case |
|-------|-----------|----------|
| `ark-web-mapping` | Folium, Leafmap, pydeck | Interactive web maps |

### 3D & Terrain (1 skill)

| Skill | Libraries | Use Case |
|-------|-----------|----------|
| `ark-lidar-pointcloud` | PDAL, whitebox, laspy | LiDAR, DEM, terrain analysis |

### Hydrology & Water (1 skill)

| Skill | Libraries | Use Case |
|-------|-----------|----------|
| `ark-hydrology` | HyRiver, Pysheds, whitebox | Watershed, flood, drainage |

### Network & Transportation (1 skill)

| Skill | Libraries | Use Case |
|-------|-----------|----------|
| `ark-network-analysis` | OSMnx, NetworkX, pandana | Routing, accessibility, streets |

### AI & Intelligence (1 skill)

| Skill | Libraries | Use Case |
|-------|-----------|----------|
| `ark-geospatial-ai` | GeoAI, torchgeo, SAM | ML/DL for satellite imagery |

### Location Services (1 skill)

| Skill | Libraries | Use Case |
|-------|-----------|----------|
| `ark-geocoding` | GeoPy, Nominatim | Address/coordinate conversion |

---

## MCP Server Configuration

Add these to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "gis": {
      "command": "uvx",
      "args": ["gis-mcp"]
    },
    "qgis": {
      "command": "uvx",
      "args": ["qgis-mcp"]
    },
    "nasa": {
      "command": "npx",
      "args": ["-y", "@programcomputer/nasa-mcp-server@latest"],
      "env": {
        "NASA_API_KEY": "your-api-key-from-api.nasa.gov"
      }
    }
  }
}
```

### Available MCP Servers

| Server | Functions | Install |
|--------|-----------|---------|
| [gis-mcp](https://github.com/mahdin75/gis-mcp) | 89 geospatial ops | `pip install gis-mcp` |
| [qgis_mcp](https://github.com/jjsantos01/qgis_mcp) | QGIS control | `pip install qgis-mcp` |
| [nasa-mcp](https://github.com/AnCode666/nasa-mcp) | NASA APIs, APOD, NEO | `npx @programcomputer/nasa-mcp-server` |
| TomTom | Location services | Via Anthropic |
| Mapbox | Geocoding, routing | Community |

---

## Directory Structure

```
70-GIS-Command-Center/
├── .claude/
│   ├── CLAUDE.md              # This file
│   ├── settings.json          # MCP servers and hooks
│   ├── core/
│   │   └── ATLAS.md           # Orchestrator persona and routing
│   ├── agents/                # 7 specialist agents
│   │   ├── spatial-analyst.md
│   │   ├── remote-sensing-analyst.md
│   │   ├── cartographer.md
│   │   ├── terrain-specialist.md
│   │   ├── hydrologist.md
│   │   ├── network-analyst.md
│   │   └── geoai-specialist.md
│   └── skills/                # 12 GIS skills
│       ├── ark-gis-operations/
│       ├── ark-qgis-mapping/
│       ├── ark-arcgis-pro/
│       ├── ark-remote-sensing/
│       ├── ark-earth-observation/
│       ├── ark-nasa-earthdata/
│       ├── ark-web-mapping/
│       ├── ark-lidar-pointcloud/
│       ├── ark-hydrology/
│       ├── ark-network-analysis/
│       ├── ark-geospatial-ai/
│       └── ark-geocoding/
│
├── Work Files - GIS/          # Staging area (Commander's inbox)
│   ├── _INBOX/                # Drop raw materials here
│   └── _PROCESSING/           # Currently being organized
│
├── data/
│   ├── vector/                # Shapefiles, GeoJSON, GPKG
│   ├── raster/                # GeoTIFF, COG, NetCDF
│   ├── lidar/                 # LAS, LAZ, E57
│   ├── satellite/             # Sentinel, Landsat, MODIS
│   └── nasa/                  # NASA harvested data (APOD, NEO, POWER)
├── projects/                  # Active GIS projects
├── outputs/
│   ├── maps/                  # Generated maps
│   ├── analysis/              # Analysis results
│   └── exports/               # Data exports
├── scripts/                   # Python/processing scripts
└── .planning/                 # GSD project management
```

---

## Python Environment Setup

### Core Installation

```bash
# Create conda environment
conda create -n gis python=3.11
conda activate gis

# Core GIS stack
conda install -c conda-forge gdal geopandas rasterio shapely fiona pyproj

# Remote sensing
pip install satpy sentinelhub pyrosar earthpy rioxarray

# Visualization
pip install folium leafmap pydeck lonboard

# Point cloud
conda install -c conda-forge pdal python-pdal
pip install laspy whitebox open3d

# Earth observation
pip install earthengine-api geemap pystac-client stackstac

# NASA Earthdata
pip install earthaccess harmony-py

# Hydrology
pip install pysheds pygeohydro pynhd py3dep richdem

# Network analysis
pip install osmnx pandana momepy pyrosm

# AI/ML
pip install torch torchvision geoai torchgeo segment-geospatial

# Geocoding
pip install geopy pgeocode
```

### Quick Verify

```python
import geopandas as gpd
import rasterio
import folium
print("GIS stack ready!")
```

---

## Skill Trigger Reference

| Task | Skill | Key Triggers |
|------|-------|--------------|
| Buffer, intersect, spatial join | `ark-gis-operations` | GIS, geospatial, spatial |
| QGIS project control | `ark-qgis-mapping` | QGIS, desktop GIS |
| ArcGIS workflows | `ark-arcgis-pro` | ArcGIS, ESRI, ArcPy |
| Satellite imagery | `ark-remote-sensing` | Sentinel, Landsat, NDVI |
| Google Earth Engine | `ark-earth-observation` | GEE, STAC, Planetary Computer |
| NASA data access | `ark-nasa-earthdata` | NASA, MODIS, earthaccess, POWER |
| Interactive maps | `ark-web-mapping` | Folium, Leafmap, web map |
| LiDAR processing | `ark-lidar-pointcloud` | LiDAR, point cloud, DEM |
| Watershed analysis | `ark-hydrology` | watershed, flood, HyRiver, drainage |
| Street routing | `ark-network-analysis` | OSMnx, routing, isochrone, network |
| ML classification | `ark-geospatial-ai` | GeoAI, torchgeo, deep learning |
| Address lookup | `ark-geocoding` | geocoding, address, location |

---

## Common Workflows

### 1. Vector Analysis
```
Load shapefile -> ark-gis-operations -> Buffer/Intersect -> Export
```

### 2. Satellite Processing
```
Download Sentinel -> ark-remote-sensing -> Cloud mask -> NDVI -> ark-web-mapping
```

### 3. Terrain Analysis
```
LiDAR LAZ -> ark-lidar-pointcloud -> DEM -> Slope/Aspect -> ark-gis-operations
```

### 4. Earth Engine Analysis
```
Authenticate -> ark-earth-observation -> Filter collection -> Process -> Export
```

### 5. Geospatial ML
```
Training data -> ark-geospatial-ai -> Train model -> Inference -> Validate
```

---

## Data Sources

### Free Satellite Imagery
| Source | Data | Access |
|--------|------|--------|
| [Copernicus Open Access Hub](https://scihub.copernicus.eu/) | Sentinel 1/2/3 | Free registration |
| [USGS EarthExplorer](https://earthexplorer.usgs.gov/) | Landsat, ASTER | Free registration |
| [Planetary Computer](https://planetarycomputer.microsoft.com/) | Multiple | Free API |
| [Google Earth Engine](https://earthengine.google.com/) | Massive archive | Academic/nonprofit |

### Free Vector Data
| Source | Data | Format |
|--------|------|--------|
| [Natural Earth](https://www.naturalearthdata.com/) | Global basemap | Shapefile |
| [OpenStreetMap](https://www.openstreetmap.org/) | Crowdsourced | Various |
| [GADM](https://gadm.org/) | Admin boundaries | Shapefile, GPKG |
| [Geofabrik](https://www.geofabrik.de/) | OSM extracts | PBF, Shapefile |

### Free LiDAR
| Source | Coverage | Access |
|--------|----------|--------|
| [OpenTopography](https://opentopography.org/) | Global select | Free registration |
| [USGS 3DEP](https://www.usgs.gov/3d-elevation-program) | USA | Free |
| [UK LiDAR](https://environment.data.gov.uk/DefraDataDownload/?Mode=survey) | UK | Free |

---

## Coordinate Systems Quick Reference

| EPSG | Name | Use Case |
|------|------|----------|
| 4326 | WGS84 | GPS, global lat/lon |
| 3857 | Web Mercator | Web maps |
| 32601-32660 | UTM North | Local measurements (N hemisphere) |
| 32701-32760 | UTM South | Local measurements (S hemisphere) |

---

## Work Files Protocol

When Commander drops materials in `Work Files - GIS/_INBOX/`:
1. **Identify** - What project or analysis does this data support?
2. **Inspect** - Check format, CRS, extent, attributes
3. **Create** - Make project folder if new (`projects/{PROJECT-ID}/`)
4. **Route** - Move to appropriate data directory or project folder
5. **Notify** - Report what was organized and suggest next steps

### Staging Workflow
```
Commander drops files -> _INBOX/ -> ATLAS identifies -> _PROCESSING/ -> Route to project/data
```

---

## Cross-Hub Integration

| Hub | Direction | Data Flow |
|-----|-----------|-----------|
| **Carbon & Meth Hub** (07) | Export | Spatial analysis, NDVI maps, land cover classification |
| **Carbon & Meth Hub** (07) | Import | Project boundaries, monitoring sites |
| **Green Sciences** (80) | Export | Remote sensing products, species distribution maps |
| **Green Sciences** (80) | Import | Ecological survey data, field observations |
| **Business DevCon** (54) | Export | Location intelligence, isochrones, site reports |
| **CineCrafter** (01) | Export | Animated maps, 3D terrain renders |

---

## Resources

### Documentation
- [GeoPandas Docs](https://geopandas.org/)
- [Rasterio Docs](https://rasterio.readthedocs.io/)
- [QGIS Documentation](https://docs.qgis.org/)
- [Google Earth Engine Guides](https://developers.google.com/earth-engine/guides)

### Tutorials
- [Python GIS Cookbook](https://pygis.io/)
- [Geospatial Python Tutorial](https://carpentries-incubator.github.io/geospatial-python/)
- [Earth Data Science](https://www.earthdatascience.org/)

### Communities
- [GIS Stack Exchange](https://gis.stackexchange.com/)
- [r/gis](https://www.reddit.com/r/gis/)
- [Spatial Thoughts](https://spatialthoughts.com/)

---

*GIS Command Center - Where geography meets intelligence.*
*Orchestrated by ATLAS - 12 skills, 7 agents, 4 MCP servers*
*Maintained by MasterMindMandan - 2026-02-06*
