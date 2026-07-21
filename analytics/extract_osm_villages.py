import geopandas as gpd
import pandas as pd
gpkg = r"C:\Users\91767\Downloads\southern-zone-260717-free.gpkg\southern-zone.gpkg"
import pandas as pd

# Load Karnataka boundary
admin = gpd.read_file(gpkg, layer="gis_osm_adminareas_a_free")
karnataka = admin[admin["name"] == "Karnataka"]

# Load all places
places = gpd.read_file(gpkg, layer="gis_osm_places_free")

# Keep only villages
villages = places[places["fclass"] == "village"].copy()

# Ensure same CRS
villages = villages.to_crs(karnataka.crs)

# Spatial filter: villages inside Karnataka
villages_ka = gpd.sjoin(
    villages,
    karnataka,
    predicate="within",
    how="inner"
)

print(villages_ka.columns.tolist())

villages_ka["longitude"] = villages_ka.geometry.x
villages_ka["latitude"] = villages_ka.geometry.y

result = villages_ka[
    ["name_left", "latitude", "longitude"]
].rename(columns={"name_left": "village"})

print("Karnataka villages:", len(result))
print(result.head())



our = pd.read_csv("datasets/processed/village_coordinates.csv")
osm = pd.read_csv("villages_karnataka_osm.csv")

matched = our["village_name"].isin(osm["village"])

print("Our villages:", len(our))
print("OSM Karnataka villages:", len(osm))
print("Matched:", matched.sum())
print("Unmatched:", (~matched).sum())