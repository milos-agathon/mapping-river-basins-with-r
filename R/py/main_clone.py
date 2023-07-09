import urllib.request
import zipfile
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import ListedColormap

# 1. GET COUNTRY BORDERS
# -----------------------
print("GET COUNTRY BORDERS")
resolution = "3"
country = "US"


def get_country_borders(resolution, country):
    country_borders = gpd.read_file(
        "https://gisco-services.ec.europa.eu/distribution/v2/countries/geojson/CNTR_RG_60M_2020_4326.geojson")

    return country_borders


country_borders = get_country_borders(resolution, country)

# 2. GET BASINS
# --------------
print("GET BASINS")


def get_basins():
    url = "https://data.hydrosheds.org/file/HydroBASINS/standard/hybas_na_lev03_v1c.zip"
    file_name = "hybas_na_lev03_v1c.zip"

    urllib.request.urlretrieve(url, file_name)
    with zipfile.ZipFile(file_name, 'r') as zip_ref:
        zip_ref.extractall()


get_basins()
print("basin downloaded")

file_names = [filename for filename in os.listdir()
              if filename.endswith(".shp")]
print("load basin")


def load_basins():
    print("loading filenames")
    filenames = [
        filename for filename in file_names if filename.endswith(".shp")]
    print(filenames)
    namerica_basin = gpd.read_file(filenames[0])

    return namerica_basin


namerica_basin = load_basins()
print("basin loaded")

print("Intersect Basin with only the wanted Country Boundary.")
gpd.sjoin(country_borders, namerica_basin)

# 3. GET RIVERS DATA
# -------------------
print("Get Rivers")


def get_rivers():
    url = "https://data.hydrosheds.org/file/HydroRIVERS/HydroRIVERS_v10_na_shp.zip"
    file_name = "na-rivers.zip"

    urllib.request.urlretrieve(url, file_name)
    with zipfile.ZipFile(file_name, 'r') as zip_ref:
        zip_ref.extractall()


get_rivers()
print("Getting Rivers")
list_files = [filename for filename in os.listdir(
    "HydroRIVERS_v10_na_shp") if filename.endswith(".shp")]
print(list_files)


def load_rivers():
    filenames = [os.path.join("HydroRIVERS_v10_na_shp", filename)
                 for filename in list_files]
    print(filenames)
    namerica_rivers = gpd.read_file(filenames[0])

    return namerica_rivers


namerica_rivers = load_rivers()

# 4. DETERMINE BASIN FOR EVERY RIVER
# ---------------------------------

country_river_basin = gpd.overlay(
    namerica_rivers, namerica_basin, how='intersection')

# 5. RIVER WIDTH
# --------------

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

# 6. PLOT
# --------

country_river_basin['HYBAS_ID'].unique()

cmap = ListedColormap(cm.get_cmap('Dark2').colors[:14])

fig, ax = plt.subplots(figsize=(7, 7.75))
country_river_basin.plot(ax=ax, column='HYBAS_ID', cmap=cmap,
                         linewidth=country_river_basin['width']*10, edgecolor='black', alpha=country_river_basin['width'])
ax.set_axis_off()
plt.title('')
plt.savefig('us-river-basins.png', dpi=600,
            bbox_inches='tight', pad_inches=0, transparent=True)

country_river_basin.to_file("us-river-basins.geojson", driver="GeoJSON")
