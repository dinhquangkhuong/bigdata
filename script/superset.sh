#!/bin/sh

CONTAINER_ID=$(docker ps | grep postgres | awk '{ print $1 }')

docker exec --user root -it $CONTAINER_ID bash
