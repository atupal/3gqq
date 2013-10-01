#!/bin/bash
#uwsgi -s 127.0.0.1:5000 --socket-protocol http --pp ./ --module application --pidfile ~/tmp/uwsgi.pid

#python application.py
#export PY27_ATUPAL_ORG_CONFIG=/home/atupal/.config/myapp/py27_config.ini
#uwsgi -s /tmp/uwsgi.sock --pp ./ --module index:app --chmod-socket 666
#uwsgi_python27 -s 127.0.0.1:8000 --pp ./  --module index:app
#uwsgi_python27 -s 127.0.0.1:8000 --socket-protocol http --pp ./ --module index:app
python2 $(cd `dirname $0`; pwd)/index.py
