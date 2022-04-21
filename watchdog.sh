#!/bin/bash
# run ny cron 
cd /usr/local/python/beacon
if ! ps aux | grep "[r]xdaemon.py" >/dev/null; then
  python3 rxdaemon.py >/dev/null  &
fi
if ! ps aux | grep "[t]xdaemon.py" >/dev/null; then
  python3 txdaemon.py >/dev/null  &
fi
if ! ps aux | grep "[d]xbeacon.py" >/dev/null; then
  python3 dxbeacon.py >/dev/null  &
fi
