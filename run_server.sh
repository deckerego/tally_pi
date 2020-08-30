#!/bin/sh

export PYTHONPATH="$PYTHONPATH:$HOME/Projects/tally_pi/lib"
./scripts/run_server.py --config "$HOME/Projects/tally_pi/tests/localsettings.conf"
