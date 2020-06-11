#!/usr/bin/env python3
# encoding: utf-8
'''Usage: sensor_fetcher.py [--init] [--export]

Fetch miflora bluettooth sensor data

Options:
    --init
    --export
'''

from docopt import docopt
from miflora.miflora_poller import MiFloraPoller
from btlewrap.gatttool import GatttoolBackend
import time
from datetime import datetime
import sys
import pandas as pd
import json
import sqlite3

class SensorFetcher(object):
    """Sensor fetching class. Iterate over sensor config and fetch data from miflora based sensors. Enriching data and creating json object to store it in database.

    """
    sensor_template = {
    'mac': None, 
    'name': None, 
    'temperature': None, 
    'light': None, 
    'moisture': None, 
    'conductivity': None, 
    'battery': None,
    'ts_utc': None, 
    'date_iso': None,
    'firmware': None
    }
    engine = None
    database_name = None
    conn = None

    def __init__(self, database_name):
        """Init with database name to create a connection

        Args:
            database_name ([string]): name of the database
        """
        self.conn = sqlite3.connect("output/%s.db" % database_name)

    def create_table(self):
        """If init we create an empty sql table
        """
        c = self.conn.cursor()
        c.execute("CREATE TABLE sensor_data (mac text, name text, temperature real, light integer, moisture real, conductivity real, battery real, ts_utc int, date_iso text, firmware text )")

    def get_sensor_data(self):
        """ iterating over the sensor names to collect the sensor data for every sensor

        Returns:
            [array]: array with dictionaries based on sensor_template
        """
        sensor_config = self.load_sensor_config()
        now_utc = datetime.utcnow()
        now = datetime.now()
        sensor_data = []
        for sensor, address in sensor_config.items():
            sensor_data.append(self.fetch_data(sensor, address, now_utc, now))
        return sensor_data

    def load_sensor_config(self):
        """loading sensor data (names and mac addresses) from json config file
        
        Returns:
            [dict]: all sensors with mac addresses
        """
        with open('sensor_config.json') as json_file:
            sensor_config = json.load(json_file)
        return sensor_config

    def write_sensor_data_to_db(self, sensor_data):
        """Writing json sensor data array to sqllite database 

        Args:
            sensor_data ([array]): json per line array with data from sensor fetching process
        """
        df = pd.DataFrame(sensor_data)
        df.to_sql('sensor_data', self.conn, if_exists='append', index = False)

    def export_sensor_data_to_csv(self):
        """Dumping whole sqllite database to csv
        """
        df = pd.read_sql('SELECT * FROM sensor_data', self.conn)
        df.to_csv('output/sensor_data.csv', index=False)

    def fetch_data(self, sensor, address, now_utc, now):
        """Fetching sensor data for a specific sensor

        Args:
            sensor ([string]): name of sensor from config
            address ([string]): mac address of the sensor from config
            now_utc ([datatime]): utc datetime object
            now ([datatime]): local datetime object

        Returns:
            [array]: filled sensor template with sensor data
        """
        poller = MiFloraPoller(address, GatttoolBackend)
        ts_utc = int(now_utc.strftime("%s"))
        temp_sensor = self.sensor_template.copy()
        temp_sensor['mac'] = address
        temp_sensor['name'] = sensor
        # liefert den Temperaturwert (in Grad Celsius)
        temp_sensor['temperature'] = poller.parameter_value("temperature")
        # gibt die lichtstaerke an
        temp_sensor['light'] = poller.parameter_value("light")
        # gibt die Feuchtigkeit an
        temp_sensor['moisture'] = poller.parameter_value("moisture")
        # gibt die Leitfaehigkeit des Bodens an.
        temp_sensor['conductivity'] = poller.parameter_value("conductivity")
        temp_sensor['battery'] = poller.parameter_value("battery")
        temp_sensor['date_iso'] = now.replace(microsecond=0).isoformat()
        temp_sensor['ts_utc'] = ts_utc
        # poller.firmware_version() # – liefert die aktuelle Firmware Version als Text.
        temp_sensor['firmware'] = poller.firmware_version()
        return temp_sensor

if __name__ == '__main__':
    """Executing data collection

    """
    arguments = docopt(__doc__)
    # print (arguments)
    database_name = 'sensor_data'
    sensor_fetch = SensorFetcher(database_name)
    if '--init' in arguments and arguments['--init'] == True:
        sensor_fetch.create_table()
    if '--export' in arguments and arguments['--init'] == True:
        sensor_fetch.export_sensor_data_to_csv()
    else:
        sensor_data = sensor_fetch.get_sensor_data()
        sensor_fetch.write_sensor_data_to_db(sensor_data)
    # print ("We gathered data of %d sensor" % len(sensor_data))
