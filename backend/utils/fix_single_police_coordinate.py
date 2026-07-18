from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="crime_dashboard")

query = "Thilaknagar Police Station, Bengaluru, Karnataka, India"

location = geolocator.geocode(query)

if location:
    print(location.latitude)
    print(location.longitude)
    print(location.address)
else:
    print("Not found")