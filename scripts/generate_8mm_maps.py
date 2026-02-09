"""
8MM Mangrove Restoration Project - Map Generator
Generates all cartographic products for the Pre-Restoration Report
"""

import geopandas as gpd
import folium
from folium import plugins
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.colors import LinearSegmentedColormap
import numpy as np
from pathlib import Path
import json

# ── Paths ──
BASE = Path(r"D:\My-Applications\70-GIS-Command-Center")
ESRI = BASE / "Work Files - GIS" / "_INBOX" / "ESRI_Data"
OUTPUT = BASE / "outputs" / "maps" / "8mm_report"
OUTPUT.mkdir(parents=True, exist_ok=True)

# ── Load all shapefiles ──
print("[1/6] Loading shapefiles...")
final_pts = gpd.read_file(ESRI / "8MM_Final_Locations_Points.shp")
final_poly = gpd.read_file(ESRI / "8MM_Final_Locations_Polygons.shp")
ali_pts = gpd.read_file(ESRI / "Abu_Ali_8MM_Sites_Points.shp")
ali_poly = gpd.read_file(ESRI / "Abu_Ali_8MM_Sites_Polygons.shp")
all_zones = gpd.read_file(ESRI / "All_Planting_Zones.shp")
all_pts = gpd.read_file(ESRI / "All_Survey_Points.shp")
control = gpd.read_file(ESRI / "Control_Sites.shp")
nursery = gpd.read_file(ESRI / "Nursery_Boundary.shp")

# ── Color scheme ──
ZONE_COLORS = ['#2E7D32', '#1B5E20', '#388E3C', '#43A047',
               '#4CAF50', '#66BB6A', '#81C784', '#A5D6A7',
               '#C8E6C9', '#00695C', '#00897B', '#26A69A']
CONTROL_COLORS = {'Control_Unplanted_1': '#E53935',
                  'Control_Natural_Ref': '#1E88E5',
                  'Control_Substrate_1': '#FB8C00'}
NURSERY_COLOR = '#8E24AA'

# ── Helper: add satellite tiles to folium ──
def add_satellite_tiles(m):
    folium.TileLayer(
        tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        attr='Esri World Imagery',
        name='Satellite',
        overlay=False
    ).add_to(m)
    folium.TileLayer(
        tiles='https://server.arcgisonline.com/ArcGIS/rest/services/Reference/World_Boundaries_and_Places/MapServer/tile/{z}/{y}/{x}',
        attr='Esri Labels',
        name='Labels',
        overlay=True
    ).add_to(m)


# ═══════════════════════════════════════════════════════════
# MAP 1: REGIONAL OVERVIEW - Abu Ali Island Context
# ═══════════════════════════════════════════════════════════
print("[2/6] Creating Map 1: Regional Overview...")

# Center on Abu Ali area
center_lat = 27.25
center_lon = 49.52

m1 = folium.Map(location=[center_lat, center_lon], zoom_start=10,
                tiles=None, width=1200, height=800)
add_satellite_tiles(m1)

# Add all planting zones
for idx, row in all_zones.iterrows():
    color = ZONE_COLORS[idx % len(ZONE_COLORS)]
    folium.GeoJson(
        gpd.GeoSeries([row.geometry]).__geo_interface__,
        style_function=lambda x, c=color: {
            'fillColor': c, 'color': c, 'weight': 2,
            'fillOpacity': 0.5
        },
        tooltip=f"{row['NAME']} ({row['AREA_HA']:.1f} ha)"
    ).add_to(m1)

# Add nursery
for idx, row in nursery.iterrows():
    folium.GeoJson(
        gpd.GeoSeries([row.geometry]).__geo_interface__,
        style_function=lambda x: {
            'fillColor': NURSERY_COLOR, 'color': NURSERY_COLOR,
            'weight': 3, 'fillOpacity': 0.6
        },
        tooltip=f"Nursery: {row['NAME']} ({row['AREA_HA']:.2f} ha)"
    ).add_to(m1)

# Add control sites
for idx, row in control.iterrows():
    color = CONTROL_COLORS.get(row['NAME'], '#FF0000')
    folium.CircleMarker(
        location=[row['LATITUDE'], row['LONGITUDE']],
        radius=10, color=color, fill=True, fill_color=color,
        fill_opacity=0.8, weight=3,
        tooltip=f"Control: {row['NAME']}"
    ).add_to(m1)

