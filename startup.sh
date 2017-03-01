#!/bin/bash

echo "Starting Docker with password: "
sudo systemctl start docker

while true; do
    ps -ef | pgrep -f docker-containerd
    if [ $? = 0 ]
    then
        echo "Docker started"
        break
     fi
    echo "Still waiting for Docker to startup"
    sleep 5
done

echo "Starting Splash"
sudo docker run -d -p 8050:8050 scrapinghub/splash &
SPLASH_PID=`ps -ef | pgrep -f splash`
sleep 10

python main.py

sudo kill ${SPLASH_PID}
echo "Splash stopped"

echo "Stopping Docker with password: "
sudo systemctl stop docker
echo "Docker is stopped"
