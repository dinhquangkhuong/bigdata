#!/bin/sh

# exec -a "customerwillbekill" python3 customer/customer.py $1 > data/log$1.log
exec -a "customerwillbekill" python3 customer/customer.py $1
