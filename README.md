# netatmo-influxdbv2
Docker image to fetch data from the Netatmo API and place it in your influxdb. This project is based on the following projects: 
* Initiator of netatmo-api-python with great documentation [lnetatmo](https://github.com/philippelt/netatmo-api-python).
* turbosnute's [netatmo-influxdb](https://github.com/turbosnute/netatmo-influxdb)
* Manabuishii's [docker-netatmo-influxdb-python](https://github.com/manabuishii/docker-netatmo-influxdb-python)
* dbsqp's fork from turbosnute with Influx DB v2 [fork to store data in Influx v2](https://github.com/dbsqp/netatmo-influxdbv2)

* created new Docker file with new base image, new Python version and latest lnetatmo version
* fixed lnetatmo module to report module data from default station
* fixed "netatmo2influxdb.py" script to support insecure Influx connections
* modified "netatmo2influxdb.py" script to use json file that stores the netatmo authentication tokens. The file must be writeable. The refresh token will be updated by the latest lnetatmo module after each request. This is due to breaking change in the Netatmo API.

  

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


![image](https://github.com/user-attachments/assets/3fbffbd2-3726-4d65-a77e-5134e8b5e923)




## InfluxDBv2 Setup

Setup InfluxDBv2, create bucket and create a token with write permissions for said bucket. 

## Docker Image creation
Newer Ubuntu base image, latest lnetatmo module with modifications and enhanced netatmo2influxdb.py script to use oauth using a credential file for clientID, client Token and refresh token. 


## Docker Setup
https://hub.docker.com/repository/docker/dbsqp/netatmo-influxdbv2
```
docker run -d \
 -v /config/netatmo/.netatmo.credentials:/netatmo/.netatmo.credentials \
 -e INFLUXDB2_HOST="influxdb" \
 -e INFLUXDB2_PORT="8086" \
 -e INFLUXDB2_ORG="Home" \
 -e INFLUXDB2_TOKEN="InfluxDbToken" \
 -e INFLUXDB2_BUCKET="netatmo" \
 -e INFLUXDB2_SSL="True" \
 -e INFLUXDB2_SSL_VERIFY="False" \
 -e DEBUG="true" \
 --network "iot" \
 --name "netatmo" \
 netatmo:latest
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
