#!/bin/sh

export PYTHONPATH="$PYTHONPATH:/home/pi/tally_pi/lib"
./scripts/run_server.py --config "/home/pi/tally_pi/tests/localsettings.conf"
