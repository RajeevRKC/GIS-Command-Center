"""
8MM Mangrove Restoration Project - Phase 2
Additional Maps: Abu Ali Overview + DEM Elevation Visualizations

Generates:
  1. Abu Ali Island overview map with ALL project overlays
  2. DEM elevation point map (survey points colored by elevation)
  3. DEM interpolated surface map (gridded elevation)
  4. DEM elevation classification map (below/optimal/above)
  5. DEM elevation profile transect
"""

import geopandas as gpd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.colors import LinearSegmentedColormap, BoundaryNorm
from matplotlib.lines import Line2D
import numpy as np
from scipy.interpolate import griddata
from pathlib import Path

# ── Paths ──
BASE = Path(r"D:\My-Applications\70-GIS-Command-Center")
ESRI = BASE / "Work Files - GIS" / "_INBOX" / "ESRI_Data"
OUTPUT = BASE / "outputs" / "maps" / "8mm_report"
OUTPUT.mkdir(parents=True, exist_ok=True)

# ── Load shapefiles ──
print("[1/6] Loading shapefiles...")
final_pts = gpd.read_file(ESRI / "8MM_Final_Locations_Points.shp")
final_poly = gpd.read_file(ESRI / "8MM_Final_Locations_Polygons.shp")
ali_pts = gpd.read_file(ESRI / "Abu_Ali_8MM_Sites_Points.shp")
ali_poly = gpd.read_file(ESRI / "Abu_Ali_8MM_Sites_Polygons.shp")
all_zones = gpd.read_file(ESRI / "All_Planting_Zones.shp")
all_pts = gpd.read_file(ESRI / "All_Survey_Points.shp")
control = gpd.read_file(ESRI / "Control_Sites.shp")
nursery = gpd.read_file(ESRI / "Nursery_Boundary.shp")

# ── Colors ──
ZONE_COLORS = ['#2E7D32', '#1B5E20', '#388E3C', '#43A047',
               '#4CAF50', '#66BB6A', '#81C784', '#A5D6A7',
               '#C8E6C9', '#00695C', '#00897B', '#26A69A']
CONTROL_COLORS = {'Control_Unplanted_1': '#E53935',
                  'Control_Natural_Ref': '#1E88E5',
                  'Control_Substrate_1': '#FB8C00'}
NURSERY_COLOR = '#8E24AA'


# ═══════════════════════════════════════════════════════════
# MAP: ABU ALI ISLAND OVERVIEW WITH ALL OVERLAYS
# ═══════════════════════════════════════════════════════════
print("[2/6] Creating Abu Ali Overview Map...")

fig, ax = plt.subplots(1, 1, figsize=(16, 12))

# Background color (ocean blue)
ax.set_facecolor('#E3F2FD')

# Plot ALL planting zones (Phase 2 + Abu Ali)
for idx, row in all_zones.iterrows():
    color = ZONE_COLORS[idx % len(ZONE_COLORS)]
    gpd.GeoSeries([row.geometry]).plot(ax=ax, color=color, alpha=0.45,
                                       edgecolor=color, linewidth=1.5)

# Plot Abu Ali polygons separately with distinct style
for idx, row in ali_poly.iterrows():
    gpd.GeoSeries([row.geometry]).plot(ax=ax, facecolor='none',
                                       edgecolor='#FF6F00', linewidth=2.5,
                                       linestyle='--')

# Plot Phase 2 polygons with green boundary
for idx, row in final_poly.iterrows():
    gpd.GeoSeries([row.geometry]).plot(ax=ax, facecolor='none',
                                       edgecolor='#1B5E20', linewidth=2.5)

# Plot nursery boundary
nursery.plot(ax=ax, color=NURSERY_COLOR, alpha=0.6,
             edgecolor=NURSERY_COLOR, linewidth=2)

# Plot all survey points (small dots, colored by elevation)
scatter = ax.scatter(all_pts.geometry.x, all_pts.geometry.y,
                     c=all_pts['ELEVATION'], cmap='RdYlGn',
                     s=20, zorder=5, edgecolors='#333', linewidth=0.3,
                     vmin=-1, vmax=2)

# Plot control sites (large markers)
for idx, row in control.iterrows():
    color = CONTROL_COLORS.get(row['NAME'], '#FF0000')
    ax.plot(row['LONGITUDE'], row['LATITUDE'], marker='^', color=color,
            markersize=14, markeredgecolor='white', markeredgewidth=1.5,
            zorder=10)

