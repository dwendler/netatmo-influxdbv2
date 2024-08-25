ARG ARCH=

# Pull base image
FROM ubuntu:24.04

# Setup external package-sources
RUN apt-get update && apt-get install -y \
    python3 \
    python3-dev \
    python3-setuptools \
    python3-pip \
    python3-virtualenv  \
    --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

# RUN pip install setuptools

#RUN pip3 install pytz influxdb-client requests lnetatmo==4.1.1 --break-system-packages
RUN pip3 install pytz influxdb-client requests --break-system-packages

# Environment vars
ENV PYTHONIOENCODING=utf-8

# Copy files
RUN mkdir -p /netatmo
ADD netatmo2influxdb.py /netatmo
ADD lnetatmo.py /netatmo
ADD get.sh /netatmo

# Run
WORKDIR "/netatmo"
CMD ["/bin/bash","./get.sh"]
