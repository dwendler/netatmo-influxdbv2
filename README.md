# netatmo-influxdbv2
Fetch data from the Netatmo API and place it in your influxdb. Based on turbosnute's [netatmo-influxdb](https://github.com/turbosnute/netatmo-influxdb), Manabuishii's [docker-netatmo-influxdb-python](https://github.com/manabuishii/docker-netatmo-influxdb-python),  and [netatmo2influxdb.py](https://pypi.org/project/netatmo2influxdb/).

Updated for InfluxDBv2.

## How to obtain Netatmo API Token
- Go to: https://dev.netatmo.com/
- Log in.
- Go to "My Apps"
- Click "Create"
- Write in the info...
- Click "Save"
- See your client id and client secret.

## InfluxDBv2 Setup

Assumes the following is already done:
- Setup InfluxDBv2
- Create Org
- Create Bucket
- Got Token

## How to run
```
$ docker run -d \
 -e NETATMO_CLIENT_ID="<NETATMO CLIENT ID>" \
 -e NETATMO_CLIENT_SECRET="<NETATMO CLIENT SECRET>" \
 -e NETATMO_USERNAME="<NETATMO USERNAME>" \
 -e NETATMO_PASSWORD="<NETATMO PASSWORD>" \
 -e INFLUXDB2_HOST="<INFLUXDBv2 SERVER>" \
 -e INFLUXDB2_PORT="8086" \
 -e INFLUXDB2_ORG="" \
 -e INFLUXDB2_TOKEN="" \
 -e INFLUXDB2_BUCKET="netatmo" \
 --name "netatmo-influxdb" \
dbsqp/netatmo-influxdbv2:latest
```

## Debug
To get more debug data add:
```
 -e DEBUG="true"
```
