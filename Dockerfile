# Python Base Image from https://hub.docker.com/r/arm32v7/python/
FROM arm32v7/python:latest

RUN pip install docopt bluepy miflora btlewrap==0.0.8 pandas
RUN pip install plotly
RUN apt-get update
RUN apt-get install bluez bluez-tools build-essential libbluetooth-dev  -y

COPY config ./
COPY src ./
# Trigger Python script
ENTRYPOINT ["python", "./sensor_fetcher.py"]