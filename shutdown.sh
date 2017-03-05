#!/bin/bash
SPLASH_PID=`ps -ef | pgrep -f splash`
sudo kill ${SPLASH_PID}
echo "Splash stopped"

echo "Stopping Docker with password: "
sudo systemctl stop docker
echo "Docker is stopped"
