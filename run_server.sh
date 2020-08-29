#!/bin/sh

export PYTHONPATH="$PYTHONPATH:$HOME/Projects/tally_pi/lib"
cd srv/tallypi
../../scripts/run_server.py --config "$HOME/Projects/tally_pi/tests/localsettings.conf"
