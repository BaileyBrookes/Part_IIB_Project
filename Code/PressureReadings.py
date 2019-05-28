################################################################################
# PressureReadings.py
#
# PURPOSE: Plot the pressure reading from a CSV file, currently not used. Excell
#		   is used instead
#
# Written by: Bailey Brookes
# Supervisor: Dr Paul Robertson
################################################################################

import csv
import matplotlib.pyplot as plt
import numpy as np
def loadCSV(Filename, OutputName):
	with open(Filename) as csv_file :
		csv_reader = csv.reader(csv_file, delimiter = ',')
		for row in csv_reader:
			OutputName.append(row)

plt.rc('xtick',labelsize=14)
plt.rc('ytick',labelsize=14)

Readings = []
time = []
alt = []
loadCSV("11-11-18/PRESSURE_WALK.txt", Readings)
for item in Readings:
	print(item)
	time.append(item[0])
	alt.append(item[1])

time.pop(0)
alt.pop(0)
print(time)
print(alt)
plt.plot(np.array(alt))
plt.xlabel("Reading", fontsize = '18')
plt.ylabel("Altitude (m)", fontsize = '18')
plt.show()

print(np.mean(array))
print(np.var(array))