# Add key labels
folium.Marker(
    location=[27.31, 49.49],
    icon=folium.DivIcon(html='<div style="font-size:14px;font-weight:bold;color:white;text-shadow:2px 2px 4px black;">Abu Ali Island</div>')
).add_to(m1)

folium.Marker(
    location=[27.20, 49.52],
    icon=folium.DivIcon(html='<div style="font-size:14px;font-weight:bold;color:white;text-shadow:2px 2px 4px black;">Al Batinah Island</div>')
).add_to(m1)

# Add scale and layer control
plugins.MeasureControl(position='topleft').add_to(m1)
folium.LayerControl().add_to(m1)

m1.save(str(OUTPUT / "01_regional_overview.html"))
print(f"  Saved: {OUTPUT / '01_regional_overview.html'}")


# ═══════════════════════════════════════════════════════════
# MAP 2: ALL SITES OVERVIEW - Phase 2 Planting Areas
# ═══════════════════════════════════════════════════════════
print("[3/6] Creating Map 2: All Sites Overview...")

# Compute center of Phase 2 sites (final locations)
bounds = final_poly.total_bounds
center2 = [(bounds[1] + bounds[3]) / 2, (bounds[0] + bounds[2]) / 2]

m2 = folium.Map(location=center2, zoom_start=12,
                tiles=None, width=1200, height=800)
add_satellite_tiles(m2)

# Phase 2 planting zones with labels
site_names = ['Site 1 (510 ha)', 'Site 2 (123.95 ha)',
              'Site 3 (53.08 ha)', 'Site 4 (122.35 ha)']
site_colors = ['#1B5E20', '#2E7D32', '#388E3C', '#43A047']

for idx, row in final_poly.iterrows():
    color = site_colors[idx % 4]
    folium.GeoJson(
        gpd.GeoSeries([row.geometry]).__geo_interface__,
        style_function=lambda x, c=color: {
            'fillColor': c, 'color': '#FFFFFF', 'weight': 3,
            'fillOpacity': 0.45, 'dashArray': '5'
        },
        tooltip=f"{site_names[idx]} - {row['AREA_HA']:.1f} ha"
    ).add_to(m2)

    # Add centroid label
    centroid = row.geometry.centroid
    folium.Marker(
        location=[centroid.y, centroid.x],
        icon=folium.DivIcon(html=f'<div style="font-size:12px;font-weight:bold;color:white;text-shadow:2px 2px 4px black;white-space:nowrap;">{site_names[idx]}</div>')
    ).add_to(m2)

# Survey points
for idx, row in final_pts.iterrows():
    folium.CircleMarker(
        location=[row['LATITUDE'], row['LONGITUDE']],
        radius=4, color='#FFD600', fill=True,
        fill_color='#FFD600', fill_opacity=0.9, weight=1,
        tooltip=f"{row['NAME']} | Elev: {row['ELEVATION']}m"
    ).add_to(m2)

# Control sites
for idx, row in control.iterrows():
    color = CONTROL_COLORS.get(row['NAME'], '#FF0000')
    folium.CircleMarker(
        location=[row['LATITUDE'], row['LONGITUDE']],
        radius=12, color=color, fill=True, fill_color=color,
        fill_opacity=0.8, weight=3,
        tooltip=f"CONTROL: {row['NAME']}"
    ).add_to(m2)
    folium.Marker(
        location=[row['LATITUDE'], row['LONGITUDE']],
        icon=folium.DivIcon(html=f'<div style="font-size:10px;font-weight:bold;color:{color};text-shadow:1px 1px 2px black;white-space:nowrap;">{row["NAME"]}</div>')
    ).add_to(m2)

plugins.MeasureControl(position='topleft').add_to(m2)
folium.LayerControl().add_to(m2)
m2.save(str(OUTPUT / "02_all_sites_overview.html"))
print(f"  Saved: {OUTPUT / '02_all_sites_overview.html'}")


# ═══════════════════════════════════════════════════════════
# MAP 3: INDIVIDUAL SITE MAPS (4 maps)
# ═══════════════════════════════════════════════════════════
print("[4/6] Creating Maps 3a-3d: Individual Site Maps...")

