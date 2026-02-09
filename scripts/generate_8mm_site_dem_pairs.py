"""
8MM Mangrove Restoration Project - Phase 2
Side-by-Side Site Maps: Standard View + DEM Elevation Overlay

For each of the 4 planting sites, generates a dual-panel figure:
  LEFT:  Site boundary with survey points (standard view)
  RIGHT: Same site boundary with survey points colored by elevation (DEM overlay)
"""

import geopandas as gpd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.lines import Line2D
import numpy as np
from pathlib import Path

# ── Paths ──
BASE = Path(r"D:\My-Applications\70-GIS-Command-Center")
ESRI = BASE / "Work Files - GIS" / "_INBOX" / "ESRI_Data"
OUTPUT = BASE / "outputs" / "maps" / "8mm_report"
OUTPUT.mkdir(parents=True, exist_ok=True)

# ── Load shapefiles ──
print("[1/2] Loading shapefiles...")
final_pts = gpd.read_file(ESRI / "8MM_Final_Locations_Points.shp")
final_poly = gpd.read_file(ESRI / "8MM_Final_Locations_Polygons.shp")
all_pts = gpd.read_file(ESRI / "All_Survey_Points.shp")

# ── Color setup ──
site_colors = ['#2E7D32', '#1B5E20', '#388E3C', '#43A047']

# Elevation colormap (terrain-like: blue->yellow->red)
elev_cmap = LinearSegmentedColormap.from_list('elev',
    ['#08306B', '#2171B5', '#6BAED6',   # deep blue (sub-MSL)
     '#FFFFB2', '#FED976', '#FEB24C',   # yellow-orange (near MSL)
     '#FD8D3C', '#FC4E2A', '#E31A1C',   # red-orange (above optimal)
     '#BD0026', '#800026'],              # dark red (high)
    N=256)

# ── Generate dual-panel maps ──
print("[2/2] Generating side-by-side site maps...")

