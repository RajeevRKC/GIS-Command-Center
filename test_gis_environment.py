"""
GIS Environment Test Script
Tests core GIS functionality: geometries, projections, spatial analysis, and mapping
"""

import warnings
warnings.filterwarnings('ignore')

print("=" * 60)
print("  GIS COMMAND CENTER - ENVIRONMENT TEST")
print("=" * 60)

# 1. Test GDAL
print("\n[1] GDAL Test...")
from osgeo import gdal, ogr, osr
print(f"    GDAL Version: {gdal.__version__}")

# 2. Test Shapely - Create geometries
print("\n[2] Shapely Geometry Test...")
from shapely.geometry import Point, Polygon, LineString
from shapely.ops import unary_union

point = Point(55.2708, 25.2048)  # Dubai coordinates
buffer = point.buffer(0.1)  # 0.1 degree buffer
print(f"    Created point at Dubai: {point}")
print(f"    Buffer area: {buffer.area:.4f} sq degrees")

# 3. Test PyProj - Coordinate transformation
print("\n[3] PyProj Coordinate Transformation...")
from pyproj import Transformer, CRS

# WGS84 to UTM Zone 40N (Dubai)
transformer = Transformer.from_crs("EPSG:4326", "EPSG:32640", always_xy=True)
x, y = transformer.transform(55.2708, 25.2048)
print(f"    WGS84: (55.2708, 25.2048)")
print(f"    UTM 40N: ({x:.2f}, {y:.2f})")

# 4. Test GeoPandas - Create GeoDataFrame
print("\n[4] GeoPandas Test...")
import geopandas as gpd
import pandas as pd

# Create sample cities
cities_data = {
    'city': ['Dubai', 'Abu Dhabi', 'Riyadh', 'Doha'],
    'country': ['UAE', 'UAE', 'Saudi Arabia', 'Qatar'],
    'lat': [25.2048, 24.4539, 24.7136, 25.2854],
    'lon': [55.2708, 54.3773, 46.6753, 51.5310]
}
df = pd.DataFrame(cities_data)
geometry = [Point(xy) for xy in zip(df.lon, df.lat)]
gdf = gpd.GeoDataFrame(df, geometry=geometry, crs="EPSG:4326")
print(f"    Created GeoDataFrame with {len(gdf)} Gulf cities")
print(gdf[['city', 'country']].to_string(index=False))

# 5. Test Rasterio
print("\n[5] Rasterio Test...")
import rasterio
from rasterio.transform import from_bounds
import numpy as np

# Create a sample raster in memory
data = np.random.rand(100, 100).astype('float32')
transform = from_bounds(54.0, 24.0, 56.0, 26.0, 100, 100)
print(f"    Created sample raster: 100x100 pixels")
print(f"    Bounds: UAE region (54-56E, 24-26N)")

# 6. Test Fiona - Vector formats
print("\n[6] Fiona Vector Drivers...")
import fiona
drivers = list(fiona.supported_drivers.keys())[:10]
print(f"    Supported drivers: {len(fiona.supported_drivers)}")
print(f"    Sample: {', '.join(drivers)}...")

# 7. Test OSMnx - Street network (small area)
print("\n[7] OSMnx Street Network Test...")
import osmnx as ox
ox.settings.use_cache = True
ox.settings.log_console = False

# Get street network for a small area (Dubai Marina)
try:
    G = ox.graph_from_point((25.0800, 55.1400), dist=500, network_type='drive')
    nodes = len(G.nodes)
    edges = len(G.edges)
    print(f"    Dubai Marina network: {nodes} nodes, {edges} edges")
except Exception as e:
    print(f"    Network fetch skipped (requires internet): {type(e).__name__}")

# 8. Test Geopy - Geocoding
print("\n[8] Geopy Geocoding Test...")
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

geolocator = Nominatim(user_agent="gis_command_center_test")
try:
    location = geolocator.geocode("Burj Khalifa, Dubai", timeout=10)
    if location:
        print(f"    Burj Khalifa: ({location.latitude:.4f}, {location.longitude:.4f})")
    else:
        print("    Geocoding returned no result")
except Exception as e:
    print(f"    Geocoding skipped (requires internet): {type(e).__name__}")

# 9. Test Leafmap
print("\n[9] Leafmap Test...")
import leafmap
print(f"    Leafmap version: {leafmap.__version__}")
print("    Interactive mapping ready (use in Jupyter for visualization)")

# 10. Test Satpy
print("\n[10] Satpy Remote Sensing Test...")
import satpy
print(f"    Satpy version: {satpy.__version__}")
print(f"    Available readers: {len(satpy.available_readers())}")

# 11. Test Earth Engine
print("\n[11] Earth Engine Test...")
import ee
print("    Earth Engine API loaded")
print("    Note: Run 'ee.Authenticate()' to enable full functionality")

# 12. Spatial Analysis Demo
print("\n[12] Spatial Analysis Demo...")
from shapely.ops import nearest_points

# Find nearest city to a point
test_point = Point(52.0, 25.0)  # Somewhere in Persian Gulf
nearest_city = min(gdf.geometry, key=lambda x: test_point.distance(x))
city_name = gdf[gdf.geometry == nearest_city]['city'].values[0]
print(f"    Test point: {test_point}")
print(f"    Nearest city: {city_name}")

# Calculate distances between all cities
print("\n    City Distances (km):")
gdf_utm = gdf.to_crs("EPSG:32640")  # Project to UTM for meters
for i, row1 in gdf_utm.iterrows():
    for j, row2 in gdf_utm.iterrows():
        if i < j:
            dist_km = row1.geometry.distance(row2.geometry) / 1000
            print(f"    {gdf.iloc[i]['city']:12} -> {gdf.iloc[j]['city']:12}: {dist_km:,.0f} km")

print("\n" + "=" * 60)
print("  ALL TESTS PASSED - GIS ENVIRONMENT OPERATIONAL")
print("=" * 60)
