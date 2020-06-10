# Python Base Image from https://hub.docker.com/r/arm32v7/python/
FROM amancevice/pandas:latest

# Copy the Python Script to blink LED
COPY config ./
COPY src ./

RUN pip install --no-cache-dir docopt bluepy miflora btlewrap

# Trigger Python script
CMD ["python", "./sensor_fetcher.py"]