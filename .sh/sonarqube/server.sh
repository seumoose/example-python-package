#!/usr/bin/env bash

SONAR_CONTAINER="sonarqube"


if [ ! "$(docker ps -a -q -f name=$SONAR_CONTAINER)" ]; then
    # check if container doesn't exist and run container
    docker pull sonarqube
    docker run -d --restart unless-stopped --name $SONAR_CONTAINER -p 8080:9000 sonarqube:latest
else
    docker start $SONAR_CONTAINER
fi

read -rsp $'Press any key to stop the sonarqube container...\n' -n1 key
echo "Stopping the sonarqube container..."

docker stop "${SONAR_CONTAINER}"