# Plot nursery center
nursery_center = nursery.geometry.centroid.iloc[0]
ax.plot(nursery_center.x, nursery_center.y, marker='s', color=NURSERY_COLOR,
        markersize=12, markeredgecolor='white', markeredgewidth=1.5, zorder=10)

# Labels for key features
label_style = dict(fontsize=8, fontweight='bold', ha='center',
                   bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                             alpha=0.85, edgecolor='#666'))

# Label planting zones
for idx, row in final_poly.iterrows():
    centroid = row.geometry.centroid
    ax.annotate(f"{row['NAME']}\n{row['AREA_HA']:.0f} ha",
                xy=(centroid.x, centroid.y), **label_style, zorder=15)

# Label Abu Ali zones
for idx, row in ali_poly.iterrows():
    if row['AREA_HA'] > 5:  # Only label larger zones
        centroid = row.geometry.centroid
        ax.annotate(f"{row['NAME']}\n{row['AREA_HA']:.0f} ha",
                    xy=(centroid.x, centroid.y),
                    fontsize=7, fontweight='bold', ha='center', color='#E65100',
                    bbox=dict(boxstyle='round,pad=0.2', facecolor='#FFF3E0',
                              alpha=0.85, edgecolor='#FF6F00'),
                    zorder=15)

# Label nursery
ax.annotate("NURSERY\n2.17 ha", xy=(nursery_center.x, nursery_center.y),
            xytext=(nursery_center.x + 0.015, nursery_center.y + 0.01),
            fontsize=8, fontweight='bold', color=NURSERY_COLOR,
            arrowprops=dict(arrowstyle='->', color=NURSERY_COLOR, lw=1.5),
            bbox=dict(boxstyle='round,pad=0.3', facecolor='#F3E5F5',
                      alpha=0.9, edgecolor=NURSERY_COLOR),
            zorder=15)

# Label control sites
for idx, row in control.iterrows():
    label = row['NAME'].replace('Control_', '').replace('_', ' ')
    ax.annotate(label, xy=(row['LONGITUDE'], row['LATITUDE']),
                xytext=(row['LONGITUDE'] + 0.01, row['LATITUDE'] - 0.005),
                fontsize=7, fontweight='bold',
                color=CONTROL_COLORS.get(row['NAME'], '#FF0000'),
                arrowprops=dict(arrowstyle='->', lw=1),
                zorder=15)

# Colorbar for elevation
cbar = plt.colorbar(scatter, ax=ax, shrink=0.6, pad=0.02)
cbar.set_label('Elevation (m MSL)', fontsize=10)

# Legend
legend_elements = [
    mpatches.Patch(facecolor='#2E7D32', alpha=0.45, edgecolor='#1B5E20',
                   linewidth=2, label='Phase 2 Planting Zones'),
    mpatches.Patch(facecolor='none', edgecolor='#FF6F00', linewidth=2,
                   linestyle='--', label='Abu Ali Site Zones'),
    mpatches.Patch(facecolor=NURSERY_COLOR, alpha=0.6, edgecolor=NURSERY_COLOR,
                   label='Nursery Boundary'),
    Line2D([0], [0], marker='^', color='w', markerfacecolor='#E53935',
           markersize=10, label='Control: Unplanted'),
    Line2D([0], [0], marker='^', color='w', markerfacecolor='#1E88E5',
           markersize=10, label='Control: Natural Reference'),
    Line2D([0], [0], marker='^', color='w', markerfacecolor='#FB8C00',
           markersize=10, label='Control: Substrate'),
    Line2D([0], [0], marker='o', color='w', markerfacecolor='#666',
           markersize=6, label='Survey Points (n=130)'),
]

ax.legend(handles=legend_elements, loc='lower left', fontsize=8,
          framealpha=0.9, edgecolor='#999')

# Styling
ax.set_title('8MM Mangrove Restoration Project - Abu Ali Island Overview\n'
             'All Project Components: Planting Zones, Nursery, Control Sites, Survey Points',
             fontsize=13, fontweight='bold', color='#0D47A1')
ax.set_xlabel('Longitude (E)', fontsize=10)
ax.set_ylabel('Latitude (N)', fontsize=10)
ax.grid(True, alpha=0.3, linestyle='--')
ax.tick_params(labelsize=8)

