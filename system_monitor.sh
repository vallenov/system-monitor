#!/usr/bin/sh

WORK_DIR=/home/vladimir/prog/python/projects/system-monitor

cd $WORK_DIR
if [ -d .venv ]
then
  venv=True
else
  venv=False
fi

if [ $venv = True ]
then
  . .venv/bin/activate && echo activate venv
else
  pyenv activate system-monitor && echo activate venv
fi

export FLASK_APP=system_monitor.py && echo export vars

echo System-monitor server is start

if [ $venv = True ]
then
  ./.venv/bin/flask run --host=0.0.0.0 --port=5112
else
  ~/.pyenv/versions/MessageSender/bin/flask run --host=0.0.0.0 --port=5112
fi
