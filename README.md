# Fork of Mapping river basins with R
forked from: https://github.com/milos-agathon/mapping-river-basins-with-r/blob/main/brazil-basins.png?raw=true

This forked repo converts the funcitonality of Milo's R script, and uses Python instead. It also adds the capability to be able to run any Country to the map the river basins for dynamically.

# py/Main.py
Just update the inputs in py/main.py to any country, continent, resolution wanted.

Country codes are based on the world_country_borders privded by Gisco as key: "CNTR_ID". 
Source: https://gisco-services.ec.europa.eu/distribution/v2/countries/geojson/CNTR_RG_60M_2020_4326.geojson

## Example Inputs:
res = "60M"
country = "US"
continent = "na" 

## Output
![us-river-basins](https://github.com/mylesmc123/mapping-river-basins-with-r-and-python/assets/64209352/0a9b43ec-e205-4424-b408-a2f315a4ec5e)
