import os
import requests
import zipfile
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import colormaps, pyplot as plt

# Choices of Country Border geojson Resolutions.
resolution_choices = ["01M", "03M", "10M", "30M", "60M"]

# resolution_choices[4] is 60M
res = resolution_choices[4]

# Choose country from ISO code
country = "US"
continent = "na"  # na = North America, sa = South America

world_country_borders = gpd.read_file(
    f"https://gisco-services.ec.europa.eu/distribution/v2/countries/geojson/CNTR_RG_{res}_2020_4326.geojson")
country_border = world_country_borders[world_country_borders["CNTR_ID"] == country]

# Clip US border to just CONUS - excludes Alaska, etc.
if country == "US":
    country_border = country_border.clip_by_rect(-140, 20, -50, 50)
    # clip_by_rect returns a geoseries, so turning back to a GDF
    country_border = gpd.GeoDataFrame(geometry=gpd.GeoSeries(country_border))
    country_border.plot()

# Get Continent-wide Watershed Basin Boundaries
url = f"https://data.hydrosheds.org/file/HydroBASINS/standard/hybas_{continent}_lev03_v1c.zip"
file_name = url.split("/")[-1]

r = requests.get(url)
with open(file_name, 'wb') as outfile:
    outfile.write(r.content)

with zipfile.ZipFile(file_name, 'r') as zip_ref:
    zip_ref.extractall()

# Intersect Basin with only the wanted Country Boundary.
continent_basin = gpd.read_file(file_name.split(".")[0]+".shp")
print("Intersect Basin with only the wanted Country Boundary.")
country_basin = gpd.overlay(
    country_border, continent_basin, how='intersection')

# Get Rivers
url = f"https://data.hydrosheds.org/file/HydroRIVERS/HydroRIVERS_v10_{continent}_shp.zip"
file_name = url.split("/")[-1]

r = requests.get(url)
with open(file_name, 'wb') as outfile:
    outfile.write(r.content)

with zipfile.ZipFile(file_name, 'r') as zip_ref:
    zip_ref.extractall()

continent_rivers = gpd.read_file(os.path.join(
    f"HydroRIVERS_v10_{continent}_shp", f"HydroRIVERS_v10_{continent}.shp"))

# Clip rivers to country_basin extent.
country_river_basin = gpd.overlay(
    continent_rivers, country_basin, how='intersection')

# RIVER WIDTH config

country_river_basin['ORD_FLOW'].unique()


def assign_river_width(row):
    if row['ORD_FLOW'] == 1:
        return 0.8
    elif row['ORD_FLOW'] == 2:
        return 0.7
    elif row['ORD_FLOW'] == 3:
        return 0.6
    elif row['ORD_FLOW'] == 4:
        return 0.45
    elif row['ORD_FLOW'] == 5:
        return 0.35
    elif row['ORD_FLOW'] == 6:
        return 0.25
    elif row['ORD_FLOW'] == 7:
        return 0.2
    elif row['ORD_FLOW'] == 8:
        return 0.15
    elif row['ORD_FLOW'] == 9:
        return 0.1
    else:
        return 0


country_river_basin['width'] = country_river_basin.apply(
    assign_river_width, axis=1)

country_river_basin['HYBAS_ID'].unique()

# 6. PLOT
# --------

fig, ax = plt.subplots(figsize=(7, 7.75))
country_river_basin.plot(ax=ax, column='HYBAS_ID', cmap=colormaps['twilight'],
                         linewidth=country_river_basin['width'],
                         #  edgecolor='black',
                         #  alpha=country_river_basin['width'],
                         categorical=True,
                         #  legend=True
                         )
ax.set_axis_off()

fig.savefig(f'{country}-river-basins.png', dpi=600,
            bbox_inches='tight', pad_inches=0, transparent=True)
