---
name: ark-arcgis-pro
description: Use when working with ArcGIS Pro for enterprise GIS, spatial analysis, or ESRI ecosystem integration through AI-assisted MCP integration.
triggers:
  - ArcGIS
  - ArcGIS Pro
  - ESRI
  - enterprise GIS
  - ArcPy
role: specialist
scope: implementation
output-format: code
---

# ArcGIS Pro MCP Integration

AI-powered enterprise GIS through Model Context Protocol integration with ArcGIS Pro.

## Prerequisites

- ArcGIS Pro with valid license
- ArcGIS Pro SDK for .NET
- .NET 8 runtime
- Named Pipes enabled

## Architecture

```
Claude/Copilot -> MCP Server (.NET) -> Named Pipes -> ArcGIS Pro Add-In
```

## MCP Configuration

Add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "arcgis": {
      "command": "dotnet",
      "args": ["run", "--project", "path/to/ArcGIS-MCP-Server"]
    }
  }
}
```

## Capabilities

- **Map Queries** - Get active map information
- **Layer Management** - List and query layers
- **Feature Counting** - Count features by layer
- **Navigation** - Zoom to layers/features
- **Geoprocessing** - Run GP tools
- **ArcPy Integration** - Execute Python scripts

## Available Tools

| Tool | Description |
|------|-------------|
| `get_active_map` | Current map information |
| `list_layers` | All layers in map |
| `count_features` | Feature count per layer |
| `zoom_to_layer` | Navigate to layer extent |
| `run_geoprocessing` | Execute GP tool |
| `execute_arcpy` | Run ArcPy code |
| `query_features` | SQL-based feature query |
| `export_map` | Render to image |

## Example Prompts

```
"List all layers in the current map"
"How many features are in the parcels layer?"
"Zoom to the study area layer"
"Run the Buffer tool on selected features"
"Calculate field statistics for population"
```

## Reference Guide

| Topic | Reference | Load When |
|-------|-----------|-----------|
| Setup | `references/setup.md` | Installation |
| Tools | `references/tools.md` | Available operations |
| Geoprocessing | `references/gp.md` | Running GP tools |

## Constraints

### MUST DO
- Have ArcGIS Pro running with Add-In
- Use valid license
- Configure Named Pipes correctly

### MUST NOT DO
- Attempt without valid license
- Run heavy GP without checking resources
- Ignore coordinate system issues
