#!/bin/sh

exec -a "kafka-producer" python3 producer/producer_run.py $1 $2

