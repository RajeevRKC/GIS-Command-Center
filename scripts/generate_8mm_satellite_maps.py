"""
8MM Mangrove Restoration Project - Phase 2
Satellite Basemap Maps: Shapefiles overlaid on real Esri World Imagery

Generates:
  1. Abu Ali overview with all project components on satellite
  2. Per-site dual-panel: standard satellite view + DEM elevation overlay on satellite
"""

import geopandas as gpd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.lines import Line2D
import contextily as ctx
import numpy as np
from pathlib import Path

# ── Paths ──
BASE = Path(r"D:\My-Applications\70-GIS-Command-Center")
ESRI = BASE / "Work Files - GIS" / "_INBOX" / "ESRI_Data"
OUTPUT = BASE / "outputs" / "maps" / "8mm_report"
OUTPUT.mkdir(parents=True, exist_ok=True)

# ── Load shapefiles (WGS84 EPSG:4326) ──
print("[1/3] Loading shapefiles...")
final_pts = gpd.read_file(ESRI / "8MM_Final_Locations_Points.shp")
final_poly = gpd.read_file(ESRI / "8MM_Final_Locations_Polygons.shp")
ali_pts = gpd.read_file(ESRI / "Abu_Ali_8MM_Sites_Points.shp")
ali_poly = gpd.read_file(ESRI / "Abu_Ali_8MM_Sites_Polygons.shp")
all_zones = gpd.read_file(ESRI / "All_Planting_Zones.shp")
all_pts = gpd.read_file(ESRI / "All_Survey_Points.shp")
control = gpd.read_file(ESRI / "Control_Sites.shp")
nursery = gpd.read_file(ESRI / "Nursery_Boundary.shp")

# ── Reproject everything to Web Mercator (EPSG:3857) for tile alignment ──
print("[2/3] Reprojecting to Web Mercator...")
final_pts_3857 = final_pts.to_crs(epsg=3857)
final_poly_3857 = final_poly.to_crs(epsg=3857)
ali_pts_3857 = ali_pts.to_crs(epsg=3857)
ali_poly_3857 = ali_poly.to_crs(epsg=3857)
all_zones_3857 = all_zones.to_crs(epsg=3857)
all_pts_3857 = all_pts.to_crs(epsg=3857)
control_3857 = control.to_crs(epsg=3857)
nursery_3857 = nursery.to_crs(epsg=3857)

# ── Colors ──
ZONE_COLORS = ['#2E7D32', '#1B5E20', '#388E3C', '#43A047',
               '#4CAF50', '#66BB6A', '#81C784', '#A5D6A7',
               '#C8E6C9', '#00695C', '#00897B', '#26A69A']
CONTROL_COLORS = {'Control_Unplanted_1': '#E53935',
                  'Control_Natural_Ref': '#1E88E5',
                  'Control_Substrate_1': '#FB8C00'}
NURSERY_COLOR = '#8E24AA'
site_colors = ['#2E7D32', '#1B5E20', '#388E3C', '#43A047']

# Elevation colormap
elev_cmap = LinearSegmentedColormap.from_list('elev',
    ['#08306B', '#2171B5', '#6BAED6',
     '#FFFFB2', '#FED976', '#FEB24C',
     '#FD8D3C', '#FC4E2A', '#E31A1C',
     '#BD0026', '#800026'],
    N=256)

# Satellite tile source
SATELLITE_TILES = ctx.providers.Esri.WorldImagery


# ═══════════════════════════════════════════════════════════
# MAP 1: ABU ALI OVERVIEW ON SATELLITE
# ═══════════════════════════════════════════════════════════
print("[3/3] Generating maps...")
print("  Map 1: Abu Ali Overview on satellite...")

fig, ax = plt.subplots(1, 1, figsize=(18, 14))

# Plot all planting zones (semi-transparent fill)
for idx, row in all_zones_3857.iterrows():
    color = ZONE_COLORS[idx % len(ZONE_COLORS)]
    gpd.GeoSeries([row.geometry]).plot(ax=ax, color=color, alpha=0.35,
                                       edgecolor=color, linewidth=1.5)

# Abu Ali polygons (orange dashed border)
for idx, row in ali_poly_3857.iterrows():
    gpd.GeoSeries([row.geometry]).plot(ax=ax, facecolor='none',
                                       edgecolor='#FF6F00', linewidth=2.5,
                                       linestyle='--')

