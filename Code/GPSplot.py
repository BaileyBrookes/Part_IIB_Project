################################################################################
# GPSplot.py
#
# PURPOSE: Read and NMEA file, parse the information and plot the location
#          of  each reading.
#
# Written by: Bailey Brookes
# Supervisor: Dr Paul Robertson
################################################################################

# Import required modules
from micropyGPS import MicropyGPS
import matplotlib.pyplot as plt
import numpy as np
import csv
import math

# Function that comupte the distance between two lat,long points using the
# haversine formula
def greatCircleDistance(lat1, lat2, lon1, lon2):
    R = 6371000
    phi_1 = math.radians(lat1)
    phi_2 = math.radians(lat2)

    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2.0) ** 2 + math.cos(phi_1) * math.cos(phi_2) * math.sin(delta_lambda / 2.0) ** 2

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    meters = R * c  # output distance in meters
    km = meters / 1000.0  # output distance in kilometers
    return  meters

# Function that computes the greatest euclieden distance in the data
def greatestDistance(lat, lon):
    i = 0
    j = 0
    MaxDistance = 0
    while i < len(lat):
        while j <len(lat):
            distance = greatCircleDistance(lat[i], lat[j], lon[i], lon[j])
            if distance > MaxDistance:
                MaxDistance = distance
            j = j + 1
        i = i + 1
    return MaxDistance

# Open NEMA files to be parsed
file = open("11-11-18/GPS_STILL_BASE.txt", "r")

# Arrays to hold data
lat = np.empty([])
lon = np.empty([])
my_gps = MicropyGPS()

# Read data file and store the MM.SS in an array
for line in file:
    for x in line:
        my_gps.update(x)
        lat = np.append(lat, my_gps.latitude[0] *100 + my_gps.latitude[1])
        lon = np.append(lon, my_gps.longitude[0]*100 + my_gps.longitude[1])

# Remove weired zeros in reading
lat = lat[50:]
lon = lon[50:]

# Compute averave location
LatAverage = np.average(lat)
LonAverage = np.average(lon)

LatError = lat-LatAverage
LonError = lon - LonAverage

# Write data to CSV file
with open('GPS_file.csv', mode='w') as GPS_file:
    GPS_writter = csv.writer(GPS_file)
    GPS_writter.writerow(lat)
    GPS_writter.writerow(lon)

# Plot results
plt.plot(lat,lon)
plt.scatter(lat,lon)
plt.xlabel("Variation in Latitude")
plt.ylabel("Variation in Longitude")
plt.show()

# Plot error over time
plt.plot(LatError)
plt.xlabel("Index")
plt.ylabel("Error")
plt.show()

print(greatestDistance(lat,lon))
print(len(LatError))
