################################################################################
# DataRate.py
#
# PURPOSE: Invesitgating the data aquisition rate of the GPS
#
# Written by: Bailey Brookes
# Supervisor: Dr Paul Robertson
################################################################################

# Import Modules ###############################################################
from micropyGPS import MicropyGPS
import csv
import math
import matplotlib.pyplot as plt
import numpy as np

plt.rc('xtick',labelsize=22)
plt.rc('ytick',labelsize=22)

# Function Defintions ##########################################################
def parseData(FileName, Output, Corrpupt): # Read the file FileName and parse into a dictionary
	i = 0
	file = open(FileName, "r")
	my_gps = MicropyGPS()
	for line in file:
		if((Corrpupt == 1 and i%2 == 1) or Corrpupt == 0):
			for x in line:
				my_gps.update(x)
				latitude = my_gps.latitude[0] + my_gps.latitude[1]/60
				longitude = my_gps.longitude[0]*100 + my_gps.longitude[1]/60
				timestamp = my_gps.timestamp[0]*10000 + my_gps.timestamp[1]*100 + round(my_gps.timestamp[2],0)
				Satellites = my_gps.satellites_visible()
			if latitude > 0: # A fix to remove zero readings from GPS module
				Output.append({'timestamp' : timestamp, 'latitude' : latitude, 'longitude': longitude, 'satellites': Satellites})
		i = i + 1
	return Output

def latLonPlotter(Readings, LegendLabel): # Unpack dictionary data and plot the data
	lat = []
	lon = []

	for item in Readings:
		lat.append(item['latitude'])
		lon.append(item['longitude'])

	lat.pop(0)
	lon.pop(0)

	plt.plot(lat,lon, marker = 'x', label = LegendLabel)
	plt.scatter(lat,lon)

def search(timestamp, SlowerReadings): # Compare timestamp to that in the base station and reutn the reading at that tiime
	for reading in SlowerReadings:
		if reading['timestamp'] == timestamp:
			return reading
	return 0

def greatCircleDistance(lat1, lat2, lon1, lon2): # Comupte the distance between two lat,long points using the haversine formula
	R = 6371000
	phi_1 = math.radians(lat1)
	phi_2 = math.radians(lat2)

	delta_phi = math.radians(lat2 - lat1)
	delta_lambda = math.radians(lon2 - lon1)

	a = math.sin(delta_phi / 2.0) ** 2 + math.cos(phi_1) * math.cos(phi_2) * math.sin(delta_lambda / 2.0) ** 2

	c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

	meters = R * c  		# Output distance in meters
	km = meters / 1000.0  	# Output distance in kilometers
	return  meters

def greatestDistance(Readings): # Function that computes the greatest euclieden distance in the data
	i = 0
	j = 0
	MaxDistance = 0

	# Unpack dictionary data and plot the data
	lat = []
	lon = []
	for item in Readings:
		lat.append(item['latitude'])
		lon.append(item['longitude'])

	lat.pop(0)
	lon.pop(0)


	while i < len(lat):
		while j <len(lat):
			distance = greatCircleDistance(lat[i], lat[j], lon[i], lon[j])
			if distance > MaxDistance:
				MaxDistance = distance
			j = j + 1
		i = i + 1
	return MaxDistance

def dataUnpacker(dictionary, lat_out, lon_out):
	for item in dictionary:
		lat_out.append(item['latitude'])
		lon_out.append(item['longitude'])

	lat_out.pop(0)
	lon_out.pop(0)

	print("Mean")
	print(np.mean(lat_out))
	print(np.mean(lon_out))
	print("Standard deviation")
	print(np.std(lat_out))
	print(np.std(lon_out))
	print("")

# Main body ####################################################################
OneHz  = []
FiveHz = []
TenHz  = []
parseData("Data_Rate_Tests/15-01-19-1Hz.txt" , OneHz , 0)
parseData("Data_Rate_Tests/15-01-19-5Hz.txt" , FiveHz, 0)
parseData("Data_Rate_Tests/15-01-19-10Hz.txt", TenHz , 0)
latLonPlotter(OneHz , '1 Hz readings')
latLonPlotter(FiveHz, '5 Hz readings')
latLonPlotter(TenHz , '10 Hz readings')
plt.xlabel('Latitude (Decimal Degrees)', fontsize = '22')
plt.ylabel('Longitude (Decimal Degrees)', fontsize = '22')
plt.legend(fontsize = '22')
plt.show()

OneLat = []
OneLon = []
FiveLat = []
FiveLon = []
TenLat = []
TenLon = []

dataUnpacker(OneHz, OneLat, OneLon)
dataUnpacker(FiveHz, FiveLat, FiveLon)
dataUnpacker(TenHz, TenLat, TenLon)

OneHzMax  = greatestDistance(OneHz)
FiveHzMax = greatestDistance(FiveHz)
TenHzMax  = greatestDistance(TenHz)

print(OneHzMax)
print(FiveHzMax)
print(TenHzMax)
