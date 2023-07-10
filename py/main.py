import os
import requests
import zipfile
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import colormaps, pyplot as plt

# INPUTS

# Choices of Country Border geojson Resolutions.
resolution_choices = ["01M", "03M", "10M", "30M", "60M"]

# resolution_choices[4] is 60M
res = resolution_choices[4]

# Choose country from gisco code: "CNTR_ID"
# country = "US"
# EL=Greece, Can always lookup via world_country_borders geojson linked below.
country = "US"
continent = "na"  # na=North America, sa=South America, au=Australia, eu=Europe

# End of Inputs


def CreateMap(country, continent, res):
    print("Getting World's Country Borders")
    world_country_borders = gpd.read_file(
        f"https://gisco-services.ec.europa.eu/distribution/v2/countries/geojson/CNTR_RG_{res}_2020_4326.geojson")
    print(f"Filtering Country Border for: {country}")
    country_border = world_country_borders[world_country_borders["CNTR_ID"] == country]
    if len(country_border) != 1:
        raise ValueError(
            f"Country code: {country} - May be incorrect check world_country_borders for a correct 'CNTR_ID'.")
    country_name = country_border.NAME_ENGL.values[0]

    # Clip US border to just CONUS - excludes Alaska, etc.
    if country == "US":
        country_border = country_border.clip_by_rect(-140, 20, -50, 50)
        # clip_by_rect returns a geoseries, so turning back to a GDF
        country_border = gpd.GeoDataFrame(
            geometry=gpd.GeoSeries(country_border))
        country_border.plot()

    # Get Continent-wide Watershed Basin Boundaries
    print(f"Getting Watershed Basin for Continent: {continent}")
    url = f"https://data.hydrosheds.org/file/HydroBASINS/standard/hybas_{continent}_lev03_v1c.zip"
    file_name = url.split("/")[-1]
    try:
        r = requests.get(url)
        with open(file_name, 'wb') as outfile:
            outfile.write(r.content)
    except:
        raise ConnectionRefusedError(
            f"Unable to Download Watersheds for Continent: {continent}. Check Continent Code.")

    with zipfile.ZipFile(file_name, 'r') as zip_ref:
        zip_ref.extractall()

    # Intersect Basin with only the wanted Country Boundary.
    print("Intersecting Country Border with Continent Watershed Basin.")
    continent_basin = gpd.read_file(file_name.split(".")[0]+".shp")
    country_basin = gpd.overlay(
        country_border, continent_basin, how='intersection')

    # Get Rivers
    print("Getting Continent Rivers.")
    url = f"https://data.hydrosheds.org/file/HydroRIVERS/HydroRIVERS_v10_{continent}_shp.zip"
    file_name = url.split("/")[-1]

    try:
        r = requests.get(url)
        with open(file_name, 'wb') as outfile:
            outfile.write(r.content)
    except:
        raise ConnectionRefusedError(
            f"Unable to Download Rivers for Continent: {continent}. Check Continent Code.")

    with zipfile.ZipFile(file_name, 'r') as zip_ref:
        zip_ref.extractall()

    continent_rivers = gpd.read_file(os.path.join(
        f"HydroRIVERS_v10_{continent}_shp", f"HydroRIVERS_v10_{continent}.shp"))

    # Clip rivers to country_basin extent.
    print("Intersecting Rivers with Country-wide watershed basin.")
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

    print("apply width values to rivers.")
    country_river_basin['width'] = country_river_basin.apply(
        assign_river_width, axis=1)

    country_river_basin['HYBAS_ID'].unique()

    # PLOT
    print("Setup Plot")
    plt.title(country_name)
    fig, ax = plt.subplots(figsize=(7, 7.75))
    country_river_basin.plot(ax=ax,
                             #  column='HYBAS_ID',
                             column='MAIN_RIV',
                             cmap=colormaps['twilight'],
                             linewidth=country_river_basin['width']*3,
                             #  edgecolor='black',
                             #  alpha=country_river_basin['width'],
                             categorical=True,
                             #  legend=True,
                             )
    ax.set_axis_off()

    print("Save Plot")
    fig.savefig(f'{country}-river-basins.png', dpi=600,
                bbox_inches='tight', pad_inches=0, transparent=True)

    # End CreateMap Function


# Create Map
CreateMap(country, continent, res)
