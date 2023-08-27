#!/bin/bash

status() {
  pid=$(ps -ef | grep fantasy.py | grep -v grep | awk '{print $2}')
  if [ -z "$pid" ]
    then
      echo "Not running"
    else
      echo "Running with pid $pid"
  fi
}

start() {
  pid=$(ps -ef | grep fantasy.py | grep -v grep | awk '{print $2}')
  if [ -z "$pid" ]
    then
      SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
      cd $SCRIPT_DIR
      source venv/bin/activate
      nohup python fantasy.py &
  fi
}

stop() {
  pid=$(ps -ef | grep fantasy.py | grep -v grep | awk '{print $2}')
  if [ -n "$pid" ]
    then
      kill -9 $pid
  fi
}

update() {
  git reset --hard
  git pull origin master
}

case "$1" in
    'start')
            start
            status
            ;;
    'stop')
            stop
            status
            ;;
    'restart')
            stop
            start
            status
            ;;
    'status')
            status
            ;;
    'update')
            update
            ;;
    *)
            echo "Usage: $0 { start | stop | restart | status | status }"
            exit 1
            ;;
esac

exit 0