for idx, row in final_poly.iterrows():
    site_num = idx + 1
    bounds = row.geometry.bounds  # minx, miny, maxx, maxy
    center = [(bounds[1] + bounds[3]) / 2, (bounds[0] + bounds[2]) / 2]

    m = folium.Map(location=center, zoom_start=13,
                   tiles=None, width=1200, height=800)
    add_satellite_tiles(m)

    # Main polygon
    folium.GeoJson(
        gpd.GeoSeries([row.geometry]).__geo_interface__,
        style_function=lambda x: {
            'fillColor': '#2E7D32', 'color': '#FFFFFF', 'weight': 3,
            'fillOpacity': 0.35, 'dashArray': '5'
        },
        tooltip=f"Site {site_num}: {row['AREA_HA']:.1f} ha"
    ).add_to(m)

    # Survey points for this site
    site_pts = final_pts[
        final_pts.geometry.within(row.geometry.buffer(0.005))
    ]
    for _, pt in site_pts.iterrows():
        folium.CircleMarker(
            location=[pt['LATITUDE'], pt['LONGITUDE']],
            radius=5, color='#FFD600', fill=True,
            fill_color='#FFD600', fill_opacity=0.9, weight=1,
            tooltip=f"{pt['NAME']} | Elev: {pt['ELEVATION']}m"
        ).add_to(m)

    # Title
    folium.Marker(
        location=[bounds[3] + 0.002, (bounds[0] + bounds[2]) / 2],
        icon=folium.DivIcon(html=f'<div style="font-size:16px;font-weight:bold;color:white;text-shadow:2px 2px 4px black;">Site {site_num} - {row["AREA_HA"]:.1f} ha</div>')
    ).add_to(m)

    plugins.MeasureControl(position='topleft').add_to(m)
    m.save(str(OUTPUT / f"03{chr(96+site_num)}_site_{site_num}_detail.html"))
    print(f"  Saved: Site {site_num} detail map")


# ═══════════════════════════════════════════════════════════
# MAP 4: NURSERY SITE MAP
# ═══════════════════════════════════════════════════════════
print("[5/6] Creating Map 4: Nursery Site...")

n_row = nursery.iloc[0]
n_bounds = n_row.geometry.bounds
n_center = [(n_bounds[1] + n_bounds[3]) / 2, (n_bounds[0] + n_bounds[2]) / 2]

m4 = folium.Map(location=n_center, zoom_start=16,
                tiles=None, width=1200, height=800)
add_satellite_tiles(m4)

folium.GeoJson(
    gpd.GeoSeries([n_row.geometry]).__geo_interface__,
    style_function=lambda x: {
        'fillColor': NURSERY_COLOR, 'color': '#FFFFFF', 'weight': 3,
        'fillOpacity': 0.4
    },
    tooltip=f"Nursery: {n_row['AREA_HA']:.2f} ha | Capacity: {n_row['CAPACITY']}"
).add_to(m4)

# Add nursery boundary points
nursery_coords = [
    (27.3052655, 49.4877966, 'P1'), (27.3056097, 49.4871276, 'P2'),
    (27.3063753, 49.4877413, 'P3'), (27.3069802, 49.4881252, 'P4'),
    (27.3067063, 49.4886710, 'P5'), (27.3072740, 49.4895351, 'P6'),
    (27.3070228, 49.4899320, 'P7'), (27.3064455, 49.4890930, 'P8')
]

for lat, lon, label in nursery_coords:
    folium.CircleMarker(
        location=[lat, lon], radius=6,
        color='#FF6F00', fill=True, fill_color='#FF6F00',
        fill_opacity=0.9, weight=2,
        tooltip=f"Nursery Boundary {label}: {lat:.6f}N, {lon:.6f}E"
    ).add_to(m4)

# Natural mangrove reference (7 ha stand)
folium.CircleMarker(
    location=[27.3060, 49.4880], radius=15,
    color='#1B5E20', fill=True, fill_color='#1B5E20',
    fill_opacity=0.5, weight=3,
    tooltip="Natural Mangrove Stand (~7 ha) - Propagule Source"
).add_to(m4)

folium.Marker(
    location=[27.3075, 49.489],
    icon=folium.DivIcon(html='<div style="font-size:14px;font-weight:bold;color:white;text-shadow:2px 2px 4px black;">Nursery (2.17 ha)</div>')
).add_to(m4)

plugins.MeasureControl(position='topleft').add_to(m4)
m4.save(str(OUTPUT / "04_nursery_site.html"))
print(f"  Saved: {OUTPUT / '04_nursery_site.html'}")


# ═══════════════════════════════════════════════════════════
# MAP 5: CONTROL SITES MAP
# ═══════════════════════════════════════════════════════════
print("[6/6] Creating Map 5: Control Sites...")

ctrl_center = [control.geometry.y.mean(), control.geometry.x.mean()]
m5 = folium.Map(location=ctrl_center, zoom_start=11,
                tiles=None, width=1200, height=800)
