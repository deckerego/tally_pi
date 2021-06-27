#!/bin/sh

export PYTHONPATH="$PYTHONPATH:$PWD/lib"
./scripts/run_server.py --config "$PWD/tests/localsettings.conf"
