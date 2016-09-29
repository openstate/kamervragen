#!/bin/bash

source /opt/bin/activate

cd /opt/duo

service elasticsearch restart
service redis-server restart

sleep 20

./start_email.py

supervisord -n -c conf/supervisor.conf
