#!/bin/sh

. venv/bin/activate

superset run -p 8088 --with-threads