# Phase 2 polygons (bold green border)
for idx, row in final_poly_3857.iterrows():
    gpd.GeoSeries([row.geometry]).plot(ax=ax, facecolor='none',
                                       edgecolor='#00E676', linewidth=2.5)

# Nursery
nursery_3857.plot(ax=ax, color=NURSERY_COLOR, alpha=0.6,
                  edgecolor='white', linewidth=2)

# Survey points colored by elevation
scatter = ax.scatter(all_pts_3857.geometry.x, all_pts_3857.geometry.y,
                     c=all_pts['ELEVATION'], cmap='RdYlGn',
                     s=25, zorder=5, edgecolors='white', linewidth=0.4,
                     vmin=-1, vmax=2)

# Control sites (large triangles)
for idx, row in control_3857.iterrows():
    name = control.iloc[idx]['NAME']
    color = CONTROL_COLORS.get(name, '#FF0000')
    ax.plot(row.geometry.x, row.geometry.y, marker='^', color=color,
            markersize=14, markeredgecolor='white', markeredgewidth=1.5,
            zorder=10)

# Nursery center marker
nursery_center = nursery_3857.geometry.centroid.iloc[0]
ax.plot(nursery_center.x, nursery_center.y, marker='s', color=NURSERY_COLOR,
        markersize=12, markeredgecolor='white', markeredgewidth=1.5, zorder=10)

# Labels for zones (use original 4326 for readable coords, plot in 3857)
for idx, row in all_zones_3857.iterrows():
    centroid = row.geometry.centroid
    orig_row = all_zones.iloc[idx]
    name = orig_row.get('NAME', f'Zone {idx+1}')
    area = orig_row.get('AREA_HA', 0)
    short_name = name.replace('Planting_Zone_', 'PZ ').replace('Site_Zone_', 'SZ ')
    ax.annotate(f'{short_name}\n{area:.0f} ha',
                xy=(centroid.x, centroid.y), fontsize=7, fontweight='bold',
                color='white', ha='center', va='center',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='black', alpha=0.7))

# Label nursery
ax.annotate('NURSERY\n2.17 ha', xy=(nursery_center.x, nursery_center.y),
            xytext=(20, 20), textcoords='offset points',
            fontsize=8, fontweight='bold', color=NURSERY_COLOR,
            bbox=dict(boxstyle='round,pad=0.3', facecolor='black', alpha=0.8),
            arrowprops=dict(arrowstyle='->', color=NURSERY_COLOR, lw=1.5))

# Label control sites
for idx, row in control_3857.iterrows():
    name = control.iloc[idx]['NAME']
    label = name.replace('Control_', '').replace('_', ' ')
    color = CONTROL_COLORS.get(name, '#FF0000')
    ax.annotate(label, xy=(row.geometry.x, row.geometry.y),
                xytext=(15, -15), textcoords='offset points',
                fontsize=7, fontweight='bold', color=color,
                bbox=dict(boxstyle='round,pad=0.2', facecolor='black', alpha=0.7))

# Add satellite basemap
ctx.add_basemap(ax, source=SATELLITE_TILES, zoom=14)

# Colorbar
cbar = plt.colorbar(scatter, ax=ax, shrink=0.6, pad=0.01)
cbar.set_label('Elevation (m MSL)', fontsize=11, color='white')
cbar.ax.tick_params(colors='white', labelsize=9)

# Title and axis styling
ax.set_title('8MM Mangrove Restoration Project - Abu Ali Island Overview\n'
             'All Project Components: Planting Zones, Nursery, Control Sites, Survey Points',
             fontsize=14, fontweight='bold', color='white', pad=15)
ax.set_xlabel('Easting (m)', fontsize=10, color='white')
ax.set_ylabel('Northing (m)', fontsize=10, color='white')
ax.tick_params(colors='white', labelsize=8)