# Add north arrow text
ax.annotate('N', xy=(0.97, 0.95), xycoords='axes fraction',
            fontsize=16, fontweight='bold', ha='center',
            bbox=dict(boxstyle='circle', facecolor='white', edgecolor='#333'))
ax.annotate('', xy=(0.97, 0.94), xytext=(0.97, 0.88),
            xycoords='axes fraction',
            arrowprops=dict(arrowstyle='->', color='#333', lw=2))

# Scale bar (approximate at this latitude)
# 1 degree longitude ~ 97.5 km at 27N
scale_lon = 0.01  # ~0.975 km
scale_x = ax.get_xlim()[0] + 0.005
scale_y = ax.get_ylim()[0] + 0.003
ax.plot([scale_x, scale_x + scale_lon], [scale_y, scale_y], 'k-', lw=3)
ax.text(scale_x + scale_lon / 2, scale_y + 0.002, '~1 km',
        ha='center', fontsize=8, fontweight='bold')

# Copyright
ax.text(0.99, 0.01, 'Saudi Aramco / AHAB | WGS84 EPSG:4326',
        transform=ax.transAxes, fontsize=7, ha='right', color='#999')

plt.tight_layout()
plt.savefig(OUTPUT / "abu_ali_overview_static.png", dpi=200, bbox_inches='tight',
            facecolor='white')
plt.close()
print("  -> abu_ali_overview_static.png")


# ═══════════════════════════════════════════════════════════
# DEM MAP 1: ELEVATION POINT MAP
# ═══════════════════════════════════════════════════════════
print("[3/6] Creating DEM Elevation Point Map...")

fig, ax = plt.subplots(1, 1, figsize=(14, 10))
ax.set_facecolor('#F5F5F5')

# Plot planting zone boundaries as context
for idx, row in all_zones.iterrows():
    gpd.GeoSeries([row.geometry]).plot(ax=ax, facecolor='none',
                                       edgecolor='#1B5E20', linewidth=1.5,
                                       alpha=0.7)

# Plot nursery boundary
nursery.plot(ax=ax, facecolor='none', edgecolor=NURSERY_COLOR, linewidth=2)

# Elevation colormap (terrain-like)
elev_cmap = LinearSegmentedColormap.from_list('elev',
    ['#08306B', '#2171B5', '#6BAED6',   # deep blue (sub-MSL)
     '#FFFFB2', '#FED976', '#FEB24C',   # yellow-orange (near MSL)
     '#FD8D3C', '#FC4E2A', '#E31A1C',   # red-orange (above optimal)
     '#BD0026', '#800026'],              # dark red (high)
    N=256)

# Plot survey points colored by elevation
scatter = ax.scatter(all_pts.geometry.x, all_pts.geometry.y,
                     c=all_pts['ELEVATION'], cmap=elev_cmap,
                     s=60, zorder=5, edgecolors='#333', linewidth=0.5,
                     vmin=-3, vmax=3.5)

# Add elevation value labels for selected points
for idx, row in all_pts.iterrows():
    if idx % 5 == 0:  # Label every 5th point to avoid clutter
        ax.annotate(f"{row['ELEVATION']:.1f}",
                    xy=(row.geometry.x, row.geometry.y),
                    xytext=(3, 3), textcoords='offset points',
                    fontsize=5, color='#333', alpha=0.8)

# Highlight optimal planting elevation band
ax.text(0.02, 0.97, 'Optimal Planting Elevation: +0.30m to +0.60m MSL',
        transform=ax.transAxes, fontsize=9, fontweight='bold',
        color='#1B5E20', va='top',
        bbox=dict(boxstyle='round,pad=0.4', facecolor='#E8F5E9',
                  edgecolor='#1B5E20', alpha=0.9))

# Stats box
elev = all_pts['ELEVATION']
stats_text = (f"Survey Points: n={len(all_pts)}\n"
              f"Elevation Range: {elev.min():.2f}m to {elev.max():.2f}m\n"
              f"Mean: {elev.mean():.2f}m | Median: {elev.median():.2f}m\n"
              f"Std Dev: {elev.std():.2f}m\n"
              f"Points in Optimal Band: {((elev >= 0.30) & (elev <= 0.60)).sum()} "
              f"({((elev >= 0.30) & (elev <= 0.60)).mean()*100:.0f}%)")
