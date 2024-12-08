import pandas as pd
import matplotlib.pyplot as plt
import contextily as ctx
from pyproj import Transformer
from shapely.geometry import Point
import geopandas as gpd

data = pd.read_csv('COH_HOSPITALS.csv')

# Transform coordinates from EPSG:3857 to EPSG:4326
transformer = Transformer.from_crs("EPSG:3857", "EPSG:4326", always_xy=True)
data['Longitude'], data['Latitude'] = transformer.transform(data['X'], data['Y'])

# Remove rows with missing or invalid coordinates
data = data.dropna(subset=['Longitude', 'Latitude'])

# Create a GeoDataFrame for plotting
gdf = gpd.GeoDataFrame(
    data,
    geometry=[Point(xy) for xy in zip(data['Longitude'], data['Latitude'])],
    crs="EPSG:4326"
)

# Reproject to EPSG:3857 for compatibility with contextily
gdf = gdf.to_crs(epsg=3857)

# Plot the map
fig, ax = plt.subplots(figsize=(10, 8))
gdf.plot(ax=ax, color='blue', alpha=0.6, label='Hospitals')

# Add a static map background
ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik)

ax.axis('off')

ax.set_title('Hospital Locations', fontsize=16)
# ax.set_xlabel('Longitude', fontsize=12)
# ax.set_ylabel('Latitude', fontsize=12)
# ax.legend()
# ax.grid(True, linestyle='--', alpha=0.5)

static_map_file = 'hospital_map_static.png'
plt.savefig(static_map_file, dpi=300, bbox_inches='tight', pad_inches=0)

# plt.show()
