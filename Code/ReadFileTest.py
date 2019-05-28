################################################################################
# ReadFileTest.py
#
# PURPOSE: Begiing to wirte the post processing code
#
# Written by: Bailey Brookes
# Supervisor: Dr Paul Robertson
################################################################################

# Import Modules ###############################################################
from micropyGPS import MicropyGPS
import csv
import numpy
import math
import matplotlib.pyplot as plt
import numpy as np

plt.rc('xtick',labelsize=22)
plt.rc('ytick',labelsize=22)

# Function Defintions ##########################################################
def parseGPSData(FileName, Output): # Read the file FileName and parse into a dictionary

	file = open(FileName, "r")
	my_gps = MicropyGPS()
	for line in file:

		if line[0] != 'G':
			continue

		output = "$"
		output += line
		print(output)
		for x in output:
			my_gps.update(x)

		latitude = my_gps.latitude[0] + my_gps.latitude[1]/60
		longitude = my_gps.longitude[0]*100 + my_gps.longitude[1]/60
		timestamp = my_gps.timestamp[0]*10000 + my_gps.timestamp[1]*100 + round(my_gps.timestamp[2],0)

		Output.append({'timestamp' : timestamp, 'latitude'  : latitude,'longitude' : longitude}) #'satellites': Satellites})

	file.close()

def parsePressure(FileName, Output):
	file = open(FileName, "r")
	for line, item in zip(file, Output):
		pressure = line
		item['pressure'] = pressure

	file.close()

def greatCircleDistance(reading1, reading2): # Comupte the distance between two lat,long points using the haversine formula
	R = 6371000
	phi_1 = math.radians(reading1['latitude'])
	phi_2 = math.radians(reading2['latitude'])

	delta_phi = math.radians(reading2['latitude'] - reading1['latitude'])
	delta_lambda = math.radians(reading2['longitude'] - reading1['longitude'])

	a = math.sin(delta_phi / 2.0) ** 2 + math.cos(phi_1) * math.cos(phi_2) * math.sin(delta_lambda / 2.0) ** 2

	c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

	meters = R * c  		# Output distance in meters
	km = meters / 1000.0  	# Output distance in kilometers
	return  meters

# Main loop ####################################################################
Output = []
Distance = []
Height = [] # Not true heoght atm
parseGPSData("GPS.txt", Output)
parsePressure("PRESSURE.TXT", Output)

# Calculate Distance
Output = Output[300:] # Rough at the minute
StartPoint = Output[0]
for item in Output:
	Distance.append(greatCircleDistance(StartPoint, item))
	#Height.append(float(item['pressure']) - float(StartPoint['pressure']))
Distance.pop(0)
#Height.pop(0)

plt.plot(Distance)
plt.show()
