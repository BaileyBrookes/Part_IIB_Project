################################################################################
# SatelliteCheck.py
#
# PURPOSE: Read and NMEA file, parse the information and plot the location
#          of  each reading.
#
# Written by: Bailey Brookes
# Supervisor: Dr Paul Robertson
################################################################################

# Import Modules
import matplotlib.pyplot as plt
import numpy as np
from micropyGPS import MicropyGPS

def parseData(FileName): # Parse NEMA data to get the satellites that are in view
	Satellites = []
	file = open(FileName, "r")
	my_gps = MicropyGPS()
	for line in file:
		for x in line:
			my_gps.update(x)
			latitude = my_gps.latitude[0] *100 + my_gps.latitude[1]
			longitude = my_gps.longitude[0]*100 + my_gps.longitude[1]
			timestamp = my_gps.timestamp
			Satellites.append(my_gps.satellites_visible())
	Satellites = Satellites[500:]
	return Satellites

# Main body ####################################################################
Satellites = parseData("Base.txt")
i = 0

# Plot results
for item in Satellites:
	print(item)
	print(len(item))
	x = i * np.ones(len(item))
	plt.scatter(x, Satellites[i])
	i = i + 1

plt.show()
