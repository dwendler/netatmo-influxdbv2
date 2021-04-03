# netatmo-influxdbv2
Fetch data from the Netatmo API and place it in your influxdb. Based on turbosnute's [netatmo-influxdb](https://github.com/turbosnute/netatmo-influxdb), Manabuishii's [docker-netatmo-influxdb-python](https://github.com/manabuishii/docker-netatmo-influxdb-python),  and [netatmo2influxdb.py](https://pypi.org/project/netatmo2influxdb/).

Updated for InfluxDBv2. Added upload of signal strength and battery percentage.

## Netatmo API Token
- Go to: https://dev.netatmo.com/
- Log in.
- Go to "My Apps"
- Click "Create"
- Write in the info...
- Click "Save"
- See your client id and client secret.

## InfluxDBv2 Setup

Setup InfluxDBv2, create bucket and create a totken with write permissions for said bucket.

## Docker Setup
```
$ docker run -d \
 -e NETATMO_CLIENT_ID="<NETATMO CLIENT ID>" \
 -e NETATMO_CLIENT_SECRET="<NETATMO CLIENT SECRET>" \
 -e NETATMO_USERNAME="<NETATMO USERNAME>" \
 -e NETATMO_PASSWORD="<NETATMO PASSWORD>" \
 -e INFLUXDB2_HOST="<INFLUXDBv2 SERVER>" \
 -e INFLUXDB2_PORT="8086" \
 -e INFLUXDB2_ORG="Home" \
 -e INFLUXDB2_TOKEN="" \
 -e INFLUXDB2_BUCKET="Staging" \
 --name "Netatmo-InfluxDBv2" \
dbsqp/netatmo-influxdbv2:latest
```

## Debug
To report out further details in the log enable debug:
```
 -e DEBUG="true"
```
