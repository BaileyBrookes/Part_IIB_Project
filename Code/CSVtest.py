################################################################################
# CSVtest..py
#
# PURPOSE: Learing how to read CSV files
#
# Written by: Bailey Brookes
# Supervisor: Dr Paul Robertson
################################################################################

import csv

parsed_data = []

with open('Test_Data/Leck/GPS5.txt') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        row = [entry.decode("utf-8", 'replace') for entry in row]
        if row == []:
            continue

        if(len(row) < 12):
            print('Not complete data')
            continue

        reading_no = row[0]
        timestamp = row[2]
        latDMS = str(row[3])
        lonDMS = str(row[5])
        latitude = float(latDMS[0:2]) + float(latDMS[2:])/60
        longitude = float(lonDMS[0:3])*100 + float(lonDMS[3:])/60
        altitude = row[10]

        parsed_data.append({'Num': reading_no , 'timestamp' : timestamp, 'latitude'  : latitude,'longitude' : longitude, 'altitude' : altitude})
        print(parsed_data)
    csv_file.close()
csv_file.close()
