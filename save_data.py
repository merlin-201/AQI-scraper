import csv
from prettyprint import *
from math import nan

#data = {'StationName': 'Alipur, Delhi - DPCC', 'DateTime': '12 Dec 2020 11:00 PM', 'AQI': 409, 'Pollutants': {'PM2.5': {'avg_value': '409', 'min_value': '338', 'max_value': '466'}, 'PM10': {'avg_value': '325', 'min_value': '209', 'max_value': '411'}, 'NO2': {'avg_value': '36', 'min_value': '26', 'max_value': '87'}, 'NH3': {'avg_value': '', 'min_value': '-', 'max_value': '-'}, 'SO2': {'avg_value': '13', 'min_value': '10', 'max_value': '18'}, 'CO': {'avg_value': '89', 'min_value': '55', 'max_value': '108'}, 'OZONE': {'avg_value': '9', 'min_value': '2', 'max_value': '19'}}}


csv_columns = [
    'StationName',
    'DateTime',
    'AQI',
    'PM2.5',
    'PM10',
    'NO2',
    'CO',
    'OZONE',
    'NH3',
    'SO2'
]


def save(data):

    for pollutant,values in data['Pollutants'].items():
        data[pollutant] = values['avg_value']

    del data['Pollutants']

    #dprint(data)

    try:
        with open('data.csv', 'x') as f:
            writer = csv.DictWriter(f, fieldnames=csv_columns)
            writer.writeheader()
    except:
        pass

    try:
        with open('data.csv', 'a') as f:
            row = ""
            row += '\"' + data['StationName'] + '\"' + ","
            row += data['DateTime'] + ","
            row += str(data['AQI']) + ","
            row += data['PM2.5'] + ","
            row += data['PM10'] + ","
            row += data['NO2'] + ","
            row += data['CO'] + ","
            row += data['OZONE'] + ","
            row += data['NH3'] + ","
            row += data['SO2'] + "\n"

            f.write(row)
    except IOError:
        print("I/O error")
