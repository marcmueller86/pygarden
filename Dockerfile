# Python Base Image from https://hub.docker.com/r/arm32v7/python/
FROM arm32v7/python:latest

# Copy the Python Script to blink LED
COPY config ./
COPY src ./
RUN apt-get update
RUN apt-get install -y python-pandas
RUN pip install docopt bluepy miflora btlewrap==0.0.8

# Trigger Python script
CMD ["python", "./sensor_fetcher.py"]