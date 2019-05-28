################################################################################
# DynamicPressure.py
#
# PURPOSE: Plots pressure vs calcualted speed to look at dynamic pressure
#          effects
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

speed = [4.935083678,
4.077665398,
6.003931046,
6.003930853,
7.078039007,
7.078038708,
8.155329093,
7.93587512,
9.005894468,
10.07935835,
9.870164157,
10.31546401,
10.07935658,
11.80564515,
12.00785527,
11.80564395,
12.87067865,
12.87067787,
13.93896633,
14.61977223,
13.93896429,
14.80523715,
15.23272238,
15.87173532,
15.8717341,
16.08270213,
16.94072432,
16.74057062,
17.80562231,
17.80562084,
18.67644215,
18.49508278,
18.87306949,
19.55239118,
20.4328139,
19.55238811,
20.61269246,
21.48963062]

pressure = [101089.75,
101086.25,
101096.25,
101100.25,
101090.5,
101098,
101100.75,
101107.75,
101121.5,
101108.75,
101105.75,
101109,
101105,
101109.75,
101105.5,
101106.25,
101104.75,
101115,
101104.25,
101106,
101108.25,
101111.5,
101110,
101107.5,
101120.5,
101115.75,
101123,
101134.5,
101140.25,
101151.75,
101169.75,
101167,
101169.25,
101180,
101172.5,
101160.75,
101158.5,
101174]

# plot the model
a = 0.6125
b = 0
c = 101080
x = np.linspace(0,23, 1000)
y = a*x*x + c
print(len(speed))
print(len(pressure))
fig, ax1 = plt.subplots()
ax1.scatter(speed, pressure)
#ax1.plot(x,y)
plt.xlabel('Speed (m/s)', fontsize = '22')
plt.ylabel('Pressure (Pa)', fontsize = '22')
plt.show()
