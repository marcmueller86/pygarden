# pygarden
Clone the repo and build the docker `docker build -t pygarden .`. 

Afterwards start the container with : `docker run -e TZ=Europe/Amsterdam --rm -it --privileged --network host -v /home/pi/workspace/pygarden/output/:/output/ pygarden`

Images is built on raspberry pi with arm32v7 as base. 

With `crontab -e` we add the following line:

`*/1 * * * *  /usr/bin/docker run -e TZ=Europe/Amsterdam --rm -it --privileged --network host -v /home/pi/workspace/pygarden/output/:/output/ pygarden`

To check the database install sqllite3

`sudo apt-get install sqlite3`

change to output folder of pygarden

`sqlite3 -column -header`
`.open "sensor_data.db"`
`SELECT * FROM sensor_data;`

You can dump the tabel to output as `data_sensor.csv`

`/usr/bin/docker run -e TZ=Europe/Amsterdam --rm -it --privileged --network host -v /home/pi/workspace/pygarden/output/:/output/ pygarden "--export"`

With `crontab -e` we add the following line for a 30 minutes interval export:
`*/30 * * * * /usr/bin/docker run -e TZ=Europe/Amsterdam --rm --privileged --network host -v /home/pi/workspace/pygarden/output/:/output/ pygarden "--export"`