# Used Hardware

* Raspberry Pi 4
* mi flower sensor
    * Royal Gardineer works for me just  [search on amazon](https://www.amazon.de/Royal-Gardineer-Gie%C3%9Fanzeiger-4in1-Pflanzensensor-Feuchtigkeitsmesser/dp/B0746XKCGC/ref=sr_1_1?adgrpid=70276114519&dchild=1&gclid=Cj0KCQjwoub3BRC6ARIsABGhnyZDclxpqaf42ijxEPYca8ZViZO-RNQ9j0zm4tqhJLb-F_SxF_eV5m4aAh_gEALw_wcB&hvadid=353097392621&hvdev=c&hvlocphy=9060657&hvnetw=g&hvqmt=e&hvrand=6116598565721446160&hvtargid=kwd-754141135158&hydadcr=28018_1723953&keywords=mi+flora+sensor&qid=1593447668&sr=8-1&tag=googhydr08-21) on pearl you find the cheapest one. The most important thing is that they are based on Xiaomi Flower. µ

# copy raspberry image to sd card

On mac search for disk `diskutil list`

download rasbian image  I used `2020-05-27-raspios-buster-full-armhf.img` [link to current rasbian image!](https://www.raspberrypi.org/downloads/raspberry-pi-os/)

Then copy image to sd card with diskutil

First unmount: `diskutil unmountDisk /dev/diskN`, for me it was disk2. Afterwards you should see a output of_ `Unmount of all volumes on disk2 was successful`

Switch to the download folder and then copy the image with `sudo dd bs=1m if=2020-05-27-raspios-buster-full-armhf.img of=/dev/diskN; sync`, replace diskN with the disk you found under diskutil list.

Put disk again in raspberry and start. 

# pygarden
Clone the repo and build the docker `docker build -t pygarden .`. 

Afterwards start the container with : `docker run -e TZ=Europe/Amsterdam --rm -it --privileged --network host -v /home/pi/workspace/pygarden/output/:/output/ pygarden "--init"`

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

To visulize data simply call : 

`docker run -e TZ=Europe/Amsterdam --rm -it --privileged --network host -v /home/pi/workspace/pygarden/output/:/output/ pygarden "--visualize"`

You will find an rendered graph in `output/html/index.html`

To access the renderd graph, you can use the lightweight http server ```

install it via `sudp apt-get install lighthttpd`

Then add at `server.document-root = "/home/pi/workspace/pygarden/output/html/"`
Then restart lighthttpd `sudo service lighthttpd force-reload`


![Sensor HTML Example](https://github.com/marcmueller86/pygarden/blob/master/doc/sensors_html.png?raw=true)
