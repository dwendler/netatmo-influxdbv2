#!/usr/bin/python3
# encoding=utf-8

from pytz import timezone
import datetime
from influxdb_client import InfluxDBClient
import json
import lnetatmo
import os
import sys
import requests

#
debug_str=os.getenv("DEBUG", None)
if debug_str is not None:
  debug = debug_str.lower() == "true"
else:
  debug = False

# settings from EnvionmentValue
netatmo_clientId=os.getenv('NETATMO_CLIENT_ID', "")
netatmo_clientSecret=os.getenv('NETATMO_CLIENT_SECRET', "")
netatmo_username=os.getenv('NETATMO_USERNAME')
netatmo_password=os.getenv('NETATMO_PASSWORD')

# influx v2 env variables

influxdb2_host=os.getenv('INFLUXDB2_HOST', "localhost")
influxdb2_port=int(os.getenv('INFLUXDB2_PORT', "8086"))
influxdb2_org=os.getenv('INFLUXDB2_ORG', "org")
influxdb2_token=os.getenv('INFLUXDB2_TOKEN', "token")
influxdb2_bucket=os.getenv('INFLUXDB2_BUCKET', "netatmo")

# netatmo
authorization = lnetatmo.ClientAuth(clientId=netatmo_clientId,
                                clientSecret=netatmo_clientSecret,
                                username=netatmo_username,
                                password=netatmo_password)
devList = lnetatmo.WeatherStationData(authorization)

# influxdb v2
influxdb2_url="http://" + influxdb2_host + ":" + influxdb2_port
if debug:
  print (influxdb2_url)
client = InfluxDBClient(url=influxdb2_url, token=influxdb2_token, org=influxdb2_org)

# these keys are float
keylist=['Temperature', 'min_temp', 'max_temp', 'Pressure', 'AbsolutePressure', 'Rain', 'sum_rain_24', 'sum_rain_1']

def send_data(ds):
    #
    write_api = client.write_api()
    senddata={}
    dd=ds['dashboard_data']
    for key in dd:
        senddata["measurement"]=key
        senddata["time"]=datetime.datetime.fromtimestamp(dd['time_utc']).strftime("%Y-%m-%dT%H:%M:%S")
        if debug:
            print (senddata["time"])
        senddata["tags"]={}
        senddata["tags"]["host"]=ds['_id']
        senddata["tags"]["module"]=ds['module_name']
        if key in keylist:
            dd[key]=float(dd[key])
        senddata["fields"]={}
        senddata["fields"]["value"]=dd[key]
        if debug:
             print (json.dumps(senddata,indent=4))
        write_api.write(influxdb2_bucket, influxdb2_org, [senddata])

for name in devList.modulesNamesList():
    if debug:
        print ("--- module")
        print (name)
    ds=devList.moduleByName(name)
    if ds is None:
        continue
    if not 'dashboard_data' in ds:
        continue
    if debug:
        print (ds['_id'])
    send_data(ds)

for station_id in devList.stations:
    if debug:
        print ("--- station")
        print (station_id)
    ds=devList.stationById(station_id)
    if ds is None:
        continue
    if not 'dashboard_data' in ds:
        continue
    if debug:
        if 'station_name' in ds:
            print (ds['station_name'])
        else:
            print (station_id)
        print (ds['_id'])
    send_data(ds)
