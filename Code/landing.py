################################################################################
# landing.py
#
# PURPOSE: Plots lanidng for a data set
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

P_o = 100900 # 104200 for leck tests, 100900 for plane

class Data:

    def __init__(self, gps_file, pressure_file): # Save paths to data files

        gps_file
        pressure_file
        parsed_data     = []
        stationary_data = []
        run_data        = []
        offset          = 0
        distances = np.array([])
        heights   = np.array([])

        self.gps_file = gps_file
        self.pressure_file = pressure_file

        # Parses data, stores some reuslts in arrays
        self.parseGPSData2()
        self.parsePressure()

    def parseGPSData2(self):
        self.parsed_data = []
        with codecs.open(self.gps_file,'r', encoding='utf-8', errors = 'ignore') as file:
            csvfile = csv.reader(x.replace('\0', '') for x in file)
            i = 0
            for row in csvfile:
                if row == []:
                    continue

                if(len(row) < 12):
                    #print('Not complete data')
                    continue

                reading_no = row[0]
                if reading_no == '' or reading_no == '0':
                    continue
                timestamp = float(row[2])
                latDMS = str(row[3])
                lonDMS = str(row[5])
                latitude = float(latDMS[0:2]) + float(latDMS[2:])/60
                longitude = float(lonDMS[0:3]) + float(lonDMS[3:])/60
                #altitude = row[10]

                self.parsed_data.append({'Num': reading_no , 'timestamp' : timestamp, 'latitude'  : latitude,'longitude' : longitude})
                if i > 10000:
                    file.close()
                    break
                i = i + 1
            file.close()

    def parsePressure(self): # Save pressure readings into data dictionary

        for item in self.parsed_data:
            valid = False
            number = item['Num']
            file = open(self.pressure_file, "r")
            for line in file: # Place each pressure reading into each dictonary entry
                comma_pos = line.find(",")
                reading_no = line[0:comma_pos]
                pres_start = comma_pos + 2

                line = line[pres_start:]

                comma_pos = line.find(",")
                pressure = line[0:comma_pos]
                temp_start = comma_pos + 2

                temperature = line[temp_start:]

                if reading_no == number:
                    item['pressure'] = float(pressure)
                    item['temperature'] = float(temperature)
                    valid = True
            if valid == False:
                item['pressure'] = float('NaN')
                item['temperature'] = float('NaN')
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

def calculateHeight(pressure):
    height = 44330.77 * (1-pow(pressure/P_o,0.1902632))
    return height

def createDistanceHeightArrays(dic):
    heights = []
    distances = []
    delta_h = []
    start_height = calculateHeight(dic[-1]['pressure'])
    start_location = dic[-1]
    for reading in dic:
        height = calculateHeight(reading['pressure'])
        #print(reading['pressure'])
        #print(height)
        distances.append(greatCircleDistance(reading, start_location))
        heights.append(height)
        #self.GPSheight.append(reading['altitude'])
        delta_h.append(height-start_height)

    return distances, heights, delta_h

    def latLonPlotter(self):
        lat = []
        lon = []
        for item in self.run_data:
            lat.append(item['latitude'])
            lon.append(item['longitude'])

        #fig, ax1 = plt.subplots()
        plt.plot(lat,lon)
        plt.xlabel('Latitude (Decimal Degrees)', fontsize = '22')
        plt.ylabel('Longitude (Decimal Degrees)', fontsize = '22')

    def calculateGroundSpeed(self):
        self.speed = []
        i = 0
        while i < len(self.distances)-1:
            reading1 = self.run_data[i]
            reading2 = self.run_data[i+1]
            distance = self.greatCircleDistance(reading1, reading2)
            self.speed.append(distance/0.2);
            i = i + 1

    def findTODR(self):
        dis_flat = np.array(self.delta_h[:10])
        dis_climb = np.array(self.distances[70:])
        dis = np.array(self.distances)
        runway = np.ones(len(dis))*np.average(dis_flat)
        slope, intercept, r_value, p_value, std_err = stats.linregress(dis_climb,self.delta_h[70:])
        print(slope)
        line = slope * dis + intercept

        self.ground_roll = (np.average(dis_flat) - intercept)/slope
        screen_height = np.average(dis_flat) + 15
        self.todr = (screen_height - intercept)/slope
        print('Ground roll: ' + str(self.ground_roll) + ' m')
        print('TODR: ' + str(self.todr) + ' m')

        plot_size = 150
        fig, ax1 = plt.subplots()
        ax1.plot(self.distances[:plot_size], self.delta_h[:plot_size], label = 'Data')
        ax1.scatter(self.ground_roll, np.average(dis_flat), label = 'Take-off point', color = 'r')
        ax1.scatter(self.todr, screen_height, label = 'TODR', color = 'c')
        ax1.plot(dis[:plot_size], line[:plot_size], label = 'Best fit of climb')
        ax1.plot(dis[:plot_size], runway[:plot_size], label = 'Best fit of run')
        plt.xlabel('Distance (meters)', fontsize = '22')
        plt.ylabel('Change in height (meters)', fontsize = '22')
        plt.legend()
        plt.show()

def averageArray(array):
    mean = sum(array)/len(array)
    ones = np.ones(len(array))
    return ones*mean;

# Main body ####################################################################
plane_run_1 = Data("Test_Data/Plane/First_run/GPS2.txt", "Test_Data/Plane/First_run/PRE2.txt")
#plane_run_2 = Data("Test_Data/Plane/First_run/GPS5.txt", "Test_Data/Plane/First_run/PRE5.txt", False) # No stationary data, so take first point as start location
#plane_run_3 = Data("Test_Data/Plane/Second_run/GPS2.txt", "Test_Data/Plane/Second_run/PRE2.txt", True)

landing = plane_run_1.parsed_data[1300:] # This is a dictionary of the later readings


distances, heights, delta_h = createDistanceHeightArrays(landing)

distances = np.array(distances) * -1
print(distances)
plt.plot(distances, delta_h)
plt.xlabel('Distance (meters)', fontsize = '22')
plt.ylabel('Change in height (meters)', fontsize = '22')
plt.show()
