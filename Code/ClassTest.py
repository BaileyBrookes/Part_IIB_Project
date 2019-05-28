################################################################################
# ClassTest.py
#
# PURPOSE: Experiemnting with pytho classes for data processing
#
# Written by: Bailey Brookes
# Supervisor: Dr Paul Robertson
################################################################################

from micropyGPS import MicropyGPS
import csv
import codecs
import numpy as np
import math
import pandas as pd
import matplotlib.pyplot as plt

plt.rc('xtick',labelsize=22)
plt.rc('ytick',labelsize=22)
plt.rcParams.update({'font.size': 22})

P_o = 100900

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

        self.parseGPSData2()
        self.parsePressure()
        self.findStationaryReadings()
        self.startLocation()
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

    def findStationaryReadings(self):
        self.stationary_data = []
        self.run_data = self.parsed_data
        start_time = self.run_data[0]['timestamp']
        for item in self.run_data:
            if item['timestamp'] - start_time > 5:
                break
            else:
                self.stationary_data.append(item)
                self.run_data.pop(0)

    def startLocation(self):
        BaseLat = np.empty([])
        BaseLon = np.empty([])
        BasePressure = np.empty([])

        for item in self.stationary_data:
            BaseLat = np.append(BaseLat, item['latitude'])
            BaseLon = np.append(BaseLon, item['longitude'])
            BasePressure = np.append(BasePressure, item['pressure'])
            print(item['pressure'])

        BaseLat = np.delete(BaseLat,0)
        BaseLon = np.delete(BaseLon,0)
        BasePressure = np.delete(BasePressure,0)
        MeanLat = np.average(BaseLat)
        MeanLon = np.average(BaseLon)
        BasePressure = BasePressure[2:]
        MeanPressure = np.average(BasePressure)
        self.start_height = 44330.77 * (1-pow(MeanPressure/P_o,0.1902632))
        #print(self.start_height)

        self.start_location = {'latitude': MeanLat, 'longitude': MeanLon, 'pressure': MeanPressure, 'height' : self.start_height}

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
            self.delta_h.append(height-self.start_height)
            self.temperatures.append(reading['temperature'])

        #self.smooth_h = self.movingAverage(self.heights, 10)

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

        fig, ax1 = plt.subplots()
        plt.scatter(lat,lon)
        plt.xlabel('Latitude', fontsize = '22')
        plt.ylabel('Longitude', fontsize = '22')


    def movingAverage(self,array, window_size, window_type):
        data = pd.DataFrame(array)
        rolling_mean_t = []
        rolling = data.rolling(window_size, win_type = window_type, center = True)
        rolling_mean_set = rolling.mean()
        rolling_mean = rolling_mean_set.values

        #rolling_mean_t = rolling_mean.transpose()
        #rolling_mean = rolling_mean[:][1]
        return rolling_mean

def averageArray(array):
    mean = sum(array)/len(array)
    ones = np.ones(len(array))
    return ones*mean;

# Main body ####################################################################
"""castle_run_1 = Data("Test_Data/Castle_Hill/GPS1.txt", "Test_Data/Castle_Hill/PRE1.txt")
castle_run_2 = Data("Test_Data/Castle_Hill/GPS2.txt", "Test_Data/Castle_Hill/PRE2.txt")
castle_run_3 = Data("Test_Data/Castle_Hill/GPS3.txt", "Test_Data/Castle_Hill/PRE3.txt")
castle_run_4 = Data("Test_Data/Castle_Hill/GPS4.txt", "Test_Data/Castle_Hill/PRE4.txt")
castle_run_5 = Data("Test_Data/Castle_Hill/GPS5.txt", "Test_Data/Castle_Hill/PRE5.txt")
"""

