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
RUN curl -LO https://github.com/yannforget/landsatxplore/archive/refs/heads/master.tar.gz
RUN tar -zxvf master.tar.gz
RUN mv landsatxplore-master/landsatxplore/ /usr/local/lib/python3.10/dist-packages/landsatxplore/
