# netatmo-influxdbv2
Docker image to fetch data from the Netatmo API and place it in your influxdb. Based on turbosnute's [netatmo-influxdb](https://github.com/turbosnute/netatmo-influxdb), Manabuishii's [docker-netatmo-influxdb-python](https://github.com/manabuishii/docker-netatmo-influxdb-python), and [netatmo2influxdb.py](https://pypi.org/project/netatmo2influxdb/). All use [lnetatmo](https://github.com/philippelt/netatmo-api-python).

Updated for InfluxDBv2. Added upload of signal strength and battery percentage.

## Netatmo API Token
1. Go to: https://dev.netatmo.com/
2. Log in.
3. Go to "My Apps"
4. Click "Create"
4. Fill out info...
5. Click "Save"
6. Get your client id and client secret
7. Generate token with scope read_station
8. Get your refresh token

## InfluxDBv2 Setup

Setup InfluxDBv2, create bucket and create a totken with write permissions for said bucket.

## Docker Setup
https://hub.docker.com/repository/docker/dbsqp/netatmo-influxdbv2
```
$ docker run -d \
 -e NETATMO_CLIENT_ID="<NETATMO CLIENT ID>" \
 -e NETATMO_CLIENT_SECRET="<NETATMO CLIENT SECRET>" \
 -e NETATMO_TOKEN="<NETATMO REFRESH TOKEN>" \
 -e INFLUXDB2_HOST="<INFLUXDBv2 SERVER>" \
 -e INFLUXDB2_PORT="8086" \
 -e INFLUXDB2_ORG="Home" \
 -e INFLUXDB2_TOKEN="" \
 -e INFLUXDB2_BUCKET="Staging" \
 --name "Netatmo-InfluxDBv2" \
dbsqp/netatmo-influxdbv2:latest
```

# Options
```
 -e INFLUXDB2_SSL="true"
 -e INFLUXDB2_SSL_VERIFY="TRUE"
```

# Debug
To report out further details in the log enable debug:
```
 -e DEBUG="true"
```
# Status
Updated for lnetatmo oauth.