ax.text(0.02, 0.82, stats_text, transform=ax.transAxes, fontsize=8,
        verticalalignment='top', family='monospace',
        bbox=dict(boxstyle='round,pad=0.4', facecolor='white',
                  edgecolor='#999', alpha=0.9))

# Colorbar
cbar = plt.colorbar(scatter, ax=ax, shrink=0.7, pad=0.02, extend='both')
cbar.set_label('Elevation (m above MSL, EGM2008)', fontsize=10)
# Add optimal band markers
cbar.ax.axhline(y=0.30, color='#1B5E20', linewidth=2, linestyle='--')
cbar.ax.axhline(y=0.60, color='#1B5E20', linewidth=2, linestyle='--')

ax.set_title('Digital Elevation Model - Survey Point Elevations\n'
             '130 Ground Control Points | Airbus Pleiades Neo 0.5m Reference',
             fontsize=13, fontweight='bold', color='#0D47A1')
ax.set_xlabel('Longitude (E)', fontsize=10)
ax.set_ylabel('Latitude (N)', fontsize=10)
ax.grid(True, alpha=0.3, linestyle='--')
ax.tick_params(labelsize=8)
ax.text(0.99, 0.01, 'Vertical Datum: EGM2008 | WGS84 EPSG:4326',
        transform=ax.transAxes, fontsize=7, ha='right', color='#999')

plt.tight_layout()
plt.savefig(OUTPUT / "dem_elevation_points.png", dpi=200, bbox_inches='tight',
            facecolor='white')
plt.close()
print("  -> dem_elevation_points.png")


# ═══════════════════════════════════════════════════════════
# DEM MAP 2: INTERPOLATED ELEVATION SURFACE
# ═══════════════════════════════════════════════════════════
print("[4/6] Creating DEM Interpolated Surface Map...")

# Extract coordinates and elevation
x = all_pts.geometry.x.values
y = all_pts.geometry.y.values
z = all_pts['ELEVATION'].values

# Create interpolation grid
margin = 0.005
xi = np.linspace(x.min() - margin, x.max() + margin, 400)
yi = np.linspace(y.min() - margin, y.max() + margin, 400)
xi_grid, yi_grid = np.meshgrid(xi, yi)

# Interpolate using cubic method
zi_grid = griddata((x, y), z, (xi_grid, yi_grid), method='cubic')

# Create figure with two subplots: surface + histogram
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 10),
                                gridspec_kw={'width_ratios': [3, 1]})

# Left: Interpolated surface
terrain_cmap = LinearSegmentedColormap.from_list('terrain_custom',
    ['#053061', '#2166AC', '#4393C3', '#92C5DE',  # deep to shallow water
     '#D1E5F0', '#F7F7F7',                        # near MSL
     '#FDDBC7', '#F4A582', '#D6604D',             # low positive
     '#B2182B', '#67001F'],                        # high ground
    N=256)

im = ax1.pcolormesh(xi_grid, yi_grid, zi_grid, cmap=terrain_cmap,
                     shading='auto', vmin=-3, vmax=3.5)

# Overlay planting zone boundaries
for idx, row in all_zones.iterrows():
    gpd.GeoSeries([row.geometry]).plot(ax=ax1, facecolor='none',
                                        edgecolor='white', linewidth=2)
    gpd.GeoSeries([row.geometry]).plot(ax=ax1, facecolor='none',
                                        edgecolor='#1B5E20', linewidth=1,
                                        linestyle='--')

# Plot survey points
ax1.scatter(x, y, c='black', s=8, zorder=5, alpha=0.5, label='Survey Points')

# Contour lines at key elevations
contour_levels = [-2, -1, 0, 0.3, 0.6, 1.0, 2.0, 3.0]
# Mask NaN before contouring
zi_masked = np.ma.masked_invalid(zi_grid)
cs = ax1.contour(xi_grid, yi_grid, zi_masked, levels=contour_levels,
                  colors='black', linewidths=0.5, alpha=0.6)
ax1.clabel(cs, inline=True, fontsize=7, fmt='%.1f m')

# Highlight optimal planting elevation band with contour fill
optimal_mask = (zi_grid >= 0.30) & (zi_grid <= 0.60)
ax1.contour(xi_grid, yi_grid, zi_grid, levels=[0.30, 0.60],
            colors=['#1B5E20'], linewidths=2, linestyles='solid')

