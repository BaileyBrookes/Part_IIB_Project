################################################################################
# CheapDGPS2.py
#
# PURPOSE: Experiemnting witht he idea of a cheap DGPS
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

def baseLocation(BaseStation): # Calcualte mean location of the base GPS module
	BaseLat = np.empty([])
	BaseLon = np.empty([])

	for item in BaseStation:
		BaseLat = np.append(BaseLat, item['latitude'])
		BaseLon = np.append(BaseLon, item['longitude'])

	BaseLat = BaseLat[2:]
	BaseLon = BaseLon[2:]

	MeanLat = np.average(BaseLat)
	MeanLon = np.average(BaseLon)
	plt.scatter(MeanLat, MeanLon, color = 'red', marker = 's', label = "Base location", )
	MeanLocation = {'latitude': MeanLat, 'longitude': MeanLon}
	return MeanLocation

def error(BaseReading, BaseLocation): # Calcualtes error between Mean location and reading passed
	LatError = BaseReading['latitude'] - BaseLocation['latitude']
	LonError = BaseReading['longitude'] - BaseLocation['longitude']
	BaseError = {'latitude': LatError, 'longitude': LonError}
	return BaseError

def search(timestamp): # Compare timestamp to that in the base station and reutn the reading at that tiime
	for reading in BaseStation:
		if reading['timestamp'] == timestamp:
			return reading
	return 0

def correctedReading(RoamingReading, BaseError): # Take Reading and correct it using the error at that time
	CorrectedLat = RoamingReading['latitude']  - BaseError['latitude']
	CorrectedLon = RoamingReading['longitude'] -  BaseError['longitude']
	CorrectedReading = {'latitude': CorrectedLat, 'longitude': CorrectedLon}
	return CorrectedReading

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

def	distances(Base, Roamer):
	LatBase = []
	LonBase = []
	LonRoam = []
	LatRoam = []
	distances = []
	i = 0

	for item in Base:
		LatBase.append(item['latitude'])
		LonBase.append(item['longitude'])

	LatBase.pop(0)
	LonBase.pop(0)

	for item in Roamer:
		LatRoam.append(item['latitude'])
		LonRoam.append(item['longitude'])

	LatRoam.pop(0)
	LonRoam.pop(0)

	while i < len(LatRoam):
		distances.append(greatCircleDistance(LatBase[i], LatRoam[i], LonBase[i], LonRoam[i]))
		i = i + 1
	return distances

def satellites(Station):
	i = 0
	for item in BaseStation:
		x = i * np.ones(len(item['satellites']))
		plt.scatter(x, item['satellites'])
		i = i + 1
	plt.xlabel("Sample")
	plt.ylabel("Satellites in view")
	plt.title("Base Station Satellites")
	plt.show()

def noSatellites(Station):
	NoSatellites = []
	for item in Station:
		NoSatellites.append(len(item['satellites']))
	NoSatellites.pop(0)
	return NoSatellites

def MSE(ErrorArray):
	ErrorsSquared = np.square(ErrorArray)
	return np.sum(ErrorsSquared)/len(ErrorsSquared)

def distanceFromAverage(BaseLocation, CorrectedReadings):
	LonRoam = []
	LatRoam = []
	distances = []
	i = 0
	for item in CorrectedReadings:
		LatRoam.append(item['latitude'])
		LonRoam.append(item['longitude'])

	LatRoam.pop(0)
	LonRoam.pop(0)

	while i < len(LatRoam):
		distances.append(greatCircleDistance(BaseLocation['latitude'],
		 									 LatRoam[i],
											 BaseLocation['longitude'],
											 LonRoam[i]))
		i = i + 1
	print(distances)
	return distances


# Main body ####################################################################
# Empty lists for data, could become types
BaseStation      = []
RoamingStation   = []
CorrectedReading = []
OrginalReading   = []
BaseReadingPair  = []
Errors 			 = []

# Enter NMEA data files to be red
parseData("18-11-18/Base_100m.txt", BaseStation, 0)
parseData("18-11-18/Roamer_100m.txt", RoamingStation, 1)
print("Base")

# Calculate average location of base
BaseLocation = baseLocation(BaseStation)

# Search for the base station reading maches the roaming reading
MissedSearches = 0
for RoamingReading in RoamingStation:
	BaseReading = search(RoamingReading['timestamp'])
	if BaseReading == 0:
		MissedSearches = MissedSearches + 1
	else:
		Error = error(BaseReading, BaseLocation)
		Errors.append(Error)
		Correction = correctedReading(RoamingReading, Error)
		CorrectedReading.append(Correction)
		OrginalReading.append(RoamingReading)
		BaseReadingPair.append(BaseReading)

	if MissedSearches > 10000:
		break

# Plot results
latLonPlotter(BaseReadingPair, 'Base Readings')
latLonPlotter(CorrectedReading, 'Corrected Roaming Readings')
latLonPlotter(OrginalReading, 'Roaming Readings')
plt.xlabel('Latitude (Decimal Degrees)', fontsize = '22')
plt.ylabel('Longitude (Decimal Degrees)', fontsize = '22')
plt.legend(fontsize = '22')
plt.show()

# Plot error corrections
latLonPlotter(Errors, 'Errors')
plt.xlabel("Error in latitude")
plt.show("Error in Longitude")

# Compute greastest distance betweeb 2 points
print(greatestDistance(OrginalReading))
print(greatestDistance(CorrectedReading))

# Plot what satellites in view
#satellites(OrginalReadings)
#satellites(BaseReadingPair)

# Plot the change in distances between 2 points
PitchDistance =   91.44 #5
Uncorrect = distances(BaseReadingPair, OrginalReading)
Corrected = distances(BaseReadingPair, CorrectedReading)
NewUncorrected = distanceFromAverage(BaseLocation, OrginalReading)
NewCorrected = distanceFromAverage(BaseLocation, CorrectedReading)
for item in NewCorrected:
	print(item)
UncorrectError = np.array(Uncorrect) - PitchDistance
CorrectedError = np.array(Corrected) - PitchDistance
NewCorrectedError = np.array(NewCorrected) - PitchDistance
NewUncorrectedError = np.array(NewUncorrected) - PitchDistance
x = np.ones(len(Uncorrect))

fig, ax1 = plt.subplots()
Label = "True Distance = " + str(PitchDistance) + "m"
ax1.plot(x*0, color = 'black', label = Label)

ax1.plot(UncorrectError, 	  label = "$greatCircle(r_i, b_i)$")
ax1.plot(CorrectedError,      label = "$greatCricle(r_{i,c}, b_i)$")
ax1.plot(NewUncorrectedError, label = "$greatCircle(r_i, b)$")
ax1.plot(NewCorrectedError,   label = "$greatCircle(r_{i,c}, b)$")

ax1.set_xlabel("Index",  fontsize = '22')
ax1.set_ylabel("Measured - Ture Distance (m)",  fontsize = '22')
ax1.legend(fontsize = '22')
#ax2 = ax1.twinx()
#NoSatellites = noSatellites(BaseReadingPair)
#ax2.set_ylabel('Number of satellities in view', color = 'green')
#ax2.plot(NoSatellites, color = 'green', linestyle = 'dotted')
fig.tight_layout()  # otherwise the right y-label is slightly clipped
plt.show()

# Print stats about reading variation, first MSE then Standard Deviation
print(MSE(UncorrectError))
print(MSE(CorrectedError))

print(np.std(UncorrectError))
print(np.std(CorrectedError))
