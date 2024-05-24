#!/bin/sh

CONTAINER_ID=$(docker ps | grep postgres | awk '{ print $1 }')

docker exec -it $CONTAINER_ID psql -U postgres

docker exec -it $CONTAINER_ID bash
