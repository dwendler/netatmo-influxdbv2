#!/usr/bin/python3
# encoding=utf-8

from pytz import timezone
import datetime
from influxdb_client import InfluxDBClient, Point, WriteOptions
from influxdb_client.client.write_api import SYNCHRONOUS
import json
import lnetatmo
import os
import sys
import requests


# debug enviroment varable
debug_str=os.getenv("DEBUG", None)
if debug_str is not None:
  debug = debug_str.lower() == "true"
else:
  debug = False


# netatmo envionment variables
netatmo_clientId=os.getenv('NETATMO_CLIENT_ID', "")
netatmo_clientSecret=os.getenv('NETATMO_CLIENT_SECRET', "")
netatmo_username=os.getenv('NETATMO_USERNAME')
netatmo_password=os.getenv('NETATMO_PASSWORD')


# influxDBv2 envionment variables
influxdb2_host=os.getenv('INFLUXDB2_HOST', "localhost")
influxdb2_port=int(os.getenv('INFLUXDB2_PORT', "8086"))
influxdb2_org=os.getenv('INFLUXDB2_ORG', "org")
influxdb2_token=os.getenv('INFLUXDB2_TOKEN', "token")
influxdb2_bucket=os.getenv('INFLUXDB2_BUCKET', "netatmo")


# hard encoded envionment varables


# report debug status
if debug:
    print ( " debug: TRUE" )
else:
    print ( " debug: FALSE" )


# netatmo
authorization = lnetatmo.ClientAuth(clientId=netatmo_clientId, clientSecret=netatmo_clientSecret, username=netatmo_username, password=netatmo_password)
devList = lnetatmo.WeatherStationData(authorization)


# influxDBv2
influxdb2_url="http://" + influxdb2_host + ":" + str(influxdb2_port)
if debug:
    print ( "influx: "+influxdb2_url )

client = InfluxDBClient(url=influxdb2_url, token=influxdb2_token, org=influxdb2_org)


# these keys are float
keylist=['Temperature', 'min_temp', 'max_temp', 'Pressure', 'AbsolutePressure', 'Rain', 'sum_rain_24', 'sum_rain_1']

# these keys are skipped
skiplist=['temp_trend', 'pressure_trend', 'date_min_temp', 'date_max_temp', 'max_temp', 'min_temp', 'AbsolutePressure', 'time_utc']

# these keys are outside
outsidelist=['Rain']


# pass data to InfluxDB
def send_data(ds):
    write_api = client.write_api(write_options=SYNCHRONOUS)
    
    senddata={}
    dd=ds['dashboard_data']
    for key in dd:
        if key in skiplist:
            if debug:
                print ( "Skipped "+key )
            continue

        if key in keylist:
            value=float(dd[key])
        else:
            value=dd[key]    
   
        if key in outsidelist:
            host = "Outside"
        else:
            host = ds['module_name']

        time = datetime.datetime.fromtimestamp(dd['time_utc']).strftime("%Y-%m-%dT%H:%M:%SZ")

        senddata["measurement"]=key
        senddata["time"]=time
        senddata["tags"]={}
        senddata["tags"]["source"]="Netatmo"
        senddata["tags"]["host"]=host
        senddata["tags"]["module"]=ds['_id']
        senddata["fields"]={}
        senddata["fields"]["value"]=value
        if debug:
             print (json.dumps(senddata,indent=4))
        write_api.write(bucket=influxdb2_bucket, org=influxdb2_org, record=[senddata])


# pass stations
for station_id in devList.stations:
    if debug:
        print ( "\ntype: Station" )
    ds=devList.stationById(station_id)
    if ds is None:
        continue
    if not 'dashboard_data' in ds:
        continue
    if debug:
        if 'station_name' in ds:
            print ("name: "+ds['station_name'])
        else:
            print ("id: "+station_id)
    send_data(ds)


# pass modules
for name in devList.modulesNamesList():
    if debug:
        print ( "\ntype: Module" )
    ds=devList.moduleByName(name)
    if ds is None:
        continue
    if not 'dashboard_data' in ds:
        continue
    if debug:
        print ( "  id: "+ds['_id'])
    send_data(ds)
