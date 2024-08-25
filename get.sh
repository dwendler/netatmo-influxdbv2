#!/bin/bash

while :
do
  date
  echo "--- Start Call API"
  python3 netatmo2influxdb.py
  RET=$?
  if [ ${RET} -ne 0 ];
  then
    echo "Exit status not 0 - waiting for one minute"
    echo "Sleep 60"
    sleep 60
  fi
  date
  echo "query Netatmo API in 15 minutes again"
  sleep 900
done