add_satellite_tiles(m5)

# Add all planting zones as context
for idx2, row2 in all_zones.iterrows():
    folium.GeoJson(
        gpd.GeoSeries([row2.geometry]).__geo_interface__,
        style_function=lambda x: {
            'fillColor': '#2E7D32', 'color': '#2E7D32', 'weight': 1,
            'fillOpacity': 0.2
        },
        tooltip=f"Planting: {row2['NAME']}"
    ).add_to(m5)

# Control sites with detailed markers
ctrl_details = {
    'Control_Unplanted_1': {
        'desc': 'Unplanted Control - Adjacent intertidal (50m buffer)',
        'purpose': 'Baseline comparison',
        'color': '#E53935'
    },
    'Control_Natural_Ref': {
        'desc': 'Natural Reference - Existing 7 ha mangrove stand',
        'purpose': 'Growth benchmarking',
        'color': '#1E88E5'
    },
    'Control_Substrate_1': {
        'desc': 'Substrate Control - Representative bare plots',
        'purpose': 'Soil development tracking',
        'color': '#FB8C00'
    }
}

for idx3, row3 in control.iterrows():
    info = ctrl_details.get(row3['NAME'], {})
    folium.CircleMarker(
        location=[row3['LATITUDE'], row3['LONGITUDE']],
        radius=15, color=info.get('color', '#FF0000'), fill=True,
        fill_color=info.get('color', '#FF0000'),
        fill_opacity=0.7, weight=3,
        tooltip=f"{info.get('desc', row3['NAME'])}<br>Purpose: {info.get('purpose', 'N/A')}<br>Coords: {row3['LATITUDE']:.4f}N, {row3['LONGITUDE']:.4f}E"
    ).add_to(m5)

    folium.Marker(
        location=[row3['LATITUDE'] + 0.005, row3['LONGITUDE']],
        icon=folium.DivIcon(html=f'<div style="font-size:11px;font-weight:bold;color:{info.get("color", "#FF0000")};text-shadow:1px 1px 2px black;white-space:nowrap;">{info.get("desc", row3["NAME"])}</div>')
    ).add_to(m5)

# Nursery
folium.GeoJson(
    gpd.GeoSeries([nursery.iloc[0].geometry]).__geo_interface__,
    style_function=lambda x: {
        'fillColor': NURSERY_COLOR, 'color': NURSERY_COLOR,
        'weight': 2, 'fillOpacity': 0.5
    },
    tooltip="Nursery Site"
).add_to(m5)

plugins.MeasureControl(position='topleft').add_to(m5)
folium.LayerControl().add_to(m5)
m5.save(str(OUTPUT / "05_control_sites.html"))
print(f"  Saved: {OUTPUT / '05_control_sites.html'}")


# ═══════════════════════════════════════════════════════════
# STATIC MAPS (PNG) for DOCX Report
# ═══════════════════════════════════════════════════════════
print("\n[BONUS] Creating static PNG maps for report...")

# --- Overview Static Map ---
fig, ax = plt.subplots(1, 1, figsize=(14, 10))
fig.patch.set_facecolor('#1a1a2e')
ax.set_facecolor('#16213e')

# Plot planting zones
for idx4, row4 in final_poly.iterrows():
    color = site_colors[idx4 % 4]
    gpd.GeoSeries([row4.geometry]).plot(ax=ax, color=color, alpha=0.6,
                                        edgecolor='white', linewidth=2)
    centroid = row4.geometry.centroid
    ax.annotate(f"Site {idx4+1}\n{row4['AREA_HA']:.0f} ha",
                xy=(centroid.x, centroid.y),
                fontsize=11, fontweight='bold', color='white',
                ha='center', va='center',
                bbox=dict(boxstyle='round,pad=0.3', facecolor=color, alpha=0.8))

# Plot survey points
final_pts.plot(ax=ax, color='#FFD600', markersize=15, alpha=0.8,
               edgecolor='black', linewidth=0.5, zorder=5)

