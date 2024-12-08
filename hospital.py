import folium
from pyproj import Transformer
import pandas as pd
import matplotlib.pyplot as plt

# Convert coordinates to latitude and longitude
# Assuming the coordinates are in EPSG:3857 (Web Mercator), convert to EPSG:4326 (WGS84)

data = pd.read_csv('COH_HOSPITALS.csv')
# print(data.head())

# Reapply the correct transformation from EPSG:3857 to EPSG:4326
transformer = Transformer.from_crs("EPSG:3857", "EPSG:4326", always_xy=True)
data['Longitude'], data['Latitude'] = transformer.transform(data['X'], data['Y'])

# Regenerate the map
hospital_map_corrected = folium.Map(location=[data['Latitude'].mean(), data['Longitude'].mean()], zoom_start=12)

# Add points to the corrected map
for _, row in data.iterrows():
    folium.Marker(
        location=[row['Latitude'], row['Longitude']],
        popup=row['NAME'],
    ).add_to(hospital_map_corrected)

# Save the corrected map to an HTML file
corrected_map_file = 'hospital_map.html'
hospital_map_corrected.save(corrected_map_file)

corrected_map_file


# # Create scatter plot of the hospital locations
# plt.figure(figsize=(10, 8))
# plt.scatter(data['Longitude'], data['Latitude'], c='blue', alpha=0.6, label='Hospitals')
# plt.title('Hospital Locations', fontsize=16)
# plt.xlabel('Longitude', fontsize=12)
# plt.ylabel('Latitude', fontsize=12)
# plt.grid(True, linestyle='--', alpha=0.5)
# plt.legend()

# # Save the non-interactive map as an image
# non_interactive_map_file = 'hospital_map_static.png'
# plt.savefig(non_interactive_map_file, dpi=300)

# plt.show()