plane_run_1 = Data("Test_Data/Plane/First_run/GPS2.txt", "Test_Data/Plane/First_run/PRE2.txt")
plane_run_2 = Data("Test_Data/Plane/First_run/GPS5.txt", "Test_Data/Plane/First_run/PRE5.txt")
#plane_run_3 = Data("Test_Data/Plane/Second_run/GPS2.txt", "Test_Data/Plane/Second_run/PRE2.txt")

for item in plane_run_1.parsed_data:
    print(item)

fig, ax1 = plt.subplots()
#ax1.plot(plane_run_1.distances, plane_run_1.heights, label = 'Run 1')
ax1.plot(plane_run_2.distances, plane_run_2.heights, label = 'Run 2')
plt.xlabel('Distance (meters)', fontsize = '22')
plt.ylabel('Height (meters)', fontsize = '22')
plt.legend()
plt.show()

#plane_run_1.latLonPlotter()
plane_run_2.latLonPlotter()
plt.show()

plt.plot(plane_run_1.heights)

plt.show()
"""
ax1.plot(castle_run_1.distances, castle_run_1.delta_h, label = 'Run 1')
ax1.plot(castle_run_2.distances, castle_run_2.delta_h, label = 'Run 2')
ax1.plot(castle_run_3.distances, castle_run_3.delta_h, label = 'Run 3')
ax1.plot(castle_run_4.distances, castle_run_4.delta_h, label = 'Run 4')
ax1.plot(castle_run_5.distances, castle_run_5.delta_h, label = 'Run 5')
plt.xlabel('Distance (meters)', fontsize = '22')
plt.ylabel('Height (meters)', fontsize = '22')


ax2 = ax1.twinx()
ax2.plot(castle_run_1.distances, averageArray(castle_run_1.temperatures))
ax2.plot(castle_run_2.distances, averageArray(castle_run_2.temperatures))
ax2.plot(castle_run_3.distances, averageArray(castle_run_3.temperatures))
ax2.plot(castle_run_4.distances, averageArray(castle_run_4.temperatures))
ax2.plot(castle_run_5.distances, averageArray(castle_run_5.temperatures))
ax2.set_ylabel('Temperature ($^\circ$C)')

print("Castle hill heights")
print(max(castle_run_1.delta_h))
print(max(castle_run_2.delta_h))
print(max(castle_run_3.delta_h))
print(max(castle_run_4.delta_h))
print(max(castle_run_5.delta_h))

plt.legend()
plt.show()
"""