# Plot control sites
for idx5, row5 in control.iterrows():
    color = CONTROL_COLORS.get(row5['NAME'], '#FF0000')
    ax.plot(row5['LONGITUDE'], row5['LATITUDE'], 'D',
            color=color, markersize=12, markeredgecolor='white',
            markeredgewidth=2, zorder=6)
    ax.annotate(row5['NAME'].replace('Control_', '').replace('_', ' '),
                xy=(row5['LONGITUDE'], row5['LATITUDE']),
                xytext=(10, 10), textcoords='offset points',
                fontsize=9, color=color, fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.2', facecolor='black', alpha=0.7))

# Plot nursery
nursery.plot(ax=ax, color=NURSERY_COLOR, alpha=0.6,
             edgecolor='white', linewidth=2)

# Formatting
ax.set_title('8MM Mangrove Restoration - Phase 2 Sites Overview\nAl Batinah Island, Eastern Province, Saudi Arabia',
             fontsize=16, fontweight='bold', color='white', pad=15)
ax.set_xlabel('Longitude (E)', fontsize=12, color='white')
ax.set_ylabel('Latitude (N)', fontsize=12, color='white')
ax.tick_params(colors='white', labelsize=10)

# Legend
legend_elements = [
    mpatches.Patch(facecolor='#1B5E20', edgecolor='white', label='Planting Zones'),
    plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#FFD600',
               markersize=8, label='Survey Points', linestyle='None'),
    plt.Line2D([0], [0], marker='D', color='w', markerfacecolor='#E53935',
               markersize=8, label='Control: Unplanted', linestyle='None'),
    plt.Line2D([0], [0], marker='D', color='w', markerfacecolor='#1E88E5',
               markersize=8, label='Control: Natural Ref', linestyle='None'),
    plt.Line2D([0], [0], marker='D', color='w', markerfacecolor='#FB8C00',
               markersize=8, label='Control: Substrate', linestyle='None'),
    mpatches.Patch(facecolor=NURSERY_COLOR, edgecolor='white', label='Nursery (2.17 ha)'),
]
ax.legend(handles=legend_elements, loc='lower right', fontsize=10,
          facecolor='black', edgecolor='white', labelcolor='white')

# Grid
ax.grid(True, alpha=0.2, color='white')

plt.tight_layout()
plt.savefig(str(OUTPUT / "overview_static.png"), dpi=200, bbox_inches='tight',
            facecolor=fig.get_facecolor())
plt.close()
print(f"  Saved: overview_static.png")

# --- Individual site static maps ---
for idx6, row6 in final_poly.iterrows():
    site_num = idx6 + 1
    fig2, ax2 = plt.subplots(1, 1, figsize=(10, 8))
    fig2.patch.set_facecolor('#1a1a2e')
    ax2.set_facecolor('#16213e')

    gpd.GeoSeries([row6.geometry]).plot(ax=ax2, color=site_colors[idx6 % 4],
                                        alpha=0.5, edgecolor='white', linewidth=2.5)

    # Points within this site
    site_pts = final_pts[
        final_pts.geometry.within(row6.geometry.buffer(0.005))
    ]
    if len(site_pts) > 0:
        site_pts.plot(ax=ax2, color='#FFD600', markersize=25, alpha=0.9,
                      edgecolor='black', linewidth=0.5, zorder=5)

    ax2.set_title(f'Site {site_num} - {row6["AREA_HA"]:.1f} ha\n8MM Mangrove Plantation Phase 2',
                  fontsize=14, fontweight='bold', color='white', pad=10)
    ax2.set_xlabel('Longitude (E)', fontsize=11, color='white')
    ax2.set_ylabel('Latitude (N)', fontsize=11, color='white')
    ax2.tick_params(colors='white', labelsize=9)
    ax2.grid(True, alpha=0.2, color='white')

    plt.tight_layout()
    plt.savefig(str(OUTPUT / f"site_{site_num}_static.png"), dpi=200,
                bbox_inches='tight', facecolor=fig2.get_facecolor())
    plt.close()
    print(f"  Saved: site_{site_num}_static.png")


# --- Nursery static map ---
fig3, ax3 = plt.subplots(1, 1, figsize=(10, 8))
fig3.patch.set_facecolor('#1a1a2e')
ax3.set_facecolor('#16213e')

nursery.plot(ax=ax3, color=NURSERY_COLOR, alpha=0.5,
             edgecolor='white', linewidth=2.5)

for lat, lon, label in nursery_coords:
    ax3.plot(lon, lat, 'o', color='#FF6F00', markersize=10,
             markeredgecolor='white', markeredgewidth=1.5, zorder=5)
    ax3.annotate(label, xy=(lon, lat), xytext=(5, 5),
                 textcoords='offset points', fontsize=9,
                 color='#FF6F00', fontweight='bold')

