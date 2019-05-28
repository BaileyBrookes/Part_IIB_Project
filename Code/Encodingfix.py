################################################################################
# Encoidngfix.py
#
# PURPOSE: Some GP NMEA sentace are corrput, this is experimenting with a parser
#          to overcome this.
#
# Written by: Bailey Brookes
# Supervisor: Dr Paul Robertson
################################################################################

import codecs
import csv
u = "347, GPGGA,133004.200,5212.0919,N,00005.8888,E,2,08,0.97,-2.1,M,47.0, } �!� �  "
u.encode('ascii', 'replace')
#print(u)

parsed_data = []
with codecs.open("Test_Data/Leck/GPS8.txt",'r', encoding='utf-8', errors = 'ignore') as file:
    csvfile = csv.reader(x.replace('\0', '') for x in file)
    for row in csvfile:
        if row == []:
            continue

        if(len(row) < 12):
            print('Not complete data')
            continue

        reading_no = int(row[0])
        timestamp = row[2]
        latDMS = str(row[3])
        lonDMS = str(row[5])
        latitude = float(latDMS[0:2]) + float(latDMS[2:])/60
        longitude = float(lonDMS[0:3])*100 + float(lonDMS[3:])/60
        altitude = row[10]

        parsed_data.append({'Num': reading_no , 'timestamp' : timestamp, 'latitude'  : latitude,'longitude' : longitude, 'altitude' : altitude})
for item in parsed_data:
    print(item)