# Legend
legend_elements = [
    mpatches.Patch(facecolor='#4CAF50', alpha=0.35, edgecolor='#00E676',
                   linewidth=2, label='Phase 2 Planting Zones'),
    mpatches.Patch(facecolor='none', edgecolor='#FF6F00', linewidth=2,
                   linestyle='--', label='Abu Ali Site Zones'),
    mpatches.Patch(facecolor=NURSERY_COLOR, alpha=0.6, edgecolor='white',
                   label='Nursery Boundary'),
    Line2D([0], [0], marker='^', color='w', markerfacecolor='#E53935',
           markersize=10, label='Control: Unplanted', linestyle='None'),
    Line2D([0], [0], marker='^', color='w', markerfacecolor='#1E88E5',
           markersize=10, label='Control: Natural Ref', linestyle='None'),
    Line2D([0], [0], marker='^', color='w', markerfacecolor='#FB8C00',
           markersize=10, label='Control: Substrate', linestyle='None'),
    Line2D([0], [0], marker='o', color='w', markerfacecolor='#4CAF50',
           markersize=6, label=f'Survey Points (n={len(all_pts)})', linestyle='None'),
]
ax.legend(handles=legend_elements, loc='lower left', fontsize=8,
          facecolor='black', edgecolor='white', labelcolor='white',
          framealpha=0.85)

# Attribution
ax.text(0.99, 0.01, 'Saudi Aramco | AMAB | WGS84 EPSG:4326\nBasemap: Esri World Imagery',
        transform=ax.transAxes, fontsize=6, color='white', alpha=0.7,
        ha='right', va='bottom')

plt.tight_layout()
outfile = OUTPUT / "abu_ali_overview_satellite.png"
plt.savefig(str(outfile), dpi=200, bbox_inches='tight', facecolor='black')
plt.close()
print(f"    Saved: {outfile.name} ({outfile.stat().st_size / 1024:.0f} KB)")


# ═══════════════════════════════════════════════════════════
# MAPS 2-5: PER-SITE DUAL PANEL ON SATELLITE
# ═══════════════════════════════════════════════════════════
print("  Maps 2-5: Per-site dual-panel on satellite...")

