# Script Name: Geocoding_Script.py
# Description: Geocoding the addresses into Geographic and Projected (UTM32-25832)
#              Coordinates by using Nominatim & pyproj library
# Things to change: Chenge the excel file name
# Date:        20-01-2023


import pandas as pd
from geopy.geocoders import Nominatim
import re
import pyproj

# Load the Excel file into a pandas DataFrame
df = pd.read_excel('Mappe1.xlsx')

# Createing object with Nominatim API
geolocator = Nominatim(user_agent="my_application")

# Define the projection systems of Geographic (WGS84) & Projected (UTM 32) coordinates
wgs84 = pyproj.CRS('EPSG:4326')
utm32n = pyproj.CRS('EPSG:25832')
# Create projection conversion object to convert from WGS84 to UTM32 system
transformer = pyproj.Transformer.from_crs(wgs84, utm32n)

# Saving the Index for which geocoding is not found from Nominatim
errors = []

# checking if columns exists in the data or not
cols_to_check = ['Latitude', 'Longitude', 'Easting', 'Northing']
for col in cols_to_check:
    if col not in df.columns:
        df[col] = ''

for index, row in df.iterrows():
    current_index = index + 1
    # Address to be geocoded and separating Street Names from Number
    string = row['Adresse']
    address = re.sub('([a-zA-Z])(\d)', r'\1 \2', string) + " " + row['Gemeinde'] + " Germany"

    # Perform geocoding
    # location = geolocator.geocode(address)
    location = geolocator.geocode(address, timeout=300)

    if location is not None:
        # Print the latitude and longitude of the addressq
        print(f"Index- {current_index} Geographic Coordinates are {location.latitude, location.longitude}.")

        # Set the value of the cell in the 'Latitude' column
        df.at[index, 'Latitude'] = location.latitude
        # Set the value of the cell in the 'Longitude' column
        df.at[index, 'Longitude'] = location.longitude

        # Convert the geographic coordinates to UTM32 (25832)
        easting, northing = transformer.transform(location.longitude, location.latitude)
        # Set the value of the cell in the 'Easting' column
        df.at[index, 'Easting'] = easting
        # Set the value of the cell in the 'Northing' column
        df.at[index, 'Northing'] = northing
        print(f"Index- {current_index} UTM Coordinates are {easting, northing}.")
        print("")

    else:
        errors.append("Location not found for Index-" + str(current_index))

#Getting the errors
if len(errors) != 0:
    print(f"In this script, there are {len(errors)} total errors (Coordinates not found).")
    for error in errors:
        print(error)

# Write the updated data and saving to the same file
df.to_excel('Geocodig_Data.xlsx', index=False)
