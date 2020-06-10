# Python Base Image from https://hub.docker.com/r/arm32v7/python/
FROM arm32v7/python:latest

# Copy the Python Script to blink LED
RUN pip install docopt bluepy miflora btlewrap==0.0.8 pandas

COPY config ./
COPY src ./

# Trigger Python script
CMD ["python", "./sensor_fetcher.py"]