for idx, row in final_poly_3857.iterrows():
    site_num = idx + 1
    geom = row.geometry
    orig_row = final_poly.iloc[idx]
    area_ha = orig_row['AREA_HA']

    # Get survey points within site (tight buffer ~100m in meters for 3857)
    site_pts_3857 = all_pts_3857[all_pts_3857.geometry.within(geom.buffer(100))]
    # Match original elevation data
    site_pts_orig = all_pts.loc[site_pts_3857.index]
    n_pts = len(site_pts_3857)

    # Stats
    if n_pts > 0 and 'ELEVATION' in site_pts_orig.columns:
        elev_min = site_pts_orig['ELEVATION'].min()
        elev_max = site_pts_orig['ELEVATION'].max()
        elev_mean = site_pts_orig['ELEVATION'].mean()
        in_opt = site_pts_orig[
            (site_pts_orig['ELEVATION'] >= 0.30) & (site_pts_orig['ELEVATION'] <= 0.60)
        ]
        pct_opt = len(in_opt) / n_pts * 100
    else:
        elev_min = elev_max = elev_mean = pct_opt = 0

    # ── Create dual panel ──
    fig, (ax_left, ax_right) = plt.subplots(1, 2, figsize=(22, 10))
    fig.patch.set_facecolor('black')

    # Compute shared extent with padding
    minx, miny, maxx, maxy = geom.bounds
    padx = (maxx - minx) * 0.2
    pady = (maxy - miny) * 0.2
    ext = [minx - padx, maxx + padx, miny - pady, maxy + pady]

    # ═══════ LEFT PANEL: Standard satellite view ═══════
    # Site boundary
    gpd.GeoSeries([geom]).plot(ax=ax_left, facecolor='none',
                                edgecolor='#00E676', linewidth=3)
    # Light fill
    gpd.GeoSeries([geom]).plot(ax=ax_left, color='#00E676', alpha=0.15,
                                edgecolor='none')

    # Survey points (white dots)
    if n_pts > 0:
        ax_left.scatter(site_pts_3857.geometry.x, site_pts_3857.geometry.y,
                        color='#FFD600', s=50, zorder=5,
                        edgecolors='black', linewidth=0.5)

    ax_left.set_xlim(ext[0], ext[1])
    ax_left.set_ylim(ext[2], ext[3])

    # Add satellite basemap
    ctx.add_basemap(ax_left, source=SATELLITE_TILES, zoom=15)

    ax_left.set_title(f'Site {site_num} - Satellite View\n{area_ha:.1f} ha | {n_pts} Survey Points',
                       fontsize=13, fontweight='bold', color='white', pad=12)
    ax_left.set_xlabel('Easting (m)', fontsize=9, color='white')
    ax_left.set_ylabel('Northing (m)', fontsize=9, color='white')
    ax_left.tick_params(colors='white', labelsize=7)

    # Left legend
    left_leg = [
        mpatches.Patch(facecolor='#00E676', alpha=0.15, edgecolor='#00E676',
                       linewidth=2, label=f'Planting Zone ({area_ha:.1f} ha)'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor='#FFD600',
               markersize=8, markeredgecolor='black', label=f'Survey Points ({n_pts})',
               linestyle='None'),
    ]
    ax_left.legend(handles=left_leg, loc='lower right', fontsize=8,
                   facecolor='black', edgecolor='white', labelcolor='white',
                   framealpha=0.85)

    # ═══════ RIGHT PANEL: DEM Elevation overlay on satellite ═══════
    # Site boundary
    gpd.GeoSeries([geom]).plot(ax=ax_right, facecolor='none',
                                edgecolor='white', linewidth=3)
    gpd.GeoSeries([geom]).plot(ax=ax_right, color='white', alpha=0.08,
                                edgecolor='none')

    # Elevation-colored points
    if n_pts > 0:
        sc = ax_right.scatter(
            site_pts_3857.geometry.x, site_pts_3857.geometry.y,
            c=site_pts_orig['ELEVATION'].values, cmap=elev_cmap,
            s=100, zorder=5, edgecolors='white', linewidth=0.8,
            vmin=-3, vmax=3.5
        )

        # Elevation labels
        for i, (_, pt3857) in enumerate(site_pts_3857.iterrows()):
            elev_val = site_pts_orig.iloc[i]['ELEVATION']
            ax_right.annotate(
                f"{elev_val:.2f}",
                xy=(pt3857.geometry.x, pt3857.geometry.y),
                xytext=(5, 5), textcoords='offset points',
                fontsize=6, color='white', fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.15', facecolor='black', alpha=0.7)
            )

        # Colorbar
        cbar = plt.colorbar(sc, ax=ax_right, shrink=0.85, pad=0.02)
        cbar.set_label('Elevation (m above MSL)', fontsize=10, color='white')
        cbar.ax.tick_params(colors='white', labelsize=8)
        cbar.ax.axhline(y=0.30, color='#00E676', linewidth=2, linestyle='--')
        cbar.ax.axhline(y=0.60, color='#00E676', linewidth=2, linestyle='--')

    ax_right.set_xlim(ext[0], ext[1])
    ax_right.set_ylim(ext[2], ext[3])

    # Add satellite basemap
    ctx.add_basemap(ax_right, source=SATELLITE_TILES, zoom=15)

    ax_right.set_title(
        f'Site {site_num} - DEM Elevation Overlay\n'
        f'Range: {elev_min:+.2f}m to {elev_max:+.2f}m | Mean: {elev_mean:+.2f}m | {pct_opt:.0f}% Optimal',
        fontsize=13, fontweight='bold', color='white', pad=12)
    ax_right.set_xlabel('Easting (m)', fontsize=9, color='white')
    ax_right.set_ylabel('Northing (m)', fontsize=9, color='white')
    ax_right.tick_params(colors='white', labelsize=7)

    # Stats box
    stats = (
        f"Elevation Statistics\n"
        f"{'='*25}\n"
        f"Points:    {n_pts}\n"
        f"Min:       {elev_min:+.2f} m\n"
        f"Max:       {elev_max:+.2f} m\n"
        f"Mean:      {elev_mean:+.2f} m\n"
        f"Optimal:   {pct_opt:.0f}%\n"
        f"(+0.30 to +0.60m MSL)"
    )
    ax_right.text(0.02, 0.97, stats, transform=ax_right.transAxes,
                  fontsize=8, fontfamily='monospace', color='white',
                  verticalalignment='top',
                  bbox=dict(boxstyle='round,pad=0.5', facecolor='black',
                            edgecolor='#4FC3F7', alpha=0.85))

    # Suptitle
    fig.suptitle(f'8MM Mangrove Plantation Phase 2 - Site {site_num} Comparison',
                 fontsize=16, fontweight='bold', color='white', y=0.98)

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    outfile = OUTPUT / f"site_{site_num}_satellite_dem.png"
    plt.savefig(str(outfile), dpi=200, bbox_inches='tight', facecolor='black')
    plt.close()
    print(f"    Saved: {outfile.name} ({outfile.stat().st_size / 1024:.0f} KB)")

print("\nAll satellite basemap maps generated.")
