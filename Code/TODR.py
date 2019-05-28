################################################################################
# TODR.py
#
# PURPOSE: Plots take-off and works out TODR and ground roll for a data set
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

P_o = 104200 # 104200 for leck tests, 100900 for plane

class Data:

    def __init__(self, gps_file, pressure_file, stat_flag): # Save paths to data files

        gps_file
        pressure_file
        stat_flag
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
        self.findStationaryReadings(stat_flag)
        self.startLocation(stat_flag)
        self.createDistanceHeightArrays()

    def parseGPSData(self): # Read the file FileName and parse into a dictionary
        self.parsed_data = []
        self.gps_height = []
        file = open(self.gps_file, "r")
        my_gps = MicropyGPS()
        for line in file:
            print(line)
            comma_pos = line.find(",")
            str_start = comma_pos + 2
            reading_no = line[0:comma_pos]
            if reading_no == '':
                continue
            line = line[str_start:]

            output = "$" # Prepend $ to front of string to make it a full NMEA sentence
            output += line

            for x in output:
                my_gps.update(x)

            # Convert latitude and longitude to decimal degrees
            latitude = my_gps.latitude[0] + my_gps.latitude[1]/60
            if(latitude == 0):
                continue
            longitude = my_gps.longitude[0]*100 + my_gps.longitude[1]/60
            # Convert time to an int of the form HHMMSS.TTT
            timestamp = my_gps.timestamp[0]*10000 + my_gps.timestamp[1]*100 + my_gps.timestamp[2]
            altitude = my_gps.altitude;

            # Save data as an array of dictonaries
            self.parsed_data.append({'Num': reading_no , 'timestamp' : timestamp, 'latitude'  : latitude,'longitude' : longitude, 'altitude' : altitude}) #'satellites': Satellites})

        file.close()

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
                if i > 200:
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

    def greatCircleDistance(self, reading1, reading2): # Comupte the distance between two lat,long points using the haversine formula
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

    def findStationaryReadings(self,stat_flag):

        self.stationary_data = []
        self.run_data = self.parsed_data

        if stat_flag == True:
            start_time = self.run_data[0]['timestamp']
            for item in self.parsed_data:
                delta_t = item['timestamp'] - start_time
                if delta_t > 5:
                    num =int(item['Num'])
                    break
                else:
                    if item['pressure'] != item['pressure']:
                        print('Pressure is a NaN')
                        del(item)
                        continue
                    self.stationary_data.append(item)
            i = 1
            while i < num:
                self.run_data.pop(0)
                i = i + 1
        else:
            while self.run_data[0]['pressure'] != self.run_data[0]['pressure']:
                self.run_data.pop(0)

            self.stationary_data = self.run_data[0]
            self.run_data.pop(0)

    def startLocation(self, stat_flag):
        if stat_flag == False:
            self.start_height = 44330.77 * (1-pow(self.stationary_data['pressure']/P_o,0.1902632))
            self.start_location = {'latitude' : self.stationary_data['latitude'] ,
                                  'longitude': self.stationary_data['longitude'] ,
                                  'pressure' : self.stationary_data['pressure'],
                                  'height'   : self.start_height}
            print(self.start_location)

        else:
            BaseLat = np.empty([])
            BaseLon = np.empty([])
            BasePressure = np.empty([])

            for item in self.stationary_data:
                BaseLat = np.append(BaseLat, item['latitude'])
                BaseLon = np.append(BaseLon, item['longitude'])
                BasePressure = np.append(BasePressure, item['pressure'])

            MeanLat = np.average(BaseLat[1:]) # First reading is wrong for some reason
            MeanLon = np.average(BaseLon[1:])
            BasePressure = BasePressure[2:]
            MeanPressure = np.average(BasePressure)
            self.start_height = 44330.77 * (1-pow(MeanPressure/P_o,0.1902632))

            self.start_location = {'latitude': MeanLat, 'longitude': MeanLon, 'pressure': MeanPressure, 'height' : self.start_height}
            print(self.start_location)

    def calculateDeltaHeight(self, pressure):
        height = 44330.77 * (1-pow(pressure/P_o,0.1902632)) - self.start_height # THIS is not a good way to do this    # Equation from datasheet (based on ISA)
        return delta_height

    def calculateHeight(self, pressure):
        height = 44330.77 * (1-pow(pressure/P_o,0.1902632)) + self.start_height # THIS is not a good way to do this    # Equation from datasheet (based on ISA)
        return height

    def createDistanceHeightArrays(self):
        self.heights = []
        self.smooth_h = []
        self.delta_h = []
        self.distances = []
        self.GPSheight = []
        self.temperatures = []

        for reading in self.run_data:
            height = self.calculateHeight(reading['pressure'])
            #print(reading['pressure'])
            #print(height)
            self.distances.append(self.greatCircleDistance(reading, self.start_location))
            self.heights.append(height)
            #self.GPSheight.append(reading['altitude'])
            self.delta_h.append(height-2*self.start_height)
            self.temperatures.append(reading['temperature'])

        self.smooth_h = self.movingAverage(self.heights, 10, 'hamming')
        self.smooth_dh = self.movingAverage(self.delta_h, 10, 'hamming')

    def plotTempAndPressure(self):
        temps = []
        pres  = []
        time = []
        i = 0
        for reading in self.run_data:
            temps.append(reading['temperature'])
            pres.append(reading['pressure'])
            time.append(i*0.2)
            i = i + 1

        fig = plt.figure()
        ax1 = fig.add_subplot(111)
        ax1.plot(time, pres, 'b-')
        ax1.set_xlabel('Time elapsed (s)')
        ax1.set_ylabel('Pressure (Pa)', color = 'b')
        for tl in ax1.get_yticklabels():
            tl.set_color('b')

        ax2 = ax1.twinx()
        ax2.plot(time, temps, 'r-')
        ax2.set_ylabel('Temperature ($^\circ$C)', color='r')
        for tl in ax2.get_yticklabels():
            tl.set_color('r')

        plt.show()

    def plotDistanceVsHeight(self):
        plt.plot(self.distances, self.heights)
        plt.xlabel('Distance (meters)', fontsize = '22')
        plt.ylabel('Change in height (meters)', fontsize = '22')

    def plotAltitudes(self, colour, label):
        length = len(self.heights)
        time = []
        i = 0
        pres_style = colour + '-'
        GPS_style = colour + '--'
        while i < length:
            time.append(i*0.2)
            i = i + 1

        #fig, ax1 = plt.subplots()
        ax1.plot(time, self.heights, pres_style,  label = label)
        ax1.plot(time, self.GPSheight, GPS_style)
        ax1.set_xlabel('Time elapsed (s)')
        ax1.set_ylabel('Height (m)')
        ax1.legend(fontsize = '22')

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

    def movingAverage(self,array, window_size, window_type):
        data = pd.DataFrame(array)
        rolling_mean_t = []
        rolling = data.rolling(window_size, win_type = window_type, center = True)
        rolling_mean_set = rolling.mean()
        rolling_mean = rolling_mean_set.values

        #rolling_mean_t = rolling_mean.transpose()
        #rolling_mean = rolling_mean[:][1]
        return rolling_mean

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

def pressureMSE(press_list):
    MSE = 0
    RMSE = 0
    for reading in press_list:
        print(reading)
        MSE = MSE + reading*reading

    MSE = MSE/len(press_list)
    RMSE = math.sqrt(MSE)
    return MSE, RMSE
# Main body ####################################################################
plane_run_1 = Data("Test_Data/Plane/First_run/GPS2.txt", "Test_Data/Plane/First_run/PRE2.txt", True) # Path to the data files
#plane_run_2 = Data("Test_Data/Plane/First_run/GPS5.txt", "Test_Data/Plane/First_run/PRE5.txt", False)
plane_run_3 = Data("Test_Data/Plane/Second_run/GPS2.txt", "Test_Data/Plane/Second_run/PRE2.txt", True)

plane_run_1.findTODR() # Plots results and display values in command line