# Colorbar
cbar = plt.colorbar(im, ax=ax1, shrink=0.7, pad=0.02, extend='both')
cbar.set_label('Elevation (m above MSL, EGM2008)', fontsize=10)
cbar.ax.axhline(y=0.30, color='#1B5E20', linewidth=2)
cbar.ax.axhline(y=0.60, color='#1B5E20', linewidth=2)
cbar.ax.text(1.5, 0.30, 'Optimal\nBand', transform=cbar.ax.get_yaxis_transform(),
             fontsize=7, color='#1B5E20', fontweight='bold', va='bottom')

ax1.set_title('Interpolated Elevation Surface (DEM)\n'
              'Cubic Interpolation from 130 Survey Points',
              fontsize=13, fontweight='bold', color='#0D47A1')
ax1.set_xlabel('Longitude (E)', fontsize=10)
ax1.set_ylabel('Latitude (N)', fontsize=10)
ax1.grid(True, alpha=0.2, linestyle='--')
ax1.tick_params(labelsize=8)

# Right: Elevation histogram
ax2.hist(z, bins=30, orientation='horizontal', color='#2171B5', alpha=0.7,
         edgecolor='white', linewidth=0.5)
ax2.axhline(y=0.30, color='#1B5E20', linewidth=2, linestyle='--',
            label='Optimal Band (+0.30m)')
ax2.axhline(y=0.60, color='#1B5E20', linewidth=2, linestyle='--',
            label='Optimal Band (+0.60m)')
ax2.axhspan(0.30, 0.60, alpha=0.15, color='#4CAF50', label='Optimal Zone')
ax2.axhline(y=0, color='#999', linewidth=1, linestyle='-', alpha=0.5,
            label='Mean Sea Level')

ax2.set_xlabel('Count (survey points)', fontsize=10)
ax2.set_ylabel('Elevation (m MSL)', fontsize=10)
ax2.set_title('Elevation\nDistribution', fontsize=11, fontweight='bold',
              color='#0D47A1')
ax2.set_ylim(-3.5, 4.0)
ax2.legend(fontsize=7, loc='upper right')
ax2.grid(True, alpha=0.3, axis='x')

plt.tight_layout()
plt.savefig(OUTPUT / "dem_interpolated_surface.png", dpi=200,
            bbox_inches='tight', facecolor='white')
plt.close()
print("  -> dem_interpolated_surface.png")


# ═══════════════════════════════════════════════════════════
# DEM MAP 3: ELEVATION CLASSIFICATION MAP
# ═══════════════════════════════════════════════════════════
print("[5/6] Creating DEM Elevation Classification Map...")

fig, ax = plt.subplots(1, 1, figsize=(14, 10))

# Classification zones
class_colors = ['#053061', '#2166AC', '#4393C3',  # Sub-MSL (< 0m)
                '#D1E5F0',                         # Low (0 to +0.30m)
                '#4CAF50',                         # Optimal (+0.30 to +0.60m)
                '#FDD835',                         # Marginal (+0.60 to +1.00m)
                '#FF6F00', '#D84315', '#B71C1C']   # Above optimal (>+1.00m)

class_cmap = LinearSegmentedColormap.from_list('class',
    ['#053061', '#2166AC', '#4393C3', '#D1E5F0',
     '#4CAF50',  # optimal band
     '#FDD835', '#FF6F00', '#D84315', '#B71C1C'],
    N=256)

# Use the same interpolated grid
bounds = [-3, -1, 0, 0.15, 0.30, 0.60, 1.00, 2.00, 3.50]
class_norm = BoundaryNorm(bounds, 256)

im = ax.pcolormesh(xi_grid, yi_grid, zi_grid, cmap=class_cmap,
                    norm=class_norm, shading='auto')

# Overlay planting zone boundaries
for idx, row in all_zones.iterrows():
    gpd.GeoSeries([row.geometry]).plot(ax=ax, facecolor='none',
                                        edgecolor='black', linewidth=2)

# Nursery
nursery.plot(ax=ax, facecolor='none', edgecolor=NURSERY_COLOR, linewidth=2.5)

# Control sites
for idx, row in control.iterrows():
    color = CONTROL_COLORS.get(row['NAME'], '#FF0000')
    ax.plot(row['LONGITUDE'], row['LATITUDE'], marker='^', color=color,
            markersize=12, markeredgecolor='white', markeredgewidth=1.5, zorder=10)

