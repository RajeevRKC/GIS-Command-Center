---
name: ark-qgis-mapping
description: Use when working with QGIS for desktop GIS mapping, layer management, processing algorithms, or cartographic production through AI-assisted MCP integration.
triggers:
  - QGIS
  - desktop GIS
  - mapping
  - cartography
  - QGIS MCP
role: specialist
scope: implementation
output-format: code
---

# QGIS MCP Integration

AI-powered desktop GIS through Model Context Protocol integration with QGIS.

## Prerequisites

- QGIS 3.22+
- Python 3.10+
- uv package manager
- Claude Desktop

## MCP Configuration

Add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "qgis": {
      "command": "uvx",
      "args": ["qgis-mcp"]
    }
  }
}
```

## Capabilities

- **Project Management** - Create, load, save projects
- **Layer Operations** - Add vector/raster layers
- **Processing Toolbox** - Run QGIS algorithms
- **Map Rendering** - Generate map images
- **Feature Queries** - Access layer features
- **Code Execution** - Run PyQGIS scripts

## Available Tools

| Tool | Description |
|------|-------------|
| `ping` | Check connection |
| `get_qgis_info` | QGIS version and status |
| `load_project` | Open existing project |
| `create_new_project` | Start new project |
| `get_project_info` | Project metadata |
| `add_vector_layer` | Load shapefile, GeoJSON |
| `add_raster_layer` | Load GeoTIFF, etc. |
| `get_layers` | List all layers |
| `remove_layer` | Delete layer |
| `zoom_to_layer` | Navigate to extent |
| `get_layer_features` | Query features |
| `execute_processing` | Run toolbox algorithm |
| `save_project` | Save changes |
| `render_map` | Export map image |
| `execute_code` | Run PyQGIS |

## Example Prompts

```
"Load the shapefile and display it on the map"
"Buffer all features by 100 meters"
"Export the map view as PNG"
"Calculate statistics for the population field"
"Clip the raster to the study area boundary"
```

## Reference Guide

| Topic | Reference | Load When |
|-------|-----------|-----------|
| Setup | `references/setup.md` | Installation |
| Layers | `references/layers.md` | Data management |
| Processing | `references/processing.md` | Toolbox algorithms |

## Constraints

### MUST DO
- Keep QGIS running during session
- Use valid file paths
- Check CRS compatibility

### MUST NOT DO
- Attempt without QGIS running
- Load incompatible data formats
- Ignore layer coordinate systems