# Look at moving average filterting
"""
leck_run_1 = Data("Test_Data/Leck/GPS1.txt", "Test_Data/Leck/PRE1.txt")

boxcar = leck_run_1.movingAverage(leck_run_1.heights, 25, 'boxcar')
triang = leck_run_1.movingAverage(leck_run_1.heights, 25, 'triang')
hamm = leck_run_1.movingAverage(leck_run_1.heights, 25, 'hamming')
plt.plot(leck_run_1.heights, label = 'Unfiltered')
plt.plot(boxcar, label = 'Boxcar')
plt.plot(triang, label = 'Triangle')
plt.plot(hamm, label = 'Hamming')
plt.legend()
plt.show()

pres = []
for item in castle_run_1.run_data:
    pres.append(item['pressure'])

pres_array = np.array(pres)
print(pres_array)
pres_fft = np.fft.fft(pres)
plt.plot(abs(pres_fft))
plt.show()


leck_run_2 = Data("Test_Data/Leck/GPS2.txt", "Test_Data/Leck/PRE2.txt")
leck_run_3 = Data("Test_Data/Leck/GPS3.txt", "Test_Data/Leck/PRE3.txt")
leck_run_4 = Data("Test_Data/Leck/GPS4.txt", "Test_Data/Leck/PRE4.txt")
leck_run_5 = Data("Test_Data/Leck/GPS5.txt", "Test_Data/Leck/PRE5.txt")
leck_run_6 = Data("Test_Data/Leck/GPS6.txt", "Test_Data/Leck/PRE6.txt")
leck_run_7 = Data("Test_Data/Leck/GPS7.txt", "Test_Data/Leck/PRE7.txt")
leck_run_8 = Data("Test_Data/Leck/GPS8.txt", "Test_Data/Leck/PRE8.txt")
leck_run_9 = Data("Test_Data/Leck/GPS9.txt", "Test_Data/Leck/PRE9.txt")
leck_run_10 = Data("Test_Data/Leck/GPS10.txt", "Test_Data/Leck/PRE10.txt")

fig, ax1 = plt.subplots()
leck_run_1.plotAltitudes('b', 'Run 1')
leck_run_2.plotAltitudes('r', 'Run 2')
leck_run_3.plotAltitudes('g', 'Run 3')
leck_run_4.plotAltitudes('m', 'Run 4')
leck_run_5.plotDistanceVsHeight()
leck_run_6.plotDistanceVsHeight()
leck_run_7.plotDistanceVsHeight()
leck_run_8.plotDistanceVsHeight()
leck_run_9.plotDistanceVsHeight()
leck_run_10.plotDistanceVsHeight()
#plt.show()

fig, ax1 = plt.subplots()
ax1.plot(leck_run_1.distances, leck_run_1.smooth_h, label = 'Run 1')
ax1.plot(leck_run_2.distances, leck_run_2.smooth_h, label = 'Run 2')
ax1.plot(leck_run_3.distances, leck_run_3.smooth_h, label = 'Run 3')
ax1.plot(leck_run_4.distances, leck_run_4.smooth_h, label = 'Run 4')
ax1.plot(leck_run_5.distances, leck_run_5.smooth_h, label = 'Run 5')
ax1.plot(leck_run_6.distances, leck_run_6.smooth_h, label = 'Run 6')
ax1.plot(leck_run_7.distances, leck_run_7.smooth_h, label = 'Run 7')
ax1.plot(leck_run_8.distances, leck_run_8.smooth_h, label = 'Run 8')
ax1.plot(leck_run_9.distances, leck_run_9.smooth_h, label = 'Run 9')
ax1.plot(leck_run_10.distances, leck_run_10.smooth_h, label = 'Run 10')
plt.xlabel('Distance (meters)', fontsize = '22')
plt.ylabel('Height (meters)', fontsize = '22')

ax2 = ax1.twinx()
ax2.plot(leck_run_1.distances, averageArray(leck_run_1.temperatures))
ax2.plot(leck_run_2.distances, averageArray(leck_run_2.temperatures))
ax2.plot(leck_run_3.distances, averageArray(leck_run_3.temperatures))
ax2.plot(leck_run_4.distances, averageArray(leck_run_4.temperatures))
ax2.plot(leck_run_5.distances, averageArray(leck_run_5.temperatures))
ax2.plot(leck_run_6.distances, averageArray(leck_run_6.temperatures))
ax2.plot(leck_run_7.distances, averageArray(leck_run_7.temperatures))
ax2.plot(leck_run_8.distances, averageArray(leck_run_8.temperatures))
ax2.plot(leck_run_9.distances, averageArray(leck_run_9.temperatures))
ax2.plot(leck_run_10.distances, averageArray(leck_run_10.temperatures))
ax2.set_ylabel('Temperature ($^\circ$C)')

plt.legend()
plt.show()

# Print max distnaces
print("Leckhampton Distaces")
print(max(leck_run_1.distances))
print(max(leck_run_2.distances))
print(max(leck_run_3.distances))
print(max(leck_run_4.distances))
print(max(leck_run_5.distances))
print(max(leck_run_6.distances))
print(max(leck_run_7.distances))
print(max(leck_run_8.distances))
print(max(leck_run_9.distances))
print(max(leck_run_10.distances))
print(" ")


print("Castle hill heights")
print(max(castle_run_1.delta_h))
print(max(castle_run_2.delta_h))
print(max(castle_run_3.delta_h))
print(max(castle_run_4.delta_h))
print(max(castle_run_5.delta_h))
"""