# Survey points
ax.scatter(x, y, c='black', s=6, zorder=5, alpha=0.4)

# Colorbar with class labels
cbar = plt.colorbar(im, ax=ax, shrink=0.7, pad=0.02, extend='both')
cbar.set_label('Elevation Classification (m MSL)', fontsize=10)
cbar.set_ticks([-2, -0.5, 0.075, 0.225, 0.45, 0.80, 1.50, 2.75])
cbar.set_ticklabels(['Deep\n(<-1m)', 'Sub-MSL\n(-1 to 0m)',
                      'Low\n(0-0.15m)', 'Marginal\nLow\n(0.15-0.30m)',
                      'OPTIMAL\n(0.30-0.60m)',
                      'Marginal\nHigh\n(0.60-1.0m)',
                      'Above\n(1.0-2.0m)', 'High\n(>2.0m)'])

# Area statistics per classification
total_pts = len(all_pts)
stats_lines = [
    f"ELEVATION CLASSIFICATION SUMMARY",
    f"{'='*35}",
    f"Below MSL (<0m):        {(z < 0).sum():3d} pts ({(z < 0).mean()*100:4.1f}%)",
    f"Low (0 to +0.15m):      {((z >= 0) & (z < 0.15)).sum():3d} pts ({((z >= 0) & (z < 0.15)).mean()*100:4.1f}%)",
    f"Marginal (0.15-0.30m):  {((z >= 0.15) & (z < 0.30)).sum():3d} pts ({((z >= 0.15) & (z < 0.30)).mean()*100:4.1f}%)",
    f"OPTIMAL (0.30-0.60m):   {((z >= 0.30) & (z <= 0.60)).sum():3d} pts ({((z >= 0.30) & (z <= 0.60)).mean()*100:4.1f}%)",
    f"Marginal (0.60-1.00m):  {((z > 0.60) & (z <= 1.00)).sum():3d} pts ({((z > 0.60) & (z <= 1.00)).mean()*100:4.1f}%)",
    f"Above optimal (>1.0m):  {(z > 1.00).sum():3d} pts ({(z > 1.00).mean()*100:4.1f}%)",
]

ax.text(0.02, 0.97, '\n'.join(stats_lines), transform=ax.transAxes,
        fontsize=7.5, verticalalignment='top', family='monospace',
        bbox=dict(boxstyle='round,pad=0.4', facecolor='white',
                  edgecolor='#333', alpha=0.92))

ax.set_title('DEM Elevation Classification for Planting Suitability\n'
             'Optimal Band: +0.30m to +0.60m MSL | Avicennia marina Establishment',
             fontsize=13, fontweight='bold', color='#0D47A1')
ax.set_xlabel('Longitude (E)', fontsize=10)
ax.set_ylabel('Latitude (N)', fontsize=10)
ax.grid(True, alpha=0.2, linestyle='--')
ax.tick_params(labelsize=8)
ax.text(0.99, 0.01, 'Classification per Aramco 8MM Phase 1 Data | EGM2008 Vertical Datum',
        transform=ax.transAxes, fontsize=7, ha='right', color='#666')

plt.tight_layout()
plt.savefig(OUTPUT / "dem_elevation_classification.png", dpi=200,
            bbox_inches='tight', facecolor='white')
plt.close()
print("  -> dem_elevation_classification.png")


# ═══════════════════════════════════════════════════════════
# DEM MAP 4: PER-SITE ELEVATION ANALYSIS
# ═══════════════════════════════════════════════════════════
print("[6/6] Creating Per-Site Elevation Analysis...")

# Split survey points by proximity to each planting zone
# Use Phase 2 final points (62 records) which are the Phase 2 survey points
# and Abu Ali points (68 records) for the Abu Ali sites

fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# Phase 2 sites - identify which points belong to each zone
phase2_pts = final_pts.copy()
ali_survey = ali_pts.copy()

# For Phase 2, we have 4 zones and their points
site_configs = [
    ("Phase 2 - Planting Zone 1", final_poly[final_poly['NAME'] == 'Planting_Zone_01'],
     '#2E7D32'),
    ("Phase 2 - Planting Zone 2", final_poly[final_poly['NAME'] == 'Planting_Zone_02'],
     '#1B5E20'),
    ("Phase 2 - Planting Zone 3", final_poly[final_poly['NAME'] == 'Planting_Zone_03'],
     '#388E3C'),
    ("Phase 2 - Planting Zone 4", final_poly[final_poly['NAME'] == 'Planting_Zone_04'],
     '#43A047'),
]