for idx, row in final_poly.iterrows():
    site_num = idx + 1
    area_ha = row['AREA_HA']
    geom = row.geometry

    # Get survey points within site boundary (tight buffer ~100m for edge points)
    site_pts = all_pts[all_pts.geometry.within(geom.buffer(0.001))]
    n_pts = len(site_pts)

    # Compute site stats
    if n_pts > 0 and 'ELEVATION' in site_pts.columns:
        elev_min = site_pts['ELEVATION'].min()
        elev_max = site_pts['ELEVATION'].max()
        elev_mean = site_pts['ELEVATION'].mean()
        in_optimal = site_pts[
            (site_pts['ELEVATION'] >= 0.30) & (site_pts['ELEVATION'] <= 0.60)
        ]
        pct_optimal = len(in_optimal) / n_pts * 100
    else:
        elev_min = elev_max = elev_mean = pct_optimal = 0

    # ── Create figure: 2 panels side by side ──
    fig, (ax_left, ax_right) = plt.subplots(1, 2, figsize=(20, 9))
    fig.patch.set_facecolor('#1a1a2e')

    # Get extent from site polygon with padding
    minx, miny, maxx, maxy = geom.bounds
    padx = (maxx - minx) * 0.15
    pady = (maxy - miny) * 0.15
    extent = [minx - padx, maxx + padx, miny - pady, maxy + pady]

    # ═══════════════════════════════════════════════
    # LEFT PANEL: Standard View (boundary + yellow dots)
    # ═══════════════════════════════════════════════
    ax_left.set_facecolor('#16213e')

    # Plot site boundary
    gpd.GeoSeries([geom]).plot(ax=ax_left, color=site_colors[idx % 4],
                                alpha=0.5, edgecolor='white', linewidth=2.5)

    # Plot survey points as yellow dots
    if n_pts > 0:
        site_pts.plot(ax=ax_left, color='#FFD600', markersize=40, alpha=0.9,
                      edgecolor='black', linewidth=0.5, zorder=5)

    ax_left.set_xlim(extent[0], extent[1])
    ax_left.set_ylim(extent[2], extent[3])
    ax_left.set_title(f'Site {site_num} - Standard View\n{area_ha:.1f} ha | {n_pts} Survey Points',
                       fontsize=13, fontweight='bold', color='white', pad=12)
    ax_left.set_xlabel('Longitude (E)', fontsize=10, color='white')
    ax_left.set_ylabel('Latitude (N)', fontsize=10, color='white')
    ax_left.tick_params(colors='white', labelsize=8)
    ax_left.grid(True, alpha=0.15, color='white')

    # Left panel legend
    left_legend = [
        mpatches.Patch(facecolor=site_colors[idx % 4], alpha=0.5,
                       edgecolor='white', label=f'Planting Zone ({area_ha:.1f} ha)'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor='#FFD600',
               markersize=8, markeredgecolor='black', label=f'Survey Points ({n_pts})', linestyle='None'),
    ]
    ax_left.legend(handles=left_legend, loc='lower right', fontsize=9,
                   facecolor='#1a1a2e', edgecolor='white', labelcolor='white',
                   framealpha=0.9)

    # ═══════════════════════════════════════════════
    # RIGHT PANEL: DEM Elevation Overlay
    # ═══════════════════════════════════════════════
    ax_right.set_facecolor('#16213e')

    # Plot site boundary (unfilled, white border)
    gpd.GeoSeries([geom]).plot(ax=ax_right, facecolor='none',
                                edgecolor='white', linewidth=2.5)

    # Lightly shade the planting zone for context
    gpd.GeoSeries([geom]).plot(ax=ax_right, color=site_colors[idx % 4],
                                alpha=0.15, edgecolor='none')

    # Plot survey points colored by elevation
    if n_pts > 0:
        scatter = ax_right.scatter(
            site_pts.geometry.x, site_pts.geometry.y,
            c=site_pts['ELEVATION'], cmap=elev_cmap,
            s=80, zorder=5, edgecolors='#333', linewidth=0.5,
            vmin=-3, vmax=3.5
        )

        # Add elevation labels on each point
        for _, pt_row in site_pts.iterrows():
            ax_right.annotate(
                f"{pt_row['ELEVATION']:.2f}",
                xy=(pt_row.geometry.x, pt_row.geometry.y),
                xytext=(4, 4), textcoords='offset points',
                fontsize=6, color='white', fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.15', facecolor='black', alpha=0.6)
            )

        # Add colorbar
        cbar = plt.colorbar(scatter, ax=ax_right, shrink=0.85, pad=0.02)
        cbar.set_label('Elevation (m above MSL)', fontsize=10, color='white')
        cbar.ax.tick_params(colors='white', labelsize=8)

        # Mark optimal band on colorbar
        cbar.ax.axhline(y=0.30, color='#00E676', linewidth=2, linestyle='--')
        cbar.ax.axhline(y=0.60, color='#00E676', linewidth=2, linestyle='--')
        cbar.ax.text(1.5, 0.45, 'OPTIMAL\nBAND', transform=cbar.ax.transData,
                     fontsize=7, color='#00E676', fontweight='bold', ha='left', va='center')

    ax_right.set_xlim(extent[0], extent[1])
    ax_right.set_ylim(extent[2], extent[3])
    ax_right.set_title(f'Site {site_num} - DEM Elevation Overlay\nRange: {elev_min:+.2f}m to {elev_max:+.2f}m | Mean: {elev_mean:+.2f}m | {pct_optimal:.0f}% Optimal',
                        fontsize=13, fontweight='bold', color='white', pad=12)
    ax_right.set_xlabel('Longitude (E)', fontsize=10, color='white')
    ax_right.set_ylabel('Latitude (N)', fontsize=10, color='white')
    ax_right.tick_params(colors='white', labelsize=8)
    ax_right.grid(True, alpha=0.15, color='white')

    # Stats box on right panel
    stats_text = (
        f"Elevation Statistics\n"
        f"{'='*25}\n"
        f"Points:    {n_pts}\n"
        f"Min:       {elev_min:+.2f} m\n"
        f"Max:       {elev_max:+.2f} m\n"
        f"Mean:      {elev_mean:+.2f} m\n"
        f"Optimal:   {pct_optimal:.0f}%\n"
        f"(+0.30 to +0.60m MSL)"
    )
    ax_right.text(0.02, 0.97, stats_text, transform=ax_right.transAxes,
                  fontsize=8, fontfamily='monospace', color='white',
                  verticalalignment='top',
                  bbox=dict(boxstyle='round,pad=0.5', facecolor='#1a1a2e',
                            edgecolor='#4FC3F7', alpha=0.9))

    # ── Suptitle and save ──
    fig.suptitle(f'8MM Mangrove Plantation Phase 2 - Site {site_num} Comparison',
                 fontsize=16, fontweight='bold', color='white', y=0.98)

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    outfile = OUTPUT / f"site_{site_num}_dem_comparison.png"
    plt.savefig(str(outfile), dpi=200, bbox_inches='tight',
                facecolor=fig.get_facecolor())
    plt.close()
    print(f"  Saved: {outfile.name} ({outfile.stat().st_size / 1024:.0f} KB)")

print("\nAll side-by-side site maps generated.")
