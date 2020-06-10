# Python Base Image from https://hub.docker.com/r/arm32v7/python/
FROM arm32v7/python:latest

# Copy the Python Script to blink LED
COPY config ./
COPY src ./

RUN pip install pandas docopt bluepy miflora

# Trigger Python script
CMD ["python", "./sensor_fetcher.py"]