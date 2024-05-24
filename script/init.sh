#!/bin/sh

CONTAINER_ID=$(docker ps | grep superset | awk '{ print $1 }')

docker exec $CONTAINER_ID superset fab create-admin \
             --username admin \
             --firstname Superset \
             --lastname Admin \
             --email admin@superset.com \
             --password admin

docker exec $CONTAINER_ID superset db upgrade
docker exec $CONTAINER_ID superset init

