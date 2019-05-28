################################################################################
# PresTemp.py
#
# PURPOSE: Plot pressure reading readings of pressure vs temperature, perform
#          regression analysis
#
# Written by: Bailey Brookes
# Supervisor: Dr Paul Robertson
################################################################################

from micropyGPS import MicropyGPS
from scipy import stats
import csv
import codecs
import numpy as np
import math
import pandas as pd
import matplotlib.pyplot as plt

plt.rc('xtick',labelsize=22)
plt.rc('ytick',labelsize=22)
plt.rcParams.update({'font.size': 22})

pressures = []
temps = []

file = open("Test_Data/Old court/OC_PRE.txt", "r")
for line in file: # Place each pressure reading into each dictonary entry
    comma_pos = line.find(",")
    reading_no = line[0:comma_pos]
    pres_start = comma_pos + 2

    line = line[pres_start:]

    comma_pos = line.find(",")
    pressure = line[0:comma_pos]
    temp_start = comma_pos + 2

    temperature = line[temp_start:]

    pressures.append(float(pressure))
    temps.append(float(temperature))
file.close()

pressures = np.array(pressures)
temps = np.array(temps)
slope, intercept, r_value, p_value, std_err = stats.linregress(temps,pressures)
line = slope * temps + intercept
print(slope)
print(intercept)
print(r_value)
print(p_value)
print(std_err)

fig, ax1 = plt.subplots()
ax1.plot(temps, line, color = 'r', label = 'Line of best fit')
ax1.scatter(temps, pressures, label = 'Data')
plt.xlabel('Temperature($^\circ$C)', fontsize = '22')
plt.ylabel('Pressure (Pa)', fontsize = '22')
plt.legend()
plt.show()
