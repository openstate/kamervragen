#!/bin/bash

cd /opt/duo

source ../bin/activate

# Download and update datasets
./manage.py extract start download
./manage.py extract start update
sleep 60
./bin/fix_aliases.py
