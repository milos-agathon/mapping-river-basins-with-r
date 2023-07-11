# Mapping river basins with R

In this tutorial, I will show you how to use HydroSHEDS data to create a beautiful and informative map of Brazil’s river basins. You will learn how to download, process and visualize the HydroSHEDS data. By the end of this tutorial, you will be able to create your own river basin maps for any region in the world. Ready to dive in? Let’s get started! 🌎🌊

![alt text]([https://github.com/milos-agathon/mapping-river-basins-with-r/blob/main/brazil-basins.png?raw=true)

# py/Main.py
This repo by Myles McManus @mylesmc123 converts the functionality of my R script, and uses Python instead. It also adds the capability to be able to map any Country dynamically.
Just update the inputs in py/main.py to any country, continent, resolution wanted.

Country codes are based on the world_country_borders provided by Gisco as key: "CNTR_ID". 
Source: https://gisco-services.ec.europa.eu/distribution/v2/countries/geojson/CNTR_RG_60M_2020_4326.geojson

## Example Inputs:
res = "60M"
country = "US"
continent = "na" 

## Output
![us-river-basins](https://github.com/mylesmc123/mapping-river-basins-with-r-and-python/assets/64209352/0a9b43ec-e205-4424-b408-a2f315a4ec5e)
