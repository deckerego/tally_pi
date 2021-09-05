#!/usr/bin/env bash

if [[ -z "$1" ]]; then
  echo "Usage: $0 IP_ADDR"
  exit -1
fi

HOSTNAME="$1"

for i in {1..5}; do
  time curl "http://$HOSTNAME:7413/set?color=FF0000&brightness=0.1"
  time curl "http://$HOSTNAME:7413/set?color=00FF00&brightness=0.1"
  time curl "http://$HOSTNAME:7413/set?color=00FF00&brightness=0.1"
  time curl "http://$HOSTNAME:7413/set?color=FFFFFF&brightness=0.1"

  open -a "/Applications/Google Chrome.app" "http://$HOSTNAME:7413/status"

  time curl "http://$HOSTNAME:7413/set?color=55AAFF&brightness=0.5"
  time curl "http://$HOSTNAME:7413/set?color=FFAA55&brightness=0.5"
  time curl "http://$HOSTNAME:7413/set?color=BB3377&brightness=0.5"
  time curl "http://$HOSTNAME:7413/set?color=000000&brightness=0.5"

  open -a "/Applications/Google Chrome.app" "http://$HOSTNAME:7413/status"

  time curl "http://$HOSTNAME:7413/set?color=0000FF&brightness=0.1"
  time curl "http://$HOSTNAME:7413/set?color=00FFFF&brightness=0.1"
  time curl "http://$HOSTNAME:7413/set?color=FFFF00&brightness=0.1"
  time curl "http://$HOSTNAME:7413/set?color=FF0000&brightness=0.1"
done

time curl "http://$HOSTNAME:7413/set?color=000000&brightness=0.0"

echo "With current settings this should take approx 15 seconds"