for i, (title, zone_gdf, color) in enumerate(site_configs):
    ax = axes[i // 2][i % 2]
    ax.set_facecolor('#F5F5F5')

    if len(zone_gdf) > 0:
        zone_geom = zone_gdf.geometry.iloc[0]
        area_ha = zone_gdf['AREA_HA'].iloc[0]

        # Find points within or near this zone
        # Use spatial join with buffer for nearby points
        zone_buffer = zone_gdf.copy()
        zone_buffer['geometry'] = zone_buffer.geometry.buffer(0.005)
        pts_in_zone = gpd.sjoin(all_pts, zone_buffer, how='inner', predicate='within')

        if len(pts_in_zone) > 0:
            # Plot zone boundary
            gpd.GeoSeries([zone_geom]).plot(ax=ax, facecolor='none',
                                             edgecolor=color, linewidth=2.5)

            # Plot points colored by elevation
            sc = ax.scatter(pts_in_zone.geometry.x, pts_in_zone.geometry.y,
                           c=pts_in_zone['ELEVATION'], cmap='RdYlGn',
                           s=80, zorder=5, edgecolors='#333', linewidth=0.5,
                           vmin=-1, vmax=2)

            # Label each point
            for _, pt in pts_in_zone.iterrows():
                ax.annotate(f"{pt['ELEVATION']:.1f}m",
                           xy=(pt.geometry.x, pt.geometry.y),
                           xytext=(4, 4), textcoords='offset points',
                           fontsize=6, color='#333')

            # Colorbar
            cbar = plt.colorbar(sc, ax=ax, shrink=0.7)
            cbar.set_label('Elev. (m)', fontsize=8)
            cbar.ax.axhline(y=0.30, color='#1B5E20', linewidth=2, linestyle='--')
            cbar.ax.axhline(y=0.60, color='#1B5E20', linewidth=2, linestyle='--')

            # Stats
            elev_zone = pts_in_zone['ELEVATION']
            optimal_pct = ((elev_zone >= 0.30) & (elev_zone <= 0.60)).mean() * 100
            stats = (f"n={len(pts_in_zone)} | Area: {area_ha:.0f} ha\n"
                     f"Elev: {elev_zone.min():.2f} to {elev_zone.max():.2f}m\n"
                     f"Mean: {elev_zone.mean():.2f}m\n"
                     f"In optimal band: {optimal_pct:.0f}%")
            ax.text(0.02, 0.97, stats, transform=ax.transAxes, fontsize=7,
                    verticalalignment='top', family='monospace',
                    bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                              edgecolor='#999', alpha=0.9))

            # Optimal band shading
            ax.axhspan(0.30, 0.60, alpha=0.0)  # placeholder for reference

    ax.set_title(title, fontsize=11, fontweight='bold', color='#0D47A1')
    ax.set_xlabel('Longitude (E)', fontsize=8)
    ax.set_ylabel('Latitude (N)', fontsize=8)
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.tick_params(labelsize=7)

fig.suptitle('Per-Site Elevation Analysis - Phase 2 Planting Zones\n'
             'Optimal Planting Elevation: +0.30m to +0.60m MSL (green dashed lines on colorbar)',
             fontsize=14, fontweight='bold', color='#0D47A1', y=1.02)

plt.tight_layout()
plt.savefig(OUTPUT / "dem_per_site_elevation.png", dpi=200,
            bbox_inches='tight', facecolor='white')
plt.close()
print("  -> dem_per_site_elevation.png")


# ── Summary ──
print(f"\n{'=' * 60}")
print(f"  ALL MAPS GENERATED SUCCESSFULLY")
print(f"  Output directory: {OUTPUT}")
print(f"  New maps:")
print(f"    1. abu_ali_overview_static.png  (Abu Ali full overview)")
print(f"    2. dem_elevation_points.png     (DEM survey points)")
print(f"    3. dem_interpolated_surface.png (DEM interpolated grid)")
print(f"    4. dem_elevation_classification.png (DEM suitability)")
print(f"    5. dem_per_site_elevation.png   (Per-site elevation)")
print(f"{'=' * 60}")
