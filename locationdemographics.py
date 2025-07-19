import pandas as pd
import requests
import time
import APIKeys
import re

# Load API Key
API_KEY = APIKeys.api_key

# Load CSV File
df = pd.read_csv("MPA Final Database.csv")

# Initialize variables
milton_count = 0
haltonhills_count = 0
southern_halton_count = 0
other_count = 0
invalid_count = 0
locations_list = []
city_list = []

# Locate addresses column and iterate through the column
locations = df["Address"]


# Check Location function to check where the location is
def check_location(loco_func):
    global milton_count
    global haltonhills_count
    global southern_halton_count
    global other_count
    global invalid_count

    loco_func = str(loco_func)
    loco_func = loco_func.strip().lower()  # Normalize data

    if "milton" in loco_func:
        milton_count += 1
    elif "oakville" in loco_func:
        southern_halton_count += 1
    elif "burlington" in loco_func:
        southern_halton_count += 1
    elif "halton hills" in loco_func:
        haltonhills_count += 1
    elif "nan" in loco_func:
        invalid_count += 1
    else:
        other_count += 1
        cleaned_location = re.sub(r'\s*ca$', '', loco_func)  # Clean location data to have only street names
        locations_list.append(cleaned_location)


# Google Maps API Function to determine city
def get_city_from_address(street_name):
    base_url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "address": street_name + ", Ontario, Canada",
        "key": API_KEY,
        "locationbias": "circle:50000@43.51,-79.87"  # make search more specific, around the Milton region

    }
    response = requests.get(base_url, params=params)
    data = response.json()

    if data["status"] == "OK":
        for component in data["results"][0]["address_components"]:
            if "locality" in component["types"]:
                return component["long_name"]
    else:
        print(f"Error for {street_name}: {data['status']}")
        return None


for location in locations:
    check_location(location)

# Run it for each street in the other list
for street in locations_list:
    city = get_city_from_address(street)
    time.sleep(0.5)  # Respect API rate limits
    city_list.append(city)

# Run it for new city list
for loco in city_list:
    check_location(loco)

# Load data to display in CSV
data_csv = {
    "milton": [milton_count],
    "haltonhills": [haltonhills_count],
    "southern_halton": [southern_halton_count],
    "other_count": [other_count],
    "invalid_count": [invalid_count]
}

# Create CSV
df = pd.DataFrame(data_csv)
df.to_csv("Location Demographics.csv", index=False)
