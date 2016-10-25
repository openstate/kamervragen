#!/bin/bash

cd /opt/duo

source ../bin/activate

# Download and update datasets
echo `date`: starting new download >> log/download_update.log
./manage.py extract start download >> log/download_update.log 2>&1
echo `date`: starting new update >> log/download_update.log
./manage.py extract start update >> log/download_update.log 2>&1
sleep 60
./bin/fix_aliases.py
