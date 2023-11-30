FROM ghcr.io/osgeo/gdal:ubuntu-small-3.8.0

RUN apt-get update && \
    apt-get install -y \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

RUN export CPLUS_INCLUDE_PATH=/usr/include/
RUN export C_INCLUDE_PATH=/usr/include/

COPY remote_sensing remote_sensing/
WORKDIR remote_sensing/
RUN pip install -r requirements.txt
