# pygarden
Clone the repo and build the docker `docker build -t pygarden .`. 

Afterwards start the container with : `docker run --rm -it --privileged --network host -v /home/pi/workspace/pygarden/output/:/output/ pygarden`

Images is built on raspberry pi with arm32v7 as base. 

With `crontab -e` we add the following line:

`*/1 * * * *  /usr/bin/docker run --rm --privileged --network host -v /home/pi/workspace/pygarden/output/:/output/ pygarden`