ax3.set_title('Nursery Site - Abu Ali Island Southern Shore\nArea: 2.17 ha | Capacity: 8,000,000 seedlings',
              fontsize=14, fontweight='bold', color='white', pad=10)
ax3.set_xlabel('Longitude (E)', fontsize=11, color='white')
ax3.set_ylabel('Latitude (N)', fontsize=11, color='white')
ax3.tick_params(colors='white', labelsize=9)
ax3.grid(True, alpha=0.2, color='white')
plt.tight_layout()
plt.savefig(str(OUTPUT / "nursery_static.png"), dpi=200,
            bbox_inches='tight', facecolor=fig3.get_facecolor())
plt.close()
print(f"  Saved: nursery_static.png")


# --- Control sites static ---
fig4, ax4 = plt.subplots(1, 1, figsize=(12, 9))
fig4.patch.set_facecolor('#1a1a2e')
ax4.set_facecolor('#16213e')

# Context: all zones
all_zones.plot(ax=ax4, color='#2E7D32', alpha=0.25, edgecolor='#4CAF50', linewidth=1)
nursery.plot(ax=ax4, color=NURSERY_COLOR, alpha=0.4, edgecolor='white', linewidth=1.5)

for idx7, row7 in control.iterrows():
    color = CONTROL_COLORS.get(row7['NAME'], '#FF0000')
    ax4.plot(row7['LONGITUDE'], row7['LATITUDE'], 'D',
             color=color, markersize=16, markeredgecolor='white',
             markeredgewidth=2.5, zorder=6)
    label = row7['NAME'].replace('Control_', '').replace('_', ' ')
    ax4.annotate(f"{label}\n({row7['LATITUDE']:.4f}N, {row7['LONGITUDE']:.4f}E)",
                 xy=(row7['LONGITUDE'], row7['LATITUDE']),
                 xytext=(15, 15), textcoords='offset points',
                 fontsize=10, color=color, fontweight='bold',
                 bbox=dict(boxstyle='round,pad=0.3', facecolor='black', alpha=0.8),
                 arrowprops=dict(arrowstyle='->', color=color, lw=1.5))

ax4.set_title('Control Site Locations\n8MM Mangrove Restoration - SAEP-13 Monitoring Framework',
              fontsize=14, fontweight='bold', color='white', pad=10)
ax4.set_xlabel('Longitude (E)', fontsize=11, color='white')
ax4.set_ylabel('Latitude (N)', fontsize=11, color='white')
ax4.tick_params(colors='white', labelsize=9)

legend4 = [
    plt.Line2D([0], [0], marker='D', color='w', markerfacecolor='#E53935',
               markersize=10, label='Unplanted Control (27.19N, 49.535E)', linestyle='None'),
    plt.Line2D([0], [0], marker='D', color='w', markerfacecolor='#1E88E5',
               markersize=10, label='Natural Reference (27.306N, 49.488E)', linestyle='None'),
    plt.Line2D([0], [0], marker='D', color='w', markerfacecolor='#FB8C00',
               markersize=10, label='Substrate Control (27.20N, 49.55E)', linestyle='None'),
    mpatches.Patch(facecolor='#2E7D32', alpha=0.3, edgecolor='#4CAF50', label='Planting Zones'),
    mpatches.Patch(facecolor=NURSERY_COLOR, alpha=0.4, edgecolor='white', label='Nursery'),
]
ax4.legend(handles=legend4, loc='lower left', fontsize=9,
           facecolor='black', edgecolor='white', labelcolor='white')
ax4.grid(True, alpha=0.2, color='white')
plt.tight_layout()
plt.savefig(str(OUTPUT / "control_sites_static.png"), dpi=200,
            bbox_inches='tight', facecolor=fig4.get_facecolor())
plt.close()
print(f"  Saved: control_sites_static.png")


# ═══════════════════════════════════════════════════════════
# SUMMARY
# ═══════════════════════════════════════════════════════════
print(f"\n{'='*60}")
print(f"  MAP GENERATION COMPLETE")
print(f"  Output directory: {OUTPUT}")
print(f"{'='*60}")
print(f"  Interactive HTML Maps:")
print(f"    01_regional_overview.html")
print(f"    02_all_sites_overview.html")
print(f"    03a-d_site_1-4_detail.html")
print(f"    04_nursery_site.html")
print(f"    05_control_sites.html")
print(f"  Static PNG Maps (for DOCX report):")
print(f"    overview_static.png")
print(f"    site_1-4_static.png")
print(f"    nursery_static.png")
print(f"    control_sites_static.png")
print(f"{'='*60